from fastapi import FastAPI
# import routers.post, routers.user, routers.auth, routers.likes  # import routers for development
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, likes  # For production

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

# # For development...
# app.include_router(routers.post.router)
# app.include_router(routers.likes.router)
# app.include_router(routers.user.router)
# app.include_router(routers.auth.router)

# For production...
app.include_router(post.router)
app.include_router(likes.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

