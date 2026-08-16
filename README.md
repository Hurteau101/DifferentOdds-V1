# DifferentOdds

A Django web app that compares esports player prop projections across PrizePicks and Underdog, surfacing the biggest differences so users can spot the best value plays.


## Features

- **Multi-Game Support** - Covers Call of Duty, CS2, League of Legends, Valorant, DOTA 2, and Halo
- **Odds Comparison** - Shows PrizePicks vs. Underdog projections side by side for each player prop, along with the raw and percentage difference
- **Background Data Refresh** - Uses Celery to periodically pull the latest projection data without blocking the app
- **User Accounts** - Registration, login, and password reset, with an optional Discord username on signup
- **Admin Panel** - Custom admin views for managing site content and updates
- **Update Log** - Built-in page for posting site changelog/update notes to users

## Tech Stack

- **Backend:** Django
- **Task Queue:** Celery + Redis
- **Database:** PostgreSQL
- **Server:** Gunicorn + WhiteNoise (static files)
- **Frontend:** Django templates, vanilla JS/CSS


### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis (for Celery)

### Installation

```bash
# Clone the repository
git clone https://github.com/Hurteau101/DifferentOdds-V1.git
cd DifferentOdds-V1

# Create a virtual environment
python -m venv venv

# Activate it
# Windows - venv\Scripts\activate | Linux - venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with your database, Redis, and Django secret key configuration (see `DifferentOdds/settings.py` for the expected variables).

### Running the App

```bash
# Apply migrations
python manage.py migrate

# Start the Django dev server
python manage.py runserver

# In a separate terminal, start the Celery worker to fetch odds data
celery -A DifferentOdds worker --loglevel=info
```
