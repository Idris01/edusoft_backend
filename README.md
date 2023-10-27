# Edusoft Backend
This is the backend of a full stack web application `EDUSOFT`. The API is a django-restframework application that serves universities public information such as Country and State location, courses offered, tuition fee etc.


## API documentation

### `/api/universites`
- Methods: `GET`
- Description: Get the list of all universities
- URL Queries:
  - limit: number of items return e.g
  - search: search universities based on course e.g `/api/universities/?search=software` return a list of universities that offers courses containing software
```
/api/universities?limit=10
```
- Response:
```
{
    "count": 3,
    "next": "<BASE_URL>/api/universities/?page=2",
    "previous": "<BASE_URL>/api/universities/",
    "results": [
        {
            "id": "f8497301-0e9f-403f-9b84-6fa38c18d336",
            "name": "Ladoke Akintola University of Technology",
            "history": "Founded in August 1990, with the aim of making education accessible to the masses of Oyo state",
            "languages": [
                "Yoruba",
                "English"
            ],
            "created_by": "idris",
            "country": "Nigeria",
            "city": "Ogbomoso",
            "accomodation": "Off-campus Accomodation",
            "website": "https://www.lautech.edu.ng"
        }
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


### Running tests for APIs
#### Setup
The api test requires interraction with the database i.e `test_db.sqlite3` which is a copy of the default dev `db.sqlite3` database.

1. Run (skip this step if `db.sqlite3` is already setup

```
python manage.py makemigrations [backend]
python manage.py migrate
python manage.py cities_light  # populate countries and cities (might take some time to complete)

```

2. Create the test db
```
cp db.sqlite3 test_db.sqlite3
```

3. Run the test

```
python manage.py test api --keepdb
```
