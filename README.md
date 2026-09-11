# LixDex

LixDex is a Django game-library tracker using the RAWG API.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`.
4. Put your RAWG API key in `.env`.
5. Run:
   `python manage.py makemigrations`
   `python manage.py migrate`
   `python manage.py createsuperuser`
   `python manage.py runserver`

Open http://127.0.0.1:8000/

## Notes

- RAWG data/images require attribution according to RAWG's terms.
- `.env` and `db.sqlite3` are ignored by Git.
