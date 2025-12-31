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

# uvicorn main:app --host 0.0.0.0 --port 8000
# this command to make it accessable by IP adress


# adi ay t3i nti ak windows user
# you can just run this command in ubuntu to get ip4v address
# hostname -I