from fastapi import FastAPI
from core.database import Base, engine
from api import auth
from api import journal
Base.metadata.create_all(bind=engine)

app = FastAPI()


# hello world api test
@app.get('/')
def hello () :
    return {"message" : "Hello World."}


app.include_router(auth.router)
app.include_router(journal.router)

