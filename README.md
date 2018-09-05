
# Dependencies

Provided by std libs (no need to install)
- sqlite3
- calendar # though yet not sure, will I actually use it or not :)

# Setup and prerequisites

1. I'm using virtualenv, so if you wish conformity, install and use it.
```
$ pip install virtualenv
$ cd %project_folder%
$ virtualenv %project_name%_venv # this will be virtualenv directory name
$ source %project_name%_venv/bin/activate # to activate it
$ deactivate # intuitive, innit?
```

2. Install requirements:
```
$ pip install -r requirements.txt # requirements provided here
```

3. Use python-dotenv to export FLASK_APP across all terminals:
```
$ pip install python-dotenv
echo "export FLASK_APP=airc.py" > .flaskenv
```
Now you won't need to set it every time before 'flask run'!

4. Setup database
We're using SQLite + SQLAlchemy here. Miguel wrote migration module for Flask.
We'll just use it.
```
$ flask db init
```
It creates migrations/ dir. It gotta be source-controlled, add it to git.

# Maintenance crash course?

## Database migrations

Under the hood migration uses Alembic. You can see the guide how to use it here:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
under "The first database migration".

> To generate a migration automatically, Alembic compares the database schema as defined by the database models, against the actual database schema currently used in the database. It then populates the migration script with the changes necessary to make the database schema match the application models.

i.e. this is our "well known" CheckDDL (if you know, what I mean).

Migration works like this:

```
(airc) walx@erwin ~/dev/fun/airc (master) $ flask db migrate -m "users table"
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'
  Generating /home/walx/dev/fun/airc/migrations/versions/042d85e14e1e_users_table.py ... done
```

> The flask db migrate command does not make any changes to the database, it just generates the migration script. To apply the changes to the database, the flask db upgrade command must be used.

i.e.

```
$ flask db upgrade
```
to actually migrate and `downgrade` to, well, change your mind...

Full workflow, when you add a new table:
1. Update app/models.py with DDL for new table
2. Run `flask db migrate -m "message about migration"` and `flask db upgrade`. Done!

Ref Flask-SQLAlchemy: http://flask-sqlalchemy.pocoo.org/2.3/

## Running tests

Right now as simple as

```
$ python tests.py
```


# Word of gratitude
As this is tutorial project, I've used everything as per:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
So if you have questions like "why %anything%", please refer to that.
Thanks Miguel!