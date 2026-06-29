from pydantic import BaseModel,ConfigDict
from app.models import OrderStatus


# order item response schema

class OrderItemResponse(BaseModel):
    product_id:int
    product_name:str
    price:float
    quantity:int
    subtotal:float

    model_config=ConfigDict(from_attributes=True)


# create order schema

class OrderCreate(BaseModel):
    pass

"""customer_id → from the logged-in JWT user.
total_amount → calculated from the cart.
order_status → defaults to Pending."""

# order response schema

class OrderResponse(BaseModel):
    id:int
    customer_id:int
    total_amount:float
    order_status:OrderStatus
    items:list[OrderItemResponse]

    model_config=ConfigDict(from_attributes=True)


# order list schema

class OrderList(BaseModel):
    total_records:int
    current_page:int
    limit:int
    data:list[OrderResponse]