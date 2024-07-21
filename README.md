# My Blog Application

## Overview

This is a blog application built with Django and Django REST Framework. It includes features for user authentication, creating, updating, deleting posts, managing comments, and liking posts.

## Blog Project Details

For more detailed information about the blog project, you can refer to the [Blog Project Details](https://docs.google.com/document/d/1ITP1w2p5g_LG9ngR2k3n4-FURQiMGx6L4v0fNUbWsCI/edit) document.


## Getting Started

### Prerequisites

- Python 3+
- Django 4.x
- Django REST Framework
- PostgreSQL (or any other database supported by Django)
- PgAdmin

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/your-repo.git
    cd your-repo
    git checkout -b 'new_branch_name'
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv blogvenv
    source blogvenv/bin/activate  # On Windows use `blogvenv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r req.txt
    ```

4. **Set up PostgreSQL database using PgAdmin:**

    - **Install PostgreSQL:** Follow the instructions for your operating system to install PostgreSQL.

    - **Start PostgreSQL server:**

        ```bash
        pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
        ```

    - **Access PostgreSQL shell:**

        ```bash
        psql postgres
        ```

    - **Create a new database and user:**

        ```sql
        CREATE DATABASE db_name;
        CREATE USER username WITH PASSWORD 'password';
        GRANT ALL PRIVILEGES ON DATABASE blog TO username;
        ```

    - **Check the created databases:**

        ```sql
        \l
        ```

    - **Grant privileges on all tables in the schema:**

        ```sql
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;
        ```

    - **Set the database URL and page limit in your `.env` file:**

        ```bash
        BLOG_DB_CONFIG=postgres://username:password@localhost/blog
        PAGE_LIMIT=10
        ```

5. **Set up the database:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

   Your application will be running at `http://127.0.0.1:8000/`.

## API Endpoints

### User

#### Register

- **Endpoint:** `/register/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X POST http://127.0.0.1:8000/register/ \
    -H "Content-Type: application/json" \
    -d '{"username": "newuser", "password": "password123", "email": "user@example.com"}'
    ```
- **Response:**
    ```json
    {
        "Message": "Registered Successfully"
    }
    ```

#### Login

- **Endpoint:** `/signin/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X POST http://127.0.0.1:8000/signin/ \
    -H "Content-Type: application/json" \
    -d '{"username": "newuser", "password": "password123"}'
    ```
- **Response:**
    ```json
    {
        "access": "access_token_here",
        "refresh": "refresh_token_here"
    }
    ```

#### Refresh Token

- **Endpoint:** `/api/token/refresh/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
    -H "Content-Type: application/json" \
    -d '{"refresh": "refresh_token_here"}'
    ```
- **Response:**
    ```json
    {
        "access": "new_access_token_here"
    }
    ```

#### Logout

- **Endpoint:** `/logout/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X POST http://127.0.0.1:8000/logout/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer access_token_here" \
    -d '{"refresh_token": "refresh_token_here"}'
    ```
- **Response:**
    ```json
    {
        "message": "Logged out successfully"
    }
    ```

### Post

#### List Posts

- **Endpoint:** `/posts/`
- **Method:** POST
- **Response:**
    ```bash
    curl -X GET http://127.0.0.1:8000/posts/
    ```
    ```json
    {
        "page_context": {
            "page_number": 1,
            "page_count": 1,
            "total_count": 1,
            "total_number_of_pages": 1
        },
        "result": [
            {
                "id": "1",
                "title": "First Post",
                "content": "This is the content of the first post.",
                "author": "author_username",
                "created": "2024-07-21T05:20:05.409228Z",
                "modified": "2024-07-21T05:20:05.409251Z"
            }
        ]
    }
    ```

#### Create Post

- **Endpoint:** `/posts/create/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X POST http://127.0.0.1:8000/posts/create/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer access_token_here" \
    -d '{"title": "New Post Title", "content": "Content of the new post."}'
    ```
- **Response:**
    ```json
    {
        "id": "2",
        "title": "New Post Title",
        "content": "Content of the new post.",
        "author": "author_username",
        "created": "2024-07-21T05:20:05.409228Z",
        "modified": "2024-07-21T05:20:05.409251Z"
    }
    ```

#### Retrieve Post

- **Endpoint:** `/posts/retrieve/{post_id}/`
- **Method:** GET
- **Response:**
    ```bash
    curl -X GET http://127.0.0.1:8000/posts/retrieve/1/
    ```
    ```json
    {
        "id": "1",
        "title": "First Post",
        "content": "This is the content of the first post.",
        "author": "author_username",
        "created": "2024-07-21T05:20:05.409228Z",
        "modified": "2024-07-21T05:20:05.409251Z"
    }
    ```

#### Update Post

- **Endpoint:** `/posts/update/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X PUT http://127.0.0.1:8000/posts/update/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer access_token_here" \
    -d '{"title": "Updated Title", "content": "Updated content."}'
    ```
- **Response:**
    ```json
    {
        "id": "1",
        "title": "Updated Title",
        "content": "Updated content.",
        "author": "author_username",
        "created": "2024-07-21T05:20:05.409228Z",
        "modified": "2024-07-21T05:20:05.409251Z"
    }
    ```

#### Delete Post

- **Endpoint:** `/posts/delete/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X DELETE http://127.0.0.1:8000/posts/delete/ \
    -H "Authorization: Bearer access_token_here" \
    -d '{"post_id": "1"}'
    ```
- **Response:**
    ```json
    {
        "Message": "Post Deleted Successfully"
    }
    ```

#### Like Post

- **Endpoint:** `/posts/like/1/`
- **Method:** GET
- **Request:**
    ```bash
    curl -X GET http://127.0.0.1:8000/posts/like/1/ \
    -H "Authorization: Bearer access_token_here"
    ```
- **Response:**
    ```json
    {
        "Message": "Post Liked Successfully",
        "LikeCount": 5
    }
    ```

### Comments

#### List Comments

- **Endpoint:** `/comments/`
- **Method:** POST
- **Request Parameters:**
    ```bash
    curl -X GET http://127.0.0.1:8000/comments/ \
    -d 'post_id=1'
    ```
- **Response:**
    ```json
    {
        "post_id": "1",
        "comments": [
            {
                "id": "1",
                "text": "This is a comment.",
                "author": "author_username",
                "created": "2024-07-21T05:20:05.409228Z",
                "modified": "2024-07-21T05:20:05.409251Z"
            }
        ]
    }
    ```

#### Create Comment

- **Endpoint:** `/comments/create/`
- **Method:** POST
- **Request Body:**
    ```bash
    curl -X POST http://127.0.0.1:8000/comments/create/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer access_token_here" \
    -d '{"post_id": "1", "text": "This is a new comment."}'
    ```
- **Response:**
    ```json
    {
        "id": "2",
        "text": "This is a new comment.",
        "author": "author_username",
        "created": "2024-07-21T05:20:05.409228Z",
        "modified": "2024-07-21T05:20:05.409251Z"
    }
    ```
    

## Additional Notes

1. **Database:** PostgreSQL is used as the database in the local development environment.
2. **Like Option:** Only the "Like" option is provided. A "Dislike" option was not included as it was not specified.
3. **Pagination:** Pagination is implemented only for the GET `/posts/` endpoint. Comments are not paginated as this was not mentioned.
