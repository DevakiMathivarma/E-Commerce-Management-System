from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas.payment_schema import PaymentCreate,PaymentResponse
from app.services.payment_service import create_payment_service,get_payment_by_id_service
from app.utils.auth import customer_required


# payment router

router=APIRouter(prefix="/payments",tags=["Payments"])


# create payment

@router.post("/{order_id}",response_model=PaymentResponse,status_code=status.HTTP_201_CREATED)
def create_payment(order_id:int,payment:PaymentCreate,db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return create_payment_service(order_id,payment,current_user,db)


# get payment by id

@router.get("/{payment_id}",response_model=PaymentResponse)
def get_payment(payment_id:int,db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return get_payment_by_id_service(payment_id,current_user,db)