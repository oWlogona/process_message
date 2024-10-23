from fastapi import FastAPI

from api import setup_api
from services.storage.database import create_tables, database


def setup_app():
    main_app = FastAPI(version="0.1.0", description="Process api", debug=True)
    setup_api(main_app)
    return main_app


app = setup_app()


@app.on_event("startup")
async def startup():
    await database.connect()
    await create_tables()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
