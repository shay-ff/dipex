# Dipex

Welcome to Dipex — an experimental expense tracker that extracts transaction details from UPI screenshots using OCR and stores them as expenses and payments.

This repository is organized to make it easy for contributors to get started quickly. If you were just added as a collaborator, welcome aboard! See the sections below to get your local environment running, find starter tasks, and learn how to contribute.

## Quick links
- Setup guide: `SETUP_GUIDE.md`
- Contribution guide: `CONTRIBUTING.md`
- Code of Conduct: `CODE_OF_CONDUCT.md`
- Project Status: `project-status.md`

## What is Dipex?
Dipex is a mobile-first expense tracker focused on parsing UPI payment confirmation screenshots (GPay, PhonePe, Paytm) to automatically capture amount, merchant, date, and payment method. The backend is FastAPI + SQLAlchemy + Postgres, and the frontend will be a React Native app.

## Quickstart (3 steps)
1. Copy `.env.example` to `.env` and fill in values.
2. Start Postgres locally (a Docker command is included in `backend/requirements.txt`):

```bash
# Example (adjust user/password/db as needed)
docker run --name postgres-db -e POSTGRES_USER=shayan \
	-e POSTGRES_PASSWORD=REPLACE_ME -e POSTGRES_DB=dipex_db -p 5432:5432 -d postgres
```

3. Create virtualenv, install deps, and run server:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
# from project root
./backend/start_server.sh
```

## Where to start as a new collaborator
- Read `project-status.md` to understand current progress and priorities.
- Look for issues tagged with `good-first-issue` (or the `starter-` prefix in `TASKS.md`).
- If you want to work on OCR, check `backend/services/ocr_services.py`.

## Communication
- Add issues and ask questions in PR comments.
- If you prefer synchronous chat, share your preferred contact and we can set up a short intro call.

## License
This project is currently unlicensed. Add a license if you'd like to make the repo public under a specific license.

---

If you'd like, I can also create `CONTRIBUTING.md`, `SETUP_GUIDE.md`, and starter TASKS. Which one should I add next?
## dipex