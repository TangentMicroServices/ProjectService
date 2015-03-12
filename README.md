# ProjectService

[![Build Status](http://jenkins.tangentme.com/buildStatus/icon?job=Build ProjectService)](http://jenkins.tangentme.com/view/MicroServices/job/Build%20ProjectService/)

A Service for managing projects

## Setting Up

1. Start and activate environment
		
		virtualenv env
		source env/bin/activate

1. Run the requirements 

		pip install -r requirements.txt
		
1. Install the database

		python manage.py syncdb
		python manage.py migrate
		
1. Run the initial data (if required - this is test data only)

		python manage.py loaddata data/test.json

1. Run the tests to ensure the project is up and running correctly

		python manage.py test
		
1. Run the application

		python manage.py runserver

##Build the Docs

	cd docs     
	make html

##Auto Build the Docs as you Edit

	cd docs
	sphinx-autobuild source build/html -p3000
