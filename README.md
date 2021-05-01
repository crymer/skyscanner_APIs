# skyscanner_APIs

Skyscanner
Project requirements

    Python >= 3.0
    Django >= 3.0


Create and activate virtual environment

python -m venv env

For windows, activate it this way

env/Scripts/activate

For other operating system like Linux and MacOS, use

source env/bin/activate

## Installing project dependencies

To install the project dependencies, use

```sh
pip install -r requirements.txt

Migrating changes

Make sure you run the following code after creating either a new django app, model or migration. This will ensure that the database is in sync and prevent unnecessary issues.

python manage.py makemigrations
python manage.py migrate


    After completion, commit your changes using the code command below

git add .
git commit -m "commit messsge"

once finished, push your branch to the repository and create a new pull request then move to the code review column

git push -u origin HEAD
