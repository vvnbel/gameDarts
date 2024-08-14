from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import game
from database import engine, Base
from fastapi.staticfiles import StaticFiles


# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Дополнительный маршрут для проверки работоспособности
@app.get("/health")
def health_check():
    return {"status": "ok"}

