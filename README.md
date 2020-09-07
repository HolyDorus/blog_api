# Blog API
This app allows you to manage your blog with HTTP requests. It is possible to view, create, edit, delete and block articles. It is also possible to register and authorize users.

## Installation
All dependencies locate in `pyproject.toml`, so you can use [poetry](https://github.com/python-poetry/poetry)
1. You need to download all files from this repository
`git clone https://github.com/HolyDorus/blog_api`

2. Use this command to install all dependencies
    ```
    cd blog_api
    poetry install
    ```

3. You need to create file `.env`  with filled values (see `.env.example`) or manually add values in your enviroment variables

4. Next, run application
`poetry run python runserver.py`

5. You can send requests to [localhost:5000](http://localhost:5000) (by default)

## Usage
A table describing all the endpoints is shown below.
|URL|Method|Description|
|---|---|---|
|/articles/|GET|Returns a list of articles|
|/articles/|POST|Creates a new article|
|/articles/{article_id}/|GET|Returns article by id|
|/articles/{article_id}|PUT, PATCH|Updates article by id|
|/articles/{article_id}|DELETE|Removes article by id|
|/articles/{article_id}/ban|POST|Ban (hide) article by id|
|/articles/{article_id}/unban|POST|Unban (unhide) article by id|
|/auth/login/|POST|Authorizes the user and returns access and refresh tokens|
|/auth/register/|POST|Registers a new user|
