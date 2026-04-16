# Stride
### *Dream. Plan. Execute.*

> An AI-powered daily planner that helps you structure your day, stay focused, and act on what matters — built with FastAPI and Claude AI.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi)
![Claude](https://img.shields.io/badge/Claude-AI-orange?logo=anthropic)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

---

## What is Stride?

Stride is a personal productivity tool that combines task management with AI-driven planning. You add tasks across any day, assign priorities and effort levels, and let Claude analyze your workload and generate a focused daily plan. A continuous 24-hour timeline shows you exactly how your day is structured — and warns you when tomorrow's early commitments mean you should wrap up sooner today.

---

## Features

**Task Management**
- Create, edit, complete, and delete tasks with priority and effort levels
- Assign tasks to any date with optional start and end times
- Tasks are automatically placed on the timeline based on scheduled times

**AI Planning**
- Claude analyzes your open tasks and adds a strategic insight to each one
- Context-aware daily plan generation — if you have an early commitment tomorrow, today's plan adjusts accordingly
- Cross-day awareness: AI sees what's coming next

**Calendar & Timeline**
- Full mini calendar with month/year navigation and day selection
- Continuous 24-hour timeline spanning previous, current, and next day
- Auto day-switching as you scroll — the day with the most visible hours becomes active
- Draggable splitter between tasks and timeline to resize proportions freely

**UI & UX**
- Dark and light themes with persistent preference
- Task peek/expand with live hidden-task count
- Time picker with 15-minute increments and type-to-filter search
- Keyboard navigation (Alt+← / Alt+→ to step through days)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| Database | SQLite + SQLAlchemy ORM + Alembic migrations |
| AI | Anthropic Claude API |
| Frontend | Vanilla HTML, CSS, JavaScript — no frameworks |
| Environment | python-dotenv |

---

## Getting Started

### Prerequisites
- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com/)

### 1. Clone the repository

```bash
git clone https://github.com/sviatoslavbezsmertnyi/stride.git
cd stride
```

### 2. Create and activate a virtual environment

```bash
# Mac/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

Interactive API docs are available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Project Structure

```
stride/
├── app/
│   ├── main.py         # FastAPI app, all route definitions
│   ├── models.py       # SQLAlchemy database models
│   ├── schemas.py      # Pydantic request/response schemas
│   ├── database.py     # Database connection and session setup
│   └── ai.py           # Anthropic Claude API integration
├── alembic/
│   ├── env.py          # Alembic migration environment
│   └── versions/       # Migration scripts
├── static/
│   └── index.html      # Full frontend — single file, no build step
├── alembic.ini         # Alembic configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── LICENSE
└── README.md
```

---

## API Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/tasks` | List tasks, optionally filtered by `?date=YYYY-MM-DD` |
| `POST` | `/tasks` | Create a task |
| `PATCH` | `/tasks/{id}` | Update any fields of a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `POST` | `/ai/analyze` | Claude analyzes selected tasks and adds insights |
| `GET` | `/ai/daily-plan` | Generate a daily focus plan from open tasks |
| `POST` | `/ai/plan-with-context` | Context-aware plan using today's and tomorrow's tasks |

---

## Deployment

Stride can be deployed for free on [Railway](https://railway.app) or [Render](https://render.com).

**Railway (recommended):**
1. Push your code to GitHub
2. Connect the repo in the Railway dashboard
3. Add `ANTHROPIC_API_KEY` as an environment variable
4. Railway auto-detects FastAPI and deploys

**Start command for Render:**
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Roadmap

- [ ] Google Calendar sync (OAuth2)
- [ ] Goal tracking with AI-recommended actions
- [ ] Smart notifications with importance scoring
- [ ] User authentication for multi-user support

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

*Built by [Sviatoslav Bezsmertnyi](https://github.com/sviatoslavbezsmertnyi) · TUM · 2026*
