from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas.cart_schema import CartAdd,CartResponse
from app.services.cart_service import add_to_cart_service,get_cart_service,remove_cart_item_service
from app.utils.auth import customer_required


# cart router

router=APIRouter(prefix="/cart",tags=["Cart"])


# add to cart

@router.post("/add",status_code=status.HTTP_201_CREATED)
def add_to_cart(cart_item:CartAdd,db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return add_to_cart_service(cart_item,current_user,db)


# get cart

@router.get("/",response_model=CartResponse)
def get_cart(db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return get_cart_service(current_user,db)


# remove cart item

@router.delete("/remove/{product_id}")
def remove_cart_item(product_id:int,db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return remove_cart_item_service(product_id,current_user,db)