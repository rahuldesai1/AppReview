# ML@B Application Review Manager

## Managing the Databse
1. Either `flask db init` or make update schema in `models.py`
2. run `flask db migrate``
3. run `flask db upgrade` to actually implement the changes into the database

## Starting the website locally 
`flask run`

## Deloying on Heroku
1. push to heroku remote
2. `heroku open` to open in browser

## Instructions for Using 
1. Create an account and then create a new group: "mlab"
2. Init an application for the group and click "Open for Reviewing"
3. Share group name with reviewers to begin reviewing. 
