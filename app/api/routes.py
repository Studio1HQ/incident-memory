from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.payment import service
from app.payment.models import Charge

router = APIRouter()

class CreateChargeRequest(BaseModel):
    user_id: str
    amount: int

@router.post("/charge", response_model=Charge)
def create_charge(request: CreateChargeRequest):
    try:
        charge = service.create_charge(request.user_id, request.amount)
        return charge
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/charge/{charge_id}/confirm")
def confirm_charge(charge_id: str):
    try:
        service.confirm_charge(charge_id)
        return {"status": "confirmed"}
    except IOError as e:
        # This is where we simulate the transient error
        # In a real app, this might trigger a rollback
        service.rollback_charge(charge_id)
        raise HTTPException(status_code=500, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/charge/{charge_id}/rollback")
def rollback_charge(charge_id: str):
    try:
        service.rollback_charge(charge_id)
        return {"status": "rolled_back"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/charge/{charge_id}/refund")
def refund_charge(charge_id: str):
    try:
        service.refund_charge(charge_id)
        return {"status": "refunded"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
