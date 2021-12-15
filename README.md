# Awadz

#### BY David Mathaga

## Description

Awadz is a simple photo web application to showcase user projects that he or she has done. Users get to view projects updated by other users. They can also click on a project and view more details about it. Users can also leave ratings on selected projects.



## Setup Requirements

- Git
- Web-browser or your choice
- Github
- Django
- Pip
- Python
- PostgreSQL
- Cloudinary (for image upload)

```
   - CLOUD_NAME
   - API_KEY
   - API_SECRET
```

### Prerequisites
Things you need to install the project and how to install them
```
Python : https://www.python.org/
Django : pip install django
```
### Installing and SetUp
1) Clone or download this project.
2) Set Up Virtual Environment and activate it
```
python -m venv --without-pip env
source env/bin/activate
```
3) Install dependencies
```
pip install -r requirements.txt
```
4) Change database settings in case you want to use PostgreSQL or MySQL
5) Migrate data using command 
```
python manage.py makemigrations
python manage.py migrate
```
6) Create Superuser
```
python manage.py createsuperuser
```
7) Run project on localhost:
```
python manage.py runserver
```
