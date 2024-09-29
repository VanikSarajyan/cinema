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
