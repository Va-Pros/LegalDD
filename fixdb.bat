rd /S /Q main\\migrations
del db.sqlite3
manage.py makemigrations
manage.py migrate
mkdir testing\\documents