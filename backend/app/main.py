from fastapi import FastAPI

app = FastAPI(
    title="uMthombolwazi Intelligence API",
    version="0.1.0",
)


@app.get("/api/v1/health", tags=["health"])
def get_health() -> dict[str, str]:
    return {"status": "healthy"}
