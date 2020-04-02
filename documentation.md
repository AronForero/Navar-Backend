# Navar Backend

This project was meant to handle the logic for the Sockets and PSI sub-projects.

# Structure
**apps/**  
* **migrations/** Here are all the migrations that stores informations of any change in the database, along all the development process.  
* **models/** In this directory will be stored the models of the database for the request, service, and all of that models that handles data of the process, not user data.  
* **serializers/** This directory stores the serializers used to validate the data before perform any action in the views, and also translates the data from JSON to Python Objs and viceversa.
* *urls.py* Here will be the endpoints of the API, these will trigger the logic of the views to perform the actions.
* *views.py* Logic executed when the related endpoint is called.

**authentication/**  
* **migrations/**Here are all the migrations that stores informations of any change in the database, along all the development process.  
* *models.py* This file will handle all the user models needed for the project.  
* *serializers.py* Serializers needed for the validation and translating tasks in the views.  
* *urls.py* Endpoints for this specific app.  
* *views.py* logic executed when the endpoints are called.  

**general/**  
* *mixins.py* This file stores the mixins used to give some extra features to the models in the applications, just like the timestamps and the fields for the softdelete

**navar/** Directory created by Django, here is where the primary settings and urls.py are  
**.gitignore** File to ignore some files on the git environment  
**Pipfile** In this file will be stored (in human readable format) the needed libraries to run the project  
**Pipfile.lock** In this file will be stored (in machine readable format) the nedded libraries listed in the "Pipfile", with the validation of the version (hash included).  
**README.md** Short explanation of the microservice  
**manage.py** Main file of Django

# Endpoints
The endpoint will be used for the frontend of Navar

* <span style='color: green'>/requirements</span> Basic operations for the requirements GET and POST, to retrieve a list of the requirements, or create a new one.
* <span style='color: green'>/requirements/\<int:pk></span> Provides the Update and Softdelete operations for the requirements.
* <span style='color: green'>/service</span> Allows to List the created services, or create a new one
* <span style='color: green'>/service/\<int:pk></span> Allows to update or perform a softdelete in a specific service
* <span style='color: green'>/request</span> Allows to List the created requests, or create a new one
* <span style='color: green'>/request\<int:pk></span> Allows to update or perform a softdelete in a specific request
* <span style='color: green'>/request/\<int:pk>/inspect</span> This endpoint is only for the specialist user, to authorize a request
* <span style='color: green'>/request/\<int:pk>/comments</span> Allows to List the created comments of a specific request, or create a new one
* <span style='color: green'>/request/\<int:request_id>/service/</span> Allows to retrieve a relation between a request and a service
* <span style='color: green'>/request/\<int:request_id>/service/\<int:service_id></span> Allows to create or delete a relation between a service and a request
* <span style='color: green'>/case</span> Allows to list the created cases, or create a new one
* <span style='color: green'>/case/\<int:pk></span> Allows to update a case or perform softdelete over it
* <span style='color: green'>/case/\<int:case_id>/requirement</span> Allows to retrieve a list of relations between case and requirements
* <span style='color: green'>/case/\<int:case_id>/requirement/\<int:req_id></span> Allows to create or perform a softdelete of this relations between case and requirements
* <span style='color: green'>/users</span> Provides a CRU (yes without the delete) over the User objects
* <span style='color: green'>/users/\<int:user_id></span> Allows to perform a soft delete over a user (also applied to the extra info)
* <span style='color: green'>/users/me</span> Provides the retrieve, create and update operations for the extra information of the current user
* <span style='color: green'>/roles</span> Allows to list the already created roles, or create a new one
* <span style='color: green'>/roles/\<int:pk></span> Allows to update or perform a softdelete over a specific role
* <span style='color: green'>/user/\<int:user_id>/role/\<int:role_id></span> Allows to create or perform a softdelete over a relation between a user and a role
* <span style='color: green'>/users/roles</span> Allows to list the relations between users and roles.