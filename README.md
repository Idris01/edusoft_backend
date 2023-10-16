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

![data model]('./updatedModelDiagram.png')
