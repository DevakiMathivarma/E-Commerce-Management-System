from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException,status
from app.models import Product
from app.schemas.product_schema import ProductCreate,ProductUpdate
import logging


# logger

logger=logging.getLogger(__name__)


# create product service

def create_product_service(product:ProductCreate,db:Session):

    logger.info("creating product")

    existing_product=db.query(Product).filter(func.lower(Product.name)==product.name.lower()).first()

    if existing_product:
        logger.warning("product already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="product name already exists")

    new_product=Product(name=product.name,description=product.description,price=product.price,stock=product.stock,category=product.category)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    logger.info(f"product created successfully : {new_product.id}")

    return new_product


# get all products service

def get_products_service(db:Session,category:str=None,page:int=1,limit:int=10):

    logger.info("fetching products")

    query=db.query(Product).filter(Product.is_active==True)

    if category:
        query=query.filter(func.lower(Product.category)==category.lower())

    total_records=query.count()

    products=query.offset((page-1)*limit).limit(limit).all()

    logger.info(f"{len(products)} products fetched")

    return {"total_records":total_records,"current_page":page,"limit":limit,"data":products}

# get product by id service

def get_product_by_id_service(product_id:int,db:Session):

    logger.info(f"fetching product : {product_id}")

    product=db.query(Product).filter(Product.id==product_id,Product.is_active==True).first()

    if not product:
        logger.warning("product not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")

    return product


# update product service
def update_product_service(product_id:int,product:ProductUpdate,db:Session):

    logger.info(f"updating product : {product_id}")

    db_product=db.query(Product).filter(Product.id==product_id,Product.is_active==True).first()

    if not db_product:
        logger.warning("product not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")

    existing_product=db.query(Product).filter(func.lower(Product.name)==product.name.lower(),Product.id!=product_id).first()

    if existing_product:
        logger.warning("product name already exists")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="product name already exists")

    for key,value in product.model_dump().items():
        setattr(db_product,key,value)

    db.commit()
    db.refresh(db_product)

    logger.info(f"product updated successfully : {product_id}")

    return db_product


# delete product service

def delete_product_service(product_id:int,db:Session):

    logger.info(f"deleting product : {product_id}")

    product=db.query(Product).filter(Product.id==product_id,Product.is_active==True).first()

    if not product:
        logger.warning("product not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")

    product.is_active=False

    db.commit()

    logger.info(f"product soft deleted : {product_id}")

    return {"message":"product deleted successfully"}