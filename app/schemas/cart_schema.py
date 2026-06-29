from pydantic import BaseModel,Field,ConfigDict


# cart item base schema

class CartItemBase(BaseModel):
    product_id:int
    quantity:int=Field(...,gt=0)


# add to cart schema

class CartAdd(CartItemBase):
    pass


# cart item response schema

class CartItemResponse(BaseModel):
    product_id:int
    product_name:str
    price:float
    quantity:int
    subtotal:float

    model_config=ConfigDict(from_attributes=True)


# cart response schema

class CartResponse(BaseModel):
    id:int
    user_id:int
    total_amount:float
    items:list[CartItemResponse]

    model_config=ConfigDict(from_attributes=True)