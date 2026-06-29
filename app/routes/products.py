from fastapi import APIRouter,Depends,Query,status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.product_schema import ProductCreate,ProductUpdate,ProductResponse,ProductList
from app.services.product_service import create_product_service,get_products_service,get_product_by_id_service,update_product_service,delete_product_service
from app.utils.auth import get_current_user,admin_required
from app.models import User


# product router

router=APIRouter(prefix="/products",tags=["Products"])


# create product

@router.post("/",response_model=ProductResponse,status_code=status.HTTP_201_CREATED)
def create_product(product:ProductCreate,db:Session=Depends(get_db),current_user:User=Depends(admin_required)):
    return create_product_service(product,db)


# get all products

@router.get("/",response_model=ProductList)
def get_products(category:str|None=Query(None),page:int=Query(1,ge=1),limit:int=Query(10,ge=1),db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_products_service(db,category,page,limit)


# get product by id

@router.get("/{product_id}",response_model=ProductResponse)
def get_product(product_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    return get_product_by_id_service(product_id,db)


# update product

@router.put("/{product_id}",response_model=ProductResponse)
def update_product(product_id:int,product:ProductUpdate,db:Session=Depends(get_db),current_user:User=Depends(admin_required)):
    return update_product_service(product_id,product,db)


# delete product

@router.delete("/{product_id}")
def delete_product(product_id:int,db:Session=Depends(get_db),current_user:User=Depends(admin_required)):
    return delete_product_service(product_id,db)