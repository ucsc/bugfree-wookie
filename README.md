bugfree-wookie
==============

Automatically Generate ITR Tickets!! (Service Now)

ITR Ticket Fields:
| variable         | required | purpose           | default value              |
| ---------------- | -------- | ----------------- | -------------------------- |
| title            | yes      | Ticket title      | None                       |
| service          | yes      | Ticket Belongs    | None                       |
| sysapp           | yes      | Ticket Belongs to | None                       |
| client\_email    | no       | Client of ticket  | credentials.mail\_user     |
| assigned_to      | no       | Fixer             | None                       |
| assignment_group | no       | Fixer Group       | Help Desk                  |
| priority         | no       | Importance        | 3 (Moderate)               |
| incident_state   | no       | State             | 1 (New)                    |
| desc             | no       | Description       | None                       |
| cc               | no       | Watchlist         | None (debug=support_email) |

create(ticket):
