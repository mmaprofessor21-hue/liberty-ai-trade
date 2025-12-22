# TIMESTAMP: 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.api_routes import router

app = FastAPI(title="Liberty AI Trade API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok", "service": "Liberty AI Trade API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
