from fastapi import FastAPI

# import database
from auth.routes import router as auth_router

# database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth_router, prefix='/auth', tags=['auth'])

