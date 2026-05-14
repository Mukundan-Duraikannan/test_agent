from fastapi import FastAPI
from routes.ingestion_routes import router
from fastapi.staticfiles import StaticFiles
app = FastAPI(title="Repository Ingestion Engine")
app.include_router(router)
app.mount("/graphs", StaticFiles(directory="storage/graphs"), name="graphs")