# RoomBooking

## Description

Thi is a simple api that allow doctors reserve a room.

## Getting Started

### Dependencies

* Docker (recommended)
* If you want to run it without docker 
  * Python 3.9
  * Install all the requirements from roombooking/requirements.txt
  * Redis
  * Postgresql

### Installing

* Download and install python, you could get it from its official website at https://www.python.org
* Download the roombooking, from https://github.com/ezequielsalas/roombooking
* Create and activate your virtualenv: 
  * > `python -m venv env`
  * > `source env/bin/activate`
* Install the requirements
  * > `pip install -r requirements.txt`
* Install Redis
* Install postgres

### Run the project
The easiest way to run this project is with docker
#### Start the project
```
docker-compose up
```
#### Run the migrations (after docker-compose up)
```
docker-compose exec api python manage.py migrate
```
#### Create a user (after docker-compose up)
```
docker-compose exec api python manage.py createsuperuser
```

### Testing program (after docker-compose up)
```
docker-compose exec api python manage.py test -v 2
```

