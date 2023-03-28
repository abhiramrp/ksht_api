from fastapi import FastAPI

from app.db import database, User

from fastapi_keycloak import FastAPIKeycloak, OIDCUser
from fastapi.responses import RedirectResponse


app = FastAPI(title="Karya Siddhi Hanuman Temple")

idp = FastAPIKeycloak(
    server_url="http://localhost:8890/",
    client_id="ksht_client",
    client_secret="7vF3BOpO5NJC6vKQ8RT8qppNAVdLXDiw",
    admin_client_secret="ZUVI3IQXBDxNqPml2dunQ5wpP5TD4pXZ", 
    realm="ksht_realm", 
    callback_uri="http://localhost:8009/"
)
idp.add_swagger_config(app)


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

@app.get("/identity-providers", tags=["admin-cli"])
def get_identity_providers():
    return idp.get_identity_providers()


@app.get("/idp-configuration", tags=["admin-cli"])
def get_idp_config():
    return idp.open_id_configuration

@app.get("/login")
def login_redirect():
    return RedirectResponse(idp.login_uri)