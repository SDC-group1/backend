# backend

## ⚒️ Env Setup 
### Setup virtual env 
```bash
python -m venv venv
```

Activate
```bash
source venv/bin/activate
```

Verify 
```bash
echo $VIRTUAL_ENV
```

### Install dependencies 

```bash
pip install -r requirements.txt
```

Freeze denpendencies 
```bash
pip freeze > requirements.txt
```
---

## 🖥️ Run the server 

```bash
uvicorn app.main:app --reload
```

---

## API 

### User
1. `POST api/auth/login` → Login 

### Post
1. `POST api/blog` → Create blog
2. `GET  api/blogs` → Browse blogs
---

## Test API 

### 1. Create fake data in development env
```bash
python app.seed.seed_runner.py
```

```bash
docker-compose run fastapi python app.seed.seed_runner.py
```

### 2. Check DB
if not yet installed 
```bash
sudo apt install sqlite3
```

should return fake data if seed_runner works
```bash
sqlite3 database.db
```

```bash
SELECT * FROM users;
SELECT * FROM posts;
SELECT * FROM comments;
SELECT * FROM user_settings;
```
