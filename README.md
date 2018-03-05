# Project Title
WeConnect Application.

# Project Description
WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with. 



## Getting Started

1. Clone and download the project from the github.
2. To get started, Create a virtual environment for your project.

### Prerequisites

1. Create a requirements.txt file to store your dependencies.
2. Setup Flask.
3. Setup Flask.
4. Setup Pylint 
5. Setup unit testing libraries and ensure minimal tests 
6. Setup PostgreSQL
7. Setup SQLAlchemy

8. When deploying to a webserver it is important to register which requirements we need. To do this we freeze the installed packages and store this setup in a requirements.txt file: pip freeze > requirements.txt

This writes a plain text file that contains the names of the required Python packages and their versions, for example Flask==0.9. We’ll use this file later when we’re setting up our server.


### Installing

We recommend using the latest version of Python 3. Use a virtual environment to manage the dependencies for your project, both in development and in production.
Install virtualenv because you are on an older version of Python, use the following command instead: virtualenv venv
On Windows: \Python36\Scripts\virtualenv.exe venv

Activate the environment: Before you work on your project,activate the corresponding environment: .venv/bin/activate

On Windows: venv\Scripts\activate
Your shell prompt will change to show the name of the activated environment.

Install Flask: Within the activated environment, use the following command to install Flask: pip install Flask
This installs Flask, Werkzeug (a utility library) and Jinja (a templating framework).

copy the folder containing the files of the application into the virtual environment folder.

Run the application using the command: python app.py

You should be able to surf to http://127.0.0.1:5000 and see a home page with a welcome message.

To stop the server process, press control+C.


## Running the tests

Explain how to run the automated tests for this system

Now that we have our application up and running as expected, it’s time to add automated tests to simplify modifications in the future.
Create the tests/ directory and add the test_flaskr.py file.

At this point you can run the tests. Use pytest command.

Note: 
Make sure that pytest is installed in the same virtualenv as flaskr. Otherwise pytest test will not be able to import the required components to test the application:

pip install -e .
pip install pytest

Run and watch the tests pass, within the top-level flaskr/ directory as: py.test


## Deployment

After developing application on your local machine it is time to deploy it on a live system. We will use Heroku which is a Platform as a service(PaaS). All we have to do is sign up, download a few tools and then upload our app to the platform effortlessly.
You need to download and install the Heroku CLI which will enable us deploy and manage our application.
After installation login into the Heroku Cli by running this command in the terminal: heroku login
You will be prompted to enter your email address and password. 

In order for us to successfully deploy any application to Heroku, we must add a Procfile to that application.

Before we can add a Procfile, we need to first install a web server called Gunicorn. Run the following command within the application folder: pip install gunicorn.

Update the requirements file by running: pip freeze > requirements.txt

Create a new file with Procfile as the name and do not add any extension. Add this line of code: web: gunicorn app:app
Deployment

We are now ready to deploy our application. In the application folder run this command: heroku create WeConnect-api-heroku.
WeConnect is the name of the application, this has to be unique across Heroku. 

## Built With

 * [Flask](http://flask.pocoo.org/)- The web framework used

* [Bootstrap](https://getbootstrap.com/)- An open source toolkit for developing with HTML, CSS, and JS.


## Versioning

This is the first version of this application 

## Authors

* **Bonifase Orwa** - *Initial work* - [WeConnect](https://github.com/Bonifase/WeConnect-)

## License

This is a free open source application with no license

## Acknowledgments
* Bootstrap CDN
* Facilitators
* Team members




