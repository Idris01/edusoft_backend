# Introduction
Welcome to the github repository of Edusoft website backend( written with django-restframework)

Edusoft is an education website that allows people who desires to study in any university around the world search and connect to their desired university and course with an adequate informations with respect to course, tuition accommodation and application processess and procedures.

## Project Link
https://edusoft-test.vercel.app/

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
    "first_name":"adeyemi",
    "last_name":"idris",
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
   curl <BASE_URL>/api/users/<id>/profile -H "Content-Type:application/json" -H "Authorization:Bearer <access_token>"
   ```

### `/api/token/refresh`
- Methods: POST
- Description: request for new access token to maintain log-in state
- Sample Request:

```
curl -X POST <base-url>/api/token/refresh -H "Content-Type:application/json" -d '{"refresh": <refresh_token>}'
```

- Sample Response:

```
{
	"access": <new-access-token>
}
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
{
	'id': 'f8497301-0e9f-403f-9b84-6fa38c18d336',
	'name': 'Lagos State University',
	'history': 'Founded August 1990',
	'languages': ['Yoruba', 'English'],
	'created_by': 'adeyemi',
	'country': 'Nigeria',
	'city': 'Lagos',
	'accomodation': 'On-campus accomodation available',
	'website': 'https://www.unilag.edu.ng',
	'postal_code': '210500',
	'country_code': 'NG'
}
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



### `/api/user`
- Methods:
    - GET (Authentication required)
      - Description: Get the primary information of a given authenticated user
	- Sample Request:
	```
	curl -X GET <base-url>/api/user \
		-H "Content-Type: application/json" \
		-H "Authorization: Bearer {access_token}"
	```
     	- Sample Response:
	{
		"id": 3f225-6b51-43bf-ad4f-e9c79800b92f',
		'username': 'adeyemi',
		'first_name': 'ade',
		'last_name': 'idris',
		'email': 'idris01@gmail.com',
		'is_active': True
	}

	```


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
					'university_id': 'cc932788-0f3c-4547-b4a8-10070d1d2fb5',
					'university': 'osun state university'
				},
				{
					'id': 'e8e8c34c-590c-433b-a814-67e51f93b47f',
					'name': 'Crop Production',
					'university_id': 'cc932788-0f3c-4547-b4a8-10070d1d2fb5',
					'university': 'osun state university'
				},
				{
					'id': 'dfb16994-6000-45c9-8c8a-3f4baad56ea9',
					'name': 'General Medicine',
					'university_id': 'ebbb46f3-c309-4c9e-aeaa-7b731d6d9120',
					'university': 'University of london'
				},
				{
					'id': 'cb039da2-b5bd-4bd2-9575-b2891a63ab3d',
					'name': 'Medical laboratory Science',
					'university_id': 'ebbb46f3-c309-4c9e-aeaa-7b731d6d9120',
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
        {'name': 'Nursing studies'}]
}
```

### `/api/courses/<slug:id>/`
-  Methods: GET
-  Description: Get detail of a given course with id "id"
-  Sample Request:
```
curl -X GET <base-url>/api/course/677062cf-8fc1-4ce7-939e-565109c132ad
```

-  Sample Response:

```
{
	'id': '677062cf-8fc1-4ce7-939e-565109c132ad',
	'name': 'Animal Production and Health',
	'about': 'This deals with the study of Animal Production and Health',
	'degrees': [],
	'university': 'University Of Ilorin',
	'university_id': 'e7e484d9-6b2c-4e80-af09-d085f90ddacc',
	'department': 'Department Of Agriculture',
	'department_id': '9339dc20-b311-4998-ad83-6fcddd0f3aaa'
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

## Contributing:
[Idris Adebowale](https://github.com/idris01)
[Gloria Nwaigba](https://github.com/Nwaigba66)


## Licensing

MIT License

Copyright (c) 2023 Idris01

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
