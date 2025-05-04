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

### Install dependencies 

```bash
pip install -r requirements.txt
```

Freeze denpendencies 
```
pip freeze > requirements.txt
```
---

## 🖥️ Run the server 

```bash
uvicorn app.main:app --reload
```






