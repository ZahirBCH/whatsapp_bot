import sys
import os
from fastapi.testclient import TestClient
from order_service.main import app

# Ajouter le chemin du projet pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue dans le service de gestion des commandes !"}

def test_create_order():
    response = client.post("/orders/", json={
        "client_name": "John Doe",
        "departure_city": "Paris",
        "delivery_city": "Lyon",
        "weight": 3.5
    })
    assert response.status_code == 200
    assert "order_id" in response.json()

def test_read_order():
    # Créer une commande avant de tester la récupération
    create_response = client.post("/orders/", json={
        "client_name": "Jane Doe",
        "departure_city": "Marseille",
        "delivery_city": "Lille",
        "weight": 5.0
    })
    assert create_response.status_code == 200

    # Récupérer l'ID de la commande créée
    order_id = create_response.json().get("order_id")
    assert order_id is not None

    # Effectuer un GET sur l'ID de la commande créée
    get_response = client.get(f"/orders/{order_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == order_id
    assert get_response.json()["client_name"] == "Jane Doe"