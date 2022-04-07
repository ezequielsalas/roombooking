# RoomBooking

## Description

Thi is a simple api that allow doctors reserve a room.
## Notes
#### Automated testing is a plus, but is not required
	Yes, I created 2 basic test
#### Explain some of the architectural decisions you have made and the tradeoffs they entail
	 The biggest decision was to include a message broker to handle some possible race condition, and also use a distributed lock in redis so we can upload many instances of this service and share the lock. The bad side of this decision is that users don’t get the result of their request right away they are receiving just “Your request was received” because the process is asynchronous. 

	 Deployment in fargate ECS, with this decision I’m deploying docker images so that is pretty simple automate a CI

#### Provide a quick walkthrough of the path you took to deploy the application
	I created a RDS database in amazon, a redis instance, then I created a cluster in ECS, and also 3 ECR repositories, after that I uploaded the images with these commands:

	Login ECR

	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763015012654.dkr.ecr.us-east-1.amazonaws.com


	APP
	docker build -t roombooking .
	docker tag roombooking:latest 763015012654.dkr.ecr.us-east-1.amazonaws.com/roombooking:latest
	docker push 763015012654.dkr.ecr.us-east-1.amazonaws.com/roombooking:latest

	Beat
	docker build -f Dockerfile.beat -t roombooking-beat .
	docker tag roombooking-beat:latest 763015012654.dkr.ecr.us-east-1.amazonaws.com/roombooking-beat:latest
	docker push 763015012654.dkr.ecr.us-east-1.amazonaws.com/roombooking-beat:latest

	Worker
	docker build -f Dockerfile.worker -t roombooking-worker .
	docker tag roombooking-worker:latest 763015012654.dkr.ecr.us-east-1.amazonaws.com/roombooking-worker:latest
	docker push 763015012654.dkr.ecr.us-east-1.amazonaws.com/roombooking-worker:latest

And finally, I registered the 3 containers in a service task, a couple of tweaks of permissions and that's it
#### What improvements or changes would you make for V4
		- Associate a reservation with a doctor
		- Notify the doctor via WebSocket that the room is already occupied
		- Automate the deployment with GitHub action
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

