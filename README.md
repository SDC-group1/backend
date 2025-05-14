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
1. `POST /users/register` → Register 
2. `POST /users/login` → Login 

### Post
1. `POST /posts` → Create all posts
2. `GET  /posts` → Browse all posts
3. `GET  /posts/search?keyword=example` → Search post by keyword 

### Comment 
1. `POST /comments/{post_id}`  → Create comment on certain post 

### Setting 
1. `GET  /settings`  → Get setting 
2. `PUT  /settings`  → Update setting 

--

## Test API 

### 1. Create fake data in development env
```bash
python app/seed_runner.py
```

```bash
docker-compose run fastapi python app/seed_runner.py
```

### 2. Check DB
```bash
sqlite3 database.db
```

```bash
SELECT * FROM users;
SELECT * FROM posts;
SELECT * FROM comments;
SELECT * FROM user_settings;
```
