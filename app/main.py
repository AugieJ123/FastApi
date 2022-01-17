from fastapi import FastAPI
import routers.post, routers.user, routers.auth 

import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

app.include_router(routers.post.router)
app.include_router(routers.user.router)
app.include_router(routers.auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

