# Edusoft Backend
This is the backend of a full stack web application `EDUSOFT`. The API is a django-restframework application that serves universities public information such as Country and State location, courses offered, tuition fee etc.


## API documentation

### `/api/users`

- METHODS: `GET`, `POST`
  - `GET`:
    Only Admin user can get list of users
    -  sample request
    ```
        curl -X GET <BASE_URL>/api/users
    ```
    -  sample response
    ```
        {
            "prev": null,
            "next": null,
            "count": 2,
            "results": [
                {
                    "id": "12abd-qq45689-12",
                    "username": "Idris1",
                    "first_name": "Adeyemi",
                    "last_name": "Adebowale",
                    "is_active": True,
                    "email": "idrys01@gmail.com"
                },
                {
                    "id": "32abd-qq45689-12",
                    "username": "Idris2",
                    "first_name": "Adeyemi",
                    "last_name": "Adebowale",
                    "is_active": True,
                    "email": "idrys02@yahoo.com"
                }
            ]
        }
    ```
  - `POST`: create new user accoun
    - sample request
    ```
        curl -X POST <BASE_URL>/api/users -H "Content-Type=application/json" \
            -d '{ "username":"idris",
                  "first_name": "ade",
                  "last_name": "yemi",
                  "password": "@passWord1",
                  "confirm_password": "@passWord1",
                  "email":"idrys01@gmail.com",
                }'
    ```
    - sample response:
    ```
        {
            "message": "registration successfull",
            "token": "<activation_token>"
        }
    ```

### `/api/account/<token>/verify`
- Methods: `GET`
- Description: Verify a new user account to enable login access

  - Sample request
  ```
  curl -X GET <BASE_URL>/api/account/<token>/verify
  ```
  - Sample Response
  ```
  {
    "message": "Account Verified"
  }
  ```
### `/api/token`
- Methods: `POST`
- Description: login registered user to obtain token pair i.e access and refresh token

  - Sample Request:
  ```
  curl -X POST <BASE_URL>/api/token -H "Content-Type=application/json" -d \
    '{
       "email": "idrys01@gmail.com",
       "password": "@myPassword1"
     }'
  ```

  - Sample Response
  ```
  {
    "username":"idrys01",
    "email": "idrys01@gmail.com",
    "access": <access_token>,
    "refresh": <refresh_token>,
    "access_expiry_seconds": 300,  # short lived 5min
    "refresh_expiry_seconds": 86400, # long lived 1hr
   }
   ```

   - Access token Usage
   After obtaining the token key pair, the access token is always attached to subsequent request as follows

   ```
   curl <BASE_URL>/api/users/<id>/profile -H "Content-Type=application/json, Authorization=Bearer <access_token>"
   ```

### `/api/universites`
- Methods: `GET`, `POST`
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

### `/api/user/profile`
- Methods: GET, POST

- GET
  - Description: Get the profile details of a given logged in user
  - Sample Request:
  ```
  curl -X GET <baseurl>/api/user/profile \
	-H "Content-Type: applicatio/json \
   	-H "Authorization: Bearer <access-token>"
  ```

  - Sample Response:

### `/api/universities/<slug:id>`
- Methods: `GET`, `PUT`, `DELETE`
- Description:
   - *GET* Request:
   Get the detail of a University of `id`

```
curl -X GET <base_url>/universities/f8497301-0e9f-403f-9b84-6fa38c18d336
```
   - Response Body

```
{'id': 'f8497301-0e9f-403f-9b84-6fa38c18d336', 'name': 'Lagos State University', 'history': 'Founded August 1990', 'languages': ['Yoruba', 'English'], 'created_by': 'adeyemi', 'country': 'Nigeria', 'city': 'Lagos', 'accomodation': 'On-campus accomodation available', 'website': 'https://www.unilag.edu.ng', 'postal_code': '210500', 'country_code': 'NG'}
```
   - *PUT* Request:
   Update details of a University of `id`

   - *DELETE* Request:
   Delete the University described by `id`

### `/api/user/profile`
- Methods:
  - GET (Authentication required)
     - Descritpion: Get the profile of a given logged-in user
     - Sample Request:
	```
	curl -X GET <base-url>/api/user/profile \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer {access_token}"
	```
     - Sample Response:
	```
	{
		"nationality": "Nigerian",
		"date_of_birth": "1990-08-20",
		"address" : "Address of User",
		"gender" : "male",
	}
	```

  - PUT
    - Description: Update logged-in user profile

### `/api/courses/list`
  - Methods
    - GET: Get list of all courses (also also accespt search query)
      - Sample Request:
	```
	curl -X GET <base-url>/api/courses/list -H "Content-Type: application/json"
	```
      - Sample Response:
	```
	{
		'count': 5,
		'next': null,
		'previous': null,
		'results':
			[
				{
					'id': 'df6544b1-10f9-4b68-8df7-8420158dd8fe',
					'name': 'Animal Production and Health',
					'department': 'Agricultural of Sciences',
					'university_id': 'cc932788-0f3c-4547-b4a8-10070d1d2fb5',
					'department_id': 'd1c1b6e3-fb65-4144-8a48-b848ae693604',
					'about': 'Study of Farm animal production and health',
					'university': 'osun state university'
				},
				{
					'id': 'e8e8c34c-590c-433b-a814-67e51f93b47f',
					'name': 'Crop Production',
					'department': 'Agricultural of Sciences',
					'university_id': 'cc932788-0f3c-4547-b4a8-10070d1d2fb5',
					'department_id': 'd1c1b6e3-fb65-4144-8a48-b848ae693604',
					'about': 'Study of Crop Production',
					'university': 'osun state university'
				},
				{
					'id': 'dfb16994-6000-45c9-8c8a-3f4baad56ea9',
					'name': 'General Medicine',
					'department': 'Medical studies',
					'university_id': 'ebbb46f3-c309-4c9e-aeaa-7b731d6d9120',
					'department_id': 'e08e8096-0045-4700-8439-ea9df7bbeb24',
					'about': 'General Studies in Medicine',
					'university': 'University of london'
				},
				{
					'id': 'cb039da2-b5bd-4bd2-9575-b2891a63ab3d',
					'name': 'Medical laboratory Science',
					'department': 'Medical studies',
					'university_id': 'ebbb46f3-c309-4c9e-aeaa-7b731d6d9120',
					'department_id': 'e08e8096-0045-4700-8439-ea9df7bbeb24',
					'about': 'Medical lab studies',
					'university': 'University of london'
				},
			]
	}
	```


### `/api/options`
-  Methods: GET
-  Description: This exposes choice of options currently available for the Edusoft API, which can be use in form as filters in the `Frontend`

-  Sample Request:
```
curl -X GET <base-url>/api/options -H "Content-Type: application/json"
```

- Sample Response

```
{
    'countries': [
        {
            'name': 'Nigeria',
            'code2': 'NG'
        }, 
        {
            'name': 'United Kingdom',
            'code2': 'GB'
        }],
    'courses': [
        {'name': 'Animal Production and Health'},
        {'name': 'Crop Production'},
        {'name': 'General Medicine'},
        {'name': 'Medical laboratory Science'}, 
        {'name': 'Nursing studies'}
        ]
}
```


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
ENVIRONMENT=Test ./manage.py test api/tests --keepdb
```
