from fastapi import FastAPI

from auth.routes import router as auth_router

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix='/auth', tags=['auth'])

