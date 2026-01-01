from fastapi import FastAPI
from core.database import Base, engine
from api import auth
from api import journal , forum
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)


app.include_router(journal.router)
app.include_router(forum.router)