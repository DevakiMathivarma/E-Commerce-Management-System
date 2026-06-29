from fastapi import APIRouter,Depends,Query,status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.schemas.order_schema import OrderCreate,OrderResponse,OrderList
from app.services.order_service import create_order_service,get_orders_service,get_order_by_id_service
from app.utils.auth import customer_required


# order router

router=APIRouter(prefix="/orders",tags=["Orders"])


# create order

@router.post("/",response_model=OrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return create_order_service(current_user,db)


# get all orders

@router.get("/",response_model=OrderList)
def get_orders(status:str|None=Query(None),page:int=Query(1,ge=1),limit:int=Query(10,ge=1),db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return get_orders_service(current_user,db,status,page,limit)


# get order by id

@router.get("/{order_id}",response_model=OrderResponse)
def get_order(order_id:int,db:Session=Depends(get_db),current_user:User=Depends(customer_required)):
    return get_order_by_id_service(order_id,current_user,db)