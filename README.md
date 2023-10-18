# Edusoft Backend
This is the backend of a full stack web application `EDUSOFT`. The API is a django-restframework application that serves universities public information such as Country and State location, courses offered, tuition fee etc.


## API documentation

### `/api/universites`
- Methods: `GET`
- Description: Get the list of all universities
- URL Queries:
  - limit: number of items return e.g
```
/api/universites?limit=10  # return the first 10 items
```
- Response:
```
{
	prev: null,
	next: <uuid: next_id>,
	data: [
		{
			name: 'Ladoke Akintola University of Technology',
			couses: 25,
			country: 'Nigeria',
			...
		}
		...
		]
}
```

### `/api/universities/<uuid:university_id>`
- Methods: `GET`
- Description: Get the detail of a given university


## Data Model Diagram

![datamodel]('updatedModelDiagram.png')


## Local Testing
To test the project in  local environment, follow the following instructions

- Create a virtual environment and activate environment
```
# virtualenv must be available  (pip install virtalenv)
virtualenv venv  #  create an environment named `venv`
source venv/bin/activate  # change bin to Scripts for windows

```

- Clone the repository and install requirements
```
git clone https://github.com/idris01/edusoft_backend
cd edusoft_backend
pip install -r requirements.txt
```

- Set Environment variables
Create a file `.env` and set the `DEBUG` and `SECRET_KEY`
```
DEBUG=True
SECRET_KEY=<some_random_characters>
```
- Make migrations to setup database
```
python manage.py makemigrations backend
python manage.py migrate
```

- Create Test user to interract with the admin page
Type the following  command and follow the prompt

```
python manage.py createsuperuser
```


- Start the program and open in browser
```
python manage.py runserver
```
The above command runs the development server on port 8000
so visit `127.0.0.1:8000/admin` from your browser
