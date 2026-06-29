from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.models import Order,Payment,User,PaymentStatus,OrderStatus
from app.schemas.payment_schema import PaymentCreate
import logging


# logger

logger=logging.getLogger(__name__)


# create payment service

def create_payment_service(order_id:int,payment:PaymentCreate,current_user:User,db:Session):

    logger.info(f"processing payment for order {order_id}")

    order=db.query(Order).filter(Order.id==order_id).first()

    if not order:
        logger.warning("order not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")

    if order.customer_id!=current_user.id:
        logger.warning("unauthorized payment attempt")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you can pay only for your own orders")

    existing_payment=db.query(Payment).filter(Payment.order_id==order_id,Payment.payment_status==PaymentStatus.SUCCESS).first()

    if existing_payment:
        logger.warning("duplicate payment")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="payment already completed")

    if payment.amount!=order.total_amount:
        logger.warning("invalid payment amount")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="payment amount must match order amount")

    new_payment=Payment(order_id=order.id,amount=payment.amount,payment_method=payment.payment_method,payment_status=PaymentStatus.SUCCESS)

    db.add(new_payment)
    order.order_status=OrderStatus.DELIVERED

    db.commit()

    db.refresh(new_payment)

    logger.info(f"payment successful : {new_payment.id}")

    return new_payment

# get payment by id service

def get_payment_by_id_service(payment_id:int,current_user:User,db:Session):

    logger.info(f"fetching payment {payment_id}")

    payment=db.query(Payment).join(Order).filter(Payment.id==payment_id,Order.customer_id==current_user.id).first()

    if not payment:
        logger.warning("payment not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="payment not found")

    logger.info(f"payment {payment_id} fetched successfully")

    return payment