from fastapi import FastAPI
from Api.api import router
# db configs
from db.base import Base
from db.session import engine
from fastapi.middleware.cors import CORSMiddleware

# table creation
Base.metadata.create_all(bind=engine)
# instance of the fastAPI
app = FastAPI(
    title="Vicci Expeses API",
    description="A sample Expenses API",
    version="0.1.0",
    docs_url="/vicciexpenses/docs",
    redoc_url="/vicciexpenses/redoc",
    contact={
        "name":"Vicci",
        "email":"vicci2regia@gmail.com",
        "tel":"0728893493"
    }    
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Custom request responses
app.include_router(router,responses={
     200: {'description': 'Ok'},
                       201: {'description': 'Created'},
                       202: {'description': 'Accepted'},
                       400: {"description": "Bad Request"},
                       401: {"description": "Unauthorized"},
                       403: {"description": "Forbidden"},
                       404: {"description": "Not found"},
                       405: {"description": "Method not allowed"}
                       })