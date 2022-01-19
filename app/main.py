from fastapi import FastAPI
import routers.post, routers.user, routers.auth, routers.likes
from fastapi.middleware.cors import CORSMiddleware

# import models

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# To give access to who want to access it.
origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.post.router)
app.include_router(routers.likes.router)
app.include_router(routers.user.router)
app.include_router(routers.auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

