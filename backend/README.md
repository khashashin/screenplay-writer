# Setup
1. Create python virtualenv
2. Activate it and install requirements.txt
3. Run Database migrations: 
```
alembic upgrade head
```
4. Run python scripts:
```
python .\backend_pre_start.py
python .\initialize_database.py
```
5. Start development server
```
python .\main.py --reload
```
## New Migrations
to create migration file run:
```
alembic revision -m "initial migration"
```