from fastapi import FastAPI
from fastapi import APIRouter
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from src.api.endpoints import router
from src.bot import bot


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import threading
    threading.Thread(target=bot.run).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
