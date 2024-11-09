from fastapi import FastAPI
from .database import engine, Base
from .routers import orders

app = FastAPI()

# Création des tables si elles n'existent pas déjà
Base.metadata.create_all(bind=engine)

# Inclusion des routes
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans le service de gestion des commandes !"}