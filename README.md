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

1. `GET /blogs/` → Get all blogs

2. `GET /blogs/{blog_id}`  → Get blog by ID

3. `POST /blogs/` → Create a new blog


--

## Test API 

```bash
pytest spec/
```

