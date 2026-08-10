# Transactional email delivery via an outbox table

**Status:** Implemented (phase 1)

**Summary:** We moved transactional email off inline sending and onto an outbox table, which
removed the duplicate-send class of bug entirely and cut p99 checkout latency by 240 ms.

## Where we are

Transactional email used to be synchronous. The checkout handler called the provider's HTTP API
inside the request, and a provider timeout either blocked checkout or produced a duplicate send
when the client retried.

We moved delivery into an outbox table, so the handler writes a row in the same transaction as
the order and a worker drains the table. 14 of 15 call sites now go through the outbox.

The digest worker writes its rows to the outbox table and drains them on the same five-second
tick as everything else, which is why digest and receipt email share a rate limiter.

The retry policy backs off exponentially to a 6-hour ceiling and gives up after 11 attempts. A
row that exhausts its attempts moves to `outbox_failed` and pages the on-call.

## What we will build

The dispatcher will read a batch of 200 rows per tick, claim them with a `SELECT ... FOR UPDATE
SKIP LOCKED`, and mark each row terminal before releasing the lock
(`app/workers/outbox_dispatcher.rb`). This will make a double-delivery impossible even if two
dispatchers run concurrently.

The dispatcher costs 14 writes per batch, so the write amplification against the current inline
path is roughly 1.4x.

Both paths write to the same table, and the reconciler compares them nightly to catch drift.

We should route provider webhooks back into the outbox so a bounce updates the originating row.
The provider signs its webhooks, and the verification helper already exists, so this is a small
piece of work.

Per-tenant rate limiting will land with the dispatcher. A tenant that exceeds its hourly ceiling
has its rows deferred rather than dropped, and the deferral is invisible to the sender.

## Risks

| Risk | Mitigation |
|---|---|
| A poison row blocks the batch | Terminal-marking before release; the row moves to `outbox_failed` after 11 attempts |
| Duplicate sends under concurrent dispatchers | `SKIP LOCKED` claim plus terminal marking |
| The outbox table grows without bound | A lifecycle job deletes terminal rows after 30 days |
| Digest email starves receipt email behind a shared rate limiter | Split the limiter per message class |
| The provider's webhook signature helper rejects valid payloads | Verify against the recorded fixtures before enabling |

## Gotchas for whoever picks this up

The `outbox` table has no index on `(status, run_after)`, so the dispatcher's claim query does a
sequential scan once the table passes about 200k rows.

The provider returns 202 for a message it has accepted and 200 for one it has deduplicated on
its side, and treating both as success is what hid the original duplicate-send bug.

`OutboxRow#deliver!` swallows `Net::ReadTimeout` and returns nil, so a timeout looks like a
successful no-op to the caller.

The reconciler runs at 03:00 UTC and holds a table lock for the duration, so a long run overlaps
the European morning.

## Rollout

Phase 1 writes rows to the outbox and keeps sending inline, so the table fills and nothing reads
it. Phase 2 turns on the dispatcher for one tenant. Phase 3 turns off the inline path. Phase 4
removes the inline code.

Currently the inline path is the only one that actually delivers, and the dispatcher is a no-op.

---

## Appendix A — flag and deployment state as of 2026-08-09

| Flag | Default | Production state |
|---|---|---|
| `outbox_writes` | on | on for all tenants since 2026-03-11 |
| `outbox_dispatch` | off | off for all tenants; never enabled outside staging |
| `outbox_webhooks` | off | off; the code is merged but the route is not mounted |
| `outbox_rate_limit` | off | off; no implementation merged, flag reserved |

The digest worker's outbox path sits behind `outbox_dispatch`, so it has never run in
production. The digest mailer continues to call the provider directly.

## Appendix B — call site inventory

15 call sites send transactional email. 14 write to the outbox. The remaining one is
`LegacyInvoiceMailer#deliver_now`, called from the quarterly invoicing rake task, which still
calls the provider inline and therefore still carries the duplicate-send risk on retry. It was
excluded from the March migration because the rake task runs outside the request cycle and the
migration was scoped to request-path sends.

## Appendix C — measurements

| Measurement | Value | When |
|---|---|---|
| Dispatcher writes per 200-row batch | 14 | one staging run, 2026-07-14 |
| p99 checkout latency, inline path | 1,180 ms | production, week of 2026-03-03 |
| p99 checkout latency, after outbox writes | 940 ms | production, week of 2026-03-17 |
| Sequential scan threshold on `outbox` | ~200k rows | staging, 2026-06-02 |

The 240 ms figure in the summary is the difference between the two latency rows. It measures
turning on outbox *writes*, not dispatch, and no dispatch has run in production.

## Appendix D — history

The inline send path was written in 2019 and has not changed materially since. The duplicate-send
bug was first reported in 2021 and reproduced in 2024. The outbox design was accepted in
February 2026 and phase 1 shipped on 2026-03-11.
