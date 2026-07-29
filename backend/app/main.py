from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, feed, follows, games, recommendations, reviews
from app.db.session import init_db

app = FastAPI(
    title="Game Diary API",
    description="Backend do app estilo Letterboxd para jogos, usando RAWG como fonte de dados.",
    version="0.1.0",
)

# Em desenvolvimento libera geral; restrinja isso antes de ir pra produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Em desenvolvimento cria as tabelas automaticamente.
    # Em produção prefira gerenciar isso via Alembic (pasta /alembic).
    init_db()


app.include_router(auth.router)
app.include_router(games.router)
app.include_router(reviews.router)
app.include_router(follows.router)
app.include_router(feed.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "game-diary-api"}
