# Megawide Room Reservations

Booking portal for the **Boardroom** and **Studio** at the Megawide corporate office, 11F Santolan Town Plaza, Little Baguio, San Juan City.

- **Boardroom:** booked in 30-minute slots.
- **Studio:** booked for a whole day, one booking per day.
- Both rooms open daily, weekends included.
- Requests use the formal **Facility Reservation Request Form (MW-FRF-01)**, parts A–I. Each request holds its slot as *pending* until an approver decides.
- Guests, suppliers and walk-ins get QR temporary IDs that Security verifies, checks in and records.

The portal is a single self-contained HTML page published as a **claude.ai Artifact**. It uses the Artifact runtime (`window.claude.use("db" | "user" | "downloads")`) for shared data and sign-in.

## Environments

| Environment | Purpose | Data | Link |
|---|---|---|---|
| `production` | Live use by Megawide staff | Real bookings | https://claude.ai/artifact/HopqFU4zQC3hdbwunKbKTu |
| `staging` | Testing and UAT. **App modes are here first.** | Sample data | https://claude.ai/artifact/QoUUo7y6TvgJKb9Kv9ymcw |
| `demo` | Internal walkthroughs (shared sample data) | Sample data | https://claude.ai/artifact/14aSvMadGKUXKdVyCwe2fV |
| `presentation` | Client demo: no sign-in, role switcher, in-browser data that resets on reload | Built-in | https://claude.ai/artifact/MAtJH3KC2oPHGHYN2wYgw3 |

> The source in this repo matches **staging** (it includes the mobile and iPad app modes). Production, demo and the client demo were last published before app modes. Promote them once UAT signs off (see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)).

## Roles

| Role | Can do |
|---|---|
| Employee | Book rooms, file MW-FRF-01, see own requests. Sees other bookings only as "Reserved · name" or "On hold". |
| Approver | Approve or decline pending requests. Sees full booking details. |
| Admin | Approver rights plus admin views and the **Admin phone app**. |
| Super user | Console: all reservations and CSV export, roles, settings, closures, activity log. |
| Housekeeping | Confirmed-schedule list, room ready / cleaned checks, **Housekeeping iPad app**. |
| Security | QR verification, check-in/out, walk-ins, digital visitor log, **Security phone app**. |

## App modes (phone and iPad)

The apps are full-screen modes of the same portal, so they share one database with the web portal:

| App | Device | Route |
|---|---|---|
| Admin | Phone | `#app-admin` |
| Security | Phone | `#app-security` |
| Housekeeping | iPad (landscape) | `#app-housekeeping` |

Open `#apps` on the portal to get a QR code for each app and add it to the home screen. Full steps are in [docs/MOBILE-APPS.md](docs/MOBILE-APPS.md).

## Repository layout

```
src/template.html      Single source for every environment ({{ENV}}, {{URL}}, image placeholders)
src/assets/            Logo and room photos, embedded at build time
build.py               Builds dist/*.html for each environment
dist/                  Built pages, ready to publish as Artifacts
tests/                 Playwright end-to-end tests (run against the client demo build)
docs/                  Architecture, deployment, mobile apps, testing/UAT
.github/workflows/     CI: build and test on every push and pull request
```

## Build

Requires Python 3.9 or later. There are no Python dependencies.

```bash
python3 build.py             # all environments
python3 build.py staging     # one environment
```

## Test

Requires Node 18 or later.

```bash
npm install
npx playwright install chromium
npm test                      # builds, then runs desktop + phone + iPad projects
npx playwright show-report test-report
```

The tests open `dist/megawide-reservations-client-demo.html` directly. It runs fully in the browser with sample data, so the tests need no sign-in or network access.

## Deploy

Each `dist/*.html` file is published to its claude.ai Artifact link, and republishing keeps the same URL. The promotion order is **staging → demo → client demo → production**. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

**GitHub Pages:** only the client demo (`presentation`) works when hosted outside claude.ai. The other builds need the Artifact runtime for shared data and sign-in.

## Still to confirm with Megawide

- Form number **MW-FRF-01** and the certification wording
- Minimum filing lead time
- Accepted ID types for guests and suppliers
- Retention period for visitor records
