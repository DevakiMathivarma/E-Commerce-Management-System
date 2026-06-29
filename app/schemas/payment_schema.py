from pydantic import BaseModel,Field,ConfigDict
from app.models import PaymentMethod,PaymentStatus


# payment base schema

class PaymentBase(BaseModel):
    amount:float=Field(...,gt=0)
    payment_method:PaymentMethod


# create payment schema

class PaymentCreate(PaymentBase):
    pass


# payment response schema

class PaymentResponse(PaymentBase):
    id:int
    order_id:int
    payment_status:PaymentStatus

    model_config=ConfigDict(from_attributes=True)