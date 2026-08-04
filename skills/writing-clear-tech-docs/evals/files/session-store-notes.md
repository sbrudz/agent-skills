# Session Store Consolidation

**Status:** draft · **Author:** M. Okonkwo · 2026-06-30

## Background

This document covers the session store work. There are currently three session stores in production.
The cookie store is used by the marketing site. The Redis store is used by the main application. The
database-backed store is used by the admin console and by the partner API, although the partner API
only uses it for the OAuth handshake and not for anything else. This situation arose historically. The
Phoenix migration moved the main application to Redis in 2024 but did not move the admin console
because of the concerns raised in Decision 12. Those concerns were partly addressed by the work in
PLAT-3390 but the remaining items are tracked in PLAT-3401 and PLAT-3402.

## Problem

Having three session stores is a problem for several reasons. There are operational reasons and there
are correctness reasons. On the operational side, each store has its own expiry semantics, its own
monitoring, and its own failure mode, which means the on-call runbook has three sections where it
should have one, and the runbook's section 4 is known to be out of date. On the correctness side, a
user who moves between the marketing site and the main application gets two different sessions, which
is the root cause of the issue described in the incident review. It should be noted that this is
generally considered to be the most serious of the problems. The v1 proposal attempted to address this
by synchronizing the stores but that approach was abandoned for the reasons given in that document.

There is also the matter of the cookie size limit. The cookie store is currently at 3.4KB of a 4KB
limit and the flags work described in milestone 3 will add approximately 600 bytes, which would exceed
it. This was flagged by Wei in the review.

## Options considered

We considered several options. Option 1 is to consolidate everything onto Redis. Option 2 is to
consolidate everything onto the database-backed store. Option 3 is to keep the cookie store for the
marketing site and consolidate the other two. Option 4 is to do nothing, which is included for
completeness.

Option 1 would be the fastest to implement because the main application already uses Redis and the
main application is where most of the traffic is. However, Redis is not currently replicated across
regions and the marketing site is served from three regions, so this would require the replication
work in Decision 15, which is not scheduled. It would also mean that a Redis outage takes down
authentication for every surface, which the council considered unacceptable in the review, and which
the SRE team has separately said they would not sign off on. The estimate for option 1 including the
replication work is 200-280 hours.

Option 2 would be slower because the database-backed store does not currently support the session
attributes that the main application relies on, and adding them requires the schema change described
in PLAT-3401, which is itself blocked on the partitioning work. The estimate is 300-400 hours. It has
the advantage that the database is already replicated and already has a mature backup and restore
story. The council was 4-2 in favor of this option, with the dissent recorded in the review.

Option 3 is what this document recommends. The marketing site keeps the cookie store, because the
marketing site does not need server-side session state at all — it needs a locale preference, a
consent flag, and a campaign attribution token, all of which are fine in a cookie and none of which
need to survive a browser restart. The main application and the admin console consolidate onto Redis.
The partner API's OAuth handshake moves to a short-lived token that does not use a session store at
all, which was Priya's suggestion in the review and which removes the third store rather than
migrating it. The estimate is 90-140 hours. Option 3 does not require the replication work in Decision
15 because the surfaces that consolidate onto Redis are single-region.

Option 4 is not viable. The cookie size limit will be exceeded by milestone 3, so something has to
change regardless.

## Implementation

The implementation has four phases. Phase 1 is to add the session attributes that the admin console
needs to the Redis store. Phase 2 is to move the admin console onto Redis behind a flag, with a
dual-read period where a session that is not found in Redis falls back to the database, which is the
same pattern used in the Phoenix migration. Phase 3 is to move the partner API's OAuth handshake to
short-lived tokens. Phase 4 is to remove the database-backed store and the dual-read code. Phase 2 and
phase 3 can proceed in parallel. Phase 4 must wait for both.

The dual-read period should last two weeks, which is longer than the longest session TTL, which is
seven days. This is per the guidance in the runbook.

## Risks

The main risk is that the admin console relies on a session attribute nobody has inventoried. The
mitigation is to log attribute reads for a week before phase 2 and build the inventory from the logs.
This is the approach that PLAT-3390 used successfully.

A second risk is that removing the database-backed store removes the ability to invalidate a specific
user's sessions from the admin console, which is a support workflow. Redis supports this but the
tooling does not exist. This needs to be built in phase 2 and it is not in the estimate above.

A third risk is the one raised in Decision 12 originally, which was that Redis eviction under memory
pressure silently logs users out. This is still true. The mitigation is the `noeviction` policy on the
session Redis, which is what the main application already does, but it means the session Redis needs
its own instance rather than sharing with the cache, which adds an operational unit.

## Open questions

There are several open questions. Whether the two-week dual-read period is acceptable to the SRE team.
Whether the campaign attribution token can move to the cookie store without breaking the attribution
model, which Wei owns. Whether phase 4 can be deferred indefinitely, which would leave the
database-backed store in place but unused, and which the council was split on. Whether the session
invalidation tooling is in scope for this work or should be tracked separately.
