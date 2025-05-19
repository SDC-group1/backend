from fastapi import Request, APIRouter, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from urllib.parse import urlencode, parse_qs
from .. import crud, schemas, auth, models, database

load_dotenv()

router = APIRouter()

config = Config(environ=os.environ)
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@router.get("/login")
async def login(request: Request, c: str = None):
    redirect_uri = request.url_for('auth_callback')
    if c:
        state_str = urlencode({"c": c})
        return await oauth.google.authorize_redirect(
            request,
            redirect_uri,
            state=state_str
        )

    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request, db: Session = Depends(database.get_db)):
    token = await oauth.google.authorize_access_token(request)
    
    state = request.query_params.get("state")
    parsed_state = parse_qs(state or "")
    frontend_callback = parsed_state.get("c", [None])[0]

    resp = await oauth.google.get("https://openidconnect.googleapis.com/v1/userinfo", token=token)
    user_info = resp.json()
    print(user_info)
    
    user: models.User = crud.find_user_by_email(db, user_info["email"])
    if (user == None):
        user = crud.create_user(db, schemas.UserCreate(
            username=user_info["name"],
            email=user_info["email"]))
    
    jwt = auth.create_access_token({
        "email": user.email
    })
    
    if (frontend_callback):
        return RedirectResponse(url=f"{frontend_callback}?access_token={jwt}")
    else:
        return {"user_info": user_info, "access_token": jwt}