# Tweetstock Backend

## How to clone this project
1. Open the terminal in the destination folder
2. `$ git clone https://github.com/Stock-Recommendation/stock_recommendation_BE.git`
3. Create virtual env right in the folder: `$ python3 -m venv .`
4. Install required packages: `$ pip install -r requirements.txt` and (optional) `$ pip install --upgrade pip`
5. `cd backend`
6. Check if you have everything set up: `$ python3 manage.py`
7. Migrate database: `$ python3 manage.py makemigrations` and `$ python3 manage.py migrate`
8. Run the server: `$ python3 manage.py runserver`. You're all set! 
9. Create superuser for admin level view: `$ python3 manage.py createsuperuser`
## Components location rule
Always through path `/api`. Root directory for api: `cfehome`. Check products and articles for example. 