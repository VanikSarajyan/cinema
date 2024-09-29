# Cinema App

Basic Cinema seat booking app

Deployed [Here](https://cinema-d2v9.onrender.com) | [Swagger API DOCS](https://cinema-d2v9.onrender.com/docs)


Use username and password `admin` to operate as admin user
Use username and password `user` to operate as regular user


## If you want to run locally

## Option 1. Using Docker
Navigate to project root directory and run
```
    docker compose up --build
```

## Option 2. Manual setup
1. Istall dependencies from `requirements.txt`
```
    pip install -r requirements.txt
```

2. Run database migrations
```
    alembic upgrade head
```

3.1 Run uvicorn server
```
   uvicorn app.main:app --host 0.0.0.0 --port 80
```

### Or just simply

3.2
```
    python app/main.py 
```

## After setup open your browser at http://localhost:80/


# Project Improvements:

### Project Improvements:

- Ensure all resources have complete CRUD functionality.
- Implement comprehensive testing and CI pipeline:
  - Add unit and integration tests.
  - Incorporate linting and code formatting tools (e.g., `flake8`, `black`, `isort`).
- Improve naming conventions and enforce code style consistency across the project.
- Enhance the user interface (UI) to make it more comprehensive and intuitive for end-users.
- Replace hardcoded values with configuration files and environment variables for:
  - API keys
  - Database URLs
  - Other sensitive settings and configurable variables
- Transition to a production-grade database for better scalability and performance.
- Implement stricter data validation and business logic validation across the system.
- Support non-rectangular room designs to allow more flexible seat arrangements.
- Ensure design consistency by using a service layer for all internal logic.
- Use [Poetry](https://python-poetry.org/) for better dependency management and packaging.