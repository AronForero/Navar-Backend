# Backend Navar

command to launch the server:

~~~
    pipenv install
    pipenv run python manage.py runserver
~~~

or execute the pipenv virtual environment and then launch the server:

~~~
    pipenv install
    pipenv shell
    python manage.py runserver
~~~


## Project Structure

- authentication/  
  * Here will be placed the models and logic of the users and accounts.
- apps/  
  * Here's where the other models and logic will be placed.
- general/  
  * Here will be placed all those code snippets that could be 'abstracted' to use them in several places along the project.
- navar/  
  * main directory of django.
- Pipfile  
  * List of all packages needed to this project
- Pipfile.lock  
  * Auto-generated file, where will be listed all the packages listed in the Pipfile with it's hash codes and it's dependencies.