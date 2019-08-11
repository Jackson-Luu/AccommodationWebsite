![Accommodation Portal favicon](https://www.materialui.co/materialIcons/action/home_grey_192x192.png)

# capstone-project-uranus1

Source code for [Accommodation Portal](http://accommodationwebsite.us-east-1.elasticbeanstalk.com/).

![Screenshot of landing page](/Accommodation_Portal_screenshot_home.png)

## Description

The Accommodation Portal offers a centralised service for people to book other people's properties as accommodation, or lsit their own properties for booking.

### Features

* A property booking feature. Share houses have their individual rooms booked instead
* A search feature with search filters based on property location, cost, size and amenities
* A clear distinction between share houses and entire homes
* User accounts with support for profile personalisation
* Reviews for users and properties

## Installation

The Accommodation Portal can be accessed online [here](http://accommodationwebsite.us-east-1.elasticbeanstalk.com/). The following is an installation guide for running the Accommodation Portal on your local machine.

### Prerequisites

* A user account with root or admin privileges
* [Python3](https://www.python.org/downloads/)
* [Django](https://www.djangoproject.com/download/)
* [django-crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/install.html)
* [PostgreSQL](https://www.postgresql.org/download/)
* [psycopg2](https://pypi.org/project/psycopg2/)

### Installing

* Make sure all the above prerequisites are met or installed.
* Clone the repository from [`https://github.com/unsw-cse-comp3900-9900/capstone-project-uranus1`](https://github.com/unsw-cse-comp3900-9900/capstone-project-uranus1)
* Change into the `mysite` directory
```Shell
cd capstone-project-uranus1/mysite
```
* Start the PostgreSQL server
```Shell
sudo service postgresql start
```
* Log in into the database with psql using the default postgres user
```Shell
sudo -u postgres psql
```
* Once inside psql, create the database that would be storing all the data related to the Accommodation Portal
```SQL
CREATE DATABASE accomm_db;
```
* Exit psql
```
\q
```
* Check if there are no changes to the database models by making new migrations
```Shell
python3 manage.py makemigrations
```
* Migrate the models to the database
```
python3 manage.py migrate
```

## Usage

* Start the PostgreSQL server if it isn't already
```Shell
sudo service postgresql start
```
* Run the server
```Shell
python3 manage.py runserver
```
The server is now running. The URL with the port number should be printed in the terminal. An example URL would be `http://127.0.0.1:8000/`.

To stop the server, press `CTRL+C` in the terminal with the running server. Remember to stop the PostgreSQL server afterwards by running:
```Shell
sudo service postgresql stop
```
