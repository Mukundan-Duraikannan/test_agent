from fastapi import FastAPI
from routes.ingestion_routes import router
app = FastAPI(title="Repository Ingestion Engine")
app.include_router(router)