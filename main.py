from fastapi import FastAPI, status
from project.src import models
from project.src.database import engine

from project.src.routers import blog, user, login

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)

##################################################################
# PATH '/'
##################################################################

@app.get('/', status_code=status.HTTP_200_OK)
def root():
    return {"data" : {"description" : "This is the root page"}}