from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# Dépendance pour obtenir la session de base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=dict)
def create_order(client_name: str, departure_city: str, delivery_city: str, weight: float, db: Session = Depends(get_db)):
    new_order = models.Order(
        client_name=client_name,
        departure_city=departure_city,
        delivery_city=delivery_city,
        weight=weight
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Commande créée avec succès", "order_id": new_order.id}

@router.get("/{order_id}", response_model=dict)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return {
        "id": order.id,
        "client_name": order.client_name,
        "departure_city": order.departure_city,
        "delivery_city": order.delivery_city,
        "weight": order.weight
    }