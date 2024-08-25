from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import uvicorn
app = FastAPI()
config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account',  # force to select account
    },
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    authorize_url = 'https://accounts.google.com/o/oauth2/v2/auth',
    access_token_url = 'https://oauth2.googleapis.com/token'
)

app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request,"index.html")

@app.get('/login')
async def login(request: Request):
    google = oauth.create_client('google')
    redirect_uri = request.url_for('auth')
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request= request, redirect_uri = redirect_uri)


@app.get('/auth')
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        request.session['user'] = user
    return RedirectResponse(url='/')

if __name__ == "__main__":
    uvicorn.run(app, reload=True, host="0.0.0.0", port=8000)

