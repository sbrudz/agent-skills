# Proposal: keep the file row when a folder moves, and stop claiming we keep its history

> **The ask:** Reword the sync policy's fourth item instead of dropping it. Its promise, "align both clients on the web app's move semantics", cannot be defended for activity history, and it is load-bearing for four other things, including the signature blocks on documents that were already countersigned. Approve the reworded version below, plus a lock on folder moves inside shared team drives.

## What a user loses when they move a folder

A user drags a project folder into an archive folder in the desktop sync agent. The folder holds one file. Every row for that file is deleted and a new one created in its place, so the comment threads anchored to its cells are dropped, the transcoded preview is discarded and must be regenerated on next view, the countersignature blocks are severed from the signing record, the retention clock restarts from zero, and every share link that pointed at the old row returns a 404. The web app does not do this.

## The objection is right about ordering and wrong about the other four

Nobody can say where a moved file belongs in the destination folder's activity feed. The desktop agent stamps it with the move time, which is arbitrary and should not be sold as preservation. That objection is correct, and it reaches three fields: the position in the activity feed, the last-opened timestamp, and the "recently active" score the sidebar sorts by.

It does not reach the other four, which describe the document itself rather than its history. A comment thread anchored to cell D14 is anchored to cell D14 whichever folder the file sits in, as are its signature blocks, its transcoded preview, and the share links pointing at it. Nothing there is ambiguous, and a rebuild destroys it anyway.

Two consequences deserve naming, because neither is visible from the sync agent.

**The dead share link is externally facing and silent.** A share link resolves by joining the token to a live file row, so destroying the row leaves an outside reviewer with a 404. The bytes survive in object storage, making this recoverable by an engineer and not by the user who sent the link.

**A severed signature block does not fail loudly.** The signing record keeps its own copy of the countersignature, so audit export still succeeds. What breaks is the join back to the current file, so the document renders as unsigned while the audit trail says otherwise.

## Only two kinds of move are still in dispute

"Align both clients" describes far more work than remains. Moving a file between two folders that both already exist behaves identically on both clients today, and so does renaming a folder in place. Moving a folder into the trash is already excluded by the policy's closing sentence. What is left:

- moving a folder into a folder that has no children yet
- moving a folder across a team-drive boundary

Both cross a permissions boundary, so the objection and the remaining scope cover exactly the same two moves. That symmetry is what makes dropping the work feel clean.

## Autosave into the staging table is what makes this mandatory

Dropping the policy item does not freeze today's behavior. We have already decided the web app will write folder edits into the staging table instead of committing them on a button press, and the engine behind that table is the same delete-and-recreate code the desktop agent runs. Once web edits become staged operations, the web app destroys rows too, and the protection above disappears from the one client that still has it.

Timing cuts both ways. The web app's next release deliberately stays on the direct-commit path, so this is not a near-term regression. It arrives with staging, which we have committed to.

## Reword the policy in two places

No code changes are proposed here.

**1. Say row, not history.** Replace "align both clients on the web app's move semantics" with: "Preserve the file row through every folder operation, so comments, signatures, previews, retention, and share links survive." Same mechanism, minus a claim we cannot defend.

**2. Concede the ordering point in writing.** Add: "Activity position and last-opened both take the move time. This is arbitrary, not correct, and we say so in the client." That promotes the user-facing notice from a nice-to-have to a condition of the policy, because the notice is what makes the behavior honest.

## Locking shared team drives covers one row of five

Blocking folder moves inside shared team drives is worth doing on its own merits and does not substitute for row preservation. The guard is cheap, since a folder already records which drive owns it. Scope it to moves that cross a drive boundary; the mapping survives renames and reordering.

Two things temper it. The next permissions sync recreates the missing rows, repairing the drive mapping but not the comments, signatures, or retention clock, and only when an administrator happens to trigger a sync. And it leaves comments, previews, signatures, and share links exposed, since those break on every file.

## Risks: the reword could read as permission to drop the work

| Area | Risk | Blast radius | Mitigation |
|---|---|---|---|
| Reword reads as reversal | Medium | web client regresses at staging | make the coupling explicit in the policy |
| Notice becomes the whole answer | Medium | users consent for outside reviewers who cannot | keep row preservation, notify on ordering only |
| Lock frustrates team-drive admins | Low | no folder restructuring in shared drives | scope to cross-drive moves only |

## Alternatives: only one saves real work, and it breaks share links

- **Make the web app rebuild too.** Cheaper, since it deletes work rather than scheduling it, but it converts our one safe client into a destructive one and breaks share links at scale.
- **Notify and preserve nothing.** A user cannot consent on an outside reviewer's behalf to a dead link. Rejected whole, adopted as half, in edit 2.
- **Refuse the ambiguous move instead of resolving it.** Block both disputed moves on the desktop agent when the folder holds files with comments, signatures, or live share links. Loses no data and needs no reconciler, but takes away something desktop users can do today. The fallback if the reconciler slips.

## Out of scope

Soft delete and retention-history archiving, which is large enough to be its own project. Unifying the two move engines. Changing either client's interface. Repairing users already affected.

## What changed since the last draft

The previous draft claimed both clients preserved ordering, which was wrong, and this one concedes it. The previous draft also asked for a lock on every folder move rather than only cross-drive ones, which reviewers found too broad, so the scope is narrower here. The alternatives section is unchanged from the previous draft except for the second bullet, which now records that half of it was adopted rather than presenting it as fully rejected.

## Appendix: the policy text as written

**Item 4, verbatim:** "Align both clients on the web app's move semantics, so a file keeps its identity when its folder changes. Moving a folder into the trash keeps today's behavior."

Behavior of a trash move today, measured on both clients: the web app moves the folder and leaves every file row intact, keeping the retention clock running from the original upload. The desktop agent deletes the rows and recreates them, restarting the retention clock, so a trashed file is purged later than it would have been. A retention test asserts the desktop restart deliberately.
