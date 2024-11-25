# Spy Cat Agency Management System

A Django-based RESTful API for managing spy cats, their missions, and targets for the Spy Cat Agency (SCA).

---

## **Features**

- Manage spy cats:
  - Add, view, update, and delete cats.
- Manage missions:
  - Create missions with targets.
  - Assign cats to missions.
  - Update targets and notes.
  - Mark targets and missions as complete.
  - List and view details of missions.
- Validations:
  - Missions cannot be deleted if assigned to a cat.
  - Notes cannot be updated if a target or mission is marked as complete.
  - Targets cannot be updated after completion.

---

## **Getting Started**

Follow these instructions to set up and run the project locally.

### Prerequisites

- Python 3.8+
- Pipenv (or pip)
- PostgreSQL (optional; default is SQLite)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/y-kondrashova/spy_cat_agency
    cd spy_cat_agency
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    pipenv install
    pipenv shell
    ```

3. Configure the `.env` file with your database credentials (if using PostgreSQL):
    ```env
    DATABASE_URL=postgres://username:password@localhost:5432/spy_cat_db
    SECRET_KEY=your_secret_key
    DEBUG=True
    ```

4. Apply migrations:
    ```bash
    python manage.py migrate
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

The API will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## **Endpoints**

### Cats

| Method | URL                   | Description                    |
|--------|-----------------------|--------------------------------|
| GET    | `/api/cats/`          | List all cats                 |
| POST   | `/api/cats/`          | Create a new cat              |
| GET    | `/api/cats/{id}/`     | Retrieve a single cat         |
| PUT    | `/api/cats/{id}/`     | Update cat information        |
| DELETE | `/api/cats/{id}/`     | Delete a cat                  |

### Missions

| Method | URL                           | Description                                  |
|--------|-------------------------------|----------------------------------------------|
| GET    | `/api/missions/`              | List all missions                           |
| POST   | `/api/missions/`              | Create a new mission with targets           |
| GET    | `/api/missions/{id}/`         | Retrieve a single mission                   |
| PATCH  | `/api/missions/{id}/assign-cat/` | Assign a cat to a mission                  |
| PATCH  | `/api/missions/{id}/`         | Update a mission (e.g., mark as complete)   |
| DELETE | `/api/missions/{id}/`         | Delete a mission                            |

### Targets

| Method | URL                                  | Description                                 |
|--------|--------------------------------------|---------------------------------------------|
| GET    | `/api/missions/{mission_id}/targets/` | List all targets for a specific mission    |
| POST   | `/api/missions/{mission_id}/targets/` | Add targets to a specific mission          |
| GET    | `/api/missions/{mission_id}/targets/{id}/` | Retrieve a specific target              |
| PUT    | `/api/missions/{mission_id}/targets/{id}/` | Update a target's details                |
| PATCH  | `/api/missions/{mission_id}/targets/{id}/mark-complete/` | Mark a target as complete             |

---

## **Postman Collection**

To test the API, import the [Postman Collection](https://spycat.postman.co/workspace/Spy_cat-Workspace~56818bc3-44de-46a4-9fb9-ca29e8c72711/collection/11124023-952d241c-9e9f-4790-abc2-61bfa229cea4?action=share&creator=11124023).

### Steps to Use the Collection:
1. Open Postman.
2. Click **Import**.
3. Paste the collection link or upload the `.json` file.

---

