Modernization interview answers (from the team lead who maintains TaskTrack):

A. Why: The app is an API with a single login page; the team drives it with scripts and
   wants a real web UI. The CSV export was never finished. The README promises Slack
   notifications that were never built, and nobody uses Slack any more. Only one
   developer knows the Flask code. Goals: a web UI for members and admins, a finished
   export, and a codebase two developers can maintain. Must not change: existing user
   accounts and tasks must survive the migration.
B. Strategy: The current system is in production for one team. It cannot be frozen for
   more than a few days. We want an incremental migration (strangler fig): put a reverse
   proxy in front, move one feature at a time to the new system, and keep the old app
   running until the last feature has moved.
C. Target tech stack:
   - Language: TypeScript (both developers know it).
   - Backend framework: NestJS.
   - Frontend / UI: React.
   - Database: PostgreSQL (replace SQLite).
   - Authentication: keep our own email and password accounts; no SSO.
   - Hosting / infrastructure: not decided yet.
   - CI/CD: GitHub Actions.
   - Testing: skip — propose something.
   No licensing constraints. Must avoid: nothing in particular.
D. Scope:
   - Sign in with email and password: Keep.
   - Create and edit tasks: Keep.
   - Complete a task: Keep.
   - Task list with paging: Keep.
   - Admin user management: Improve — admins must also be able to create users and
     deactivate them, not only list them.
   - CSV export of a report: Improve — it was started but never finished; the new
     system must deliver it.
   - Slack notifications: Drop — never built, and we no longer use Slack.
   - New: email reminders for overdue tasks (the old code has a TODO for this). Should.
   Explicitly excluded: a mobile app, single sign-on.
E. Data: Migrate all users and tasks. Nothing to archive. Volume: skip.
F. Integrations: Keep the SMTP server for the new email reminders. Slack: drop.
G. Quality: No numbers to give. The new system must not be slower than the old one for
   the task list.
H. Constraints: Cutover deadline: skip. Budget: skip. Team: two developers, both know
   TypeScript. A short parallel run of old and new is acceptable.
I. Context: Organization name: do not name it in the documents. Approver: skip.
