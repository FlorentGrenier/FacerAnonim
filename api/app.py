from fastapi import FastAPI
from api.routes import router  # Import des routes

app = FastAPI(
    title="FacerAnonim API",
    description="API pour anonymiser du texte en utilisant la NER et le remplacement contextuel ",
    version="1.0",
    docs_url="/",
    redoc_url="/redoc"
)

app.include_router(router)  # On ajoute les routes

# Endpoint de test
@app.get("/anonymize/healthcheck")
def health_check():
    """
    Vérifie l'état de l'API.
    
    - Retourne un message indiquant si l'API est active ou non.
    """
    return {"message": "API is running!"}
