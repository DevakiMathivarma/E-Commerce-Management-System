from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException,status
from app.models import Cart,CartItem,Product,User
from app.schemas.cart_schema import CartAdd
import logging


# logger

logger=logging.getLogger(__name__)


# add to cart service

def add_to_cart_service(cart_item:CartAdd,current_user:User,db:Session):

    logger.info(f"user {current_user.id} adding product {cart_item.product_id} to cart")

    product=db.query(Product).filter(Product.id==cart_item.product_id).first()

    if not product:
        logger.warning("product not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")

    if not product.is_active:
        logger.warning("inactive product")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="product is inactive")

    if cart_item.quantity>product.stock:
        logger.warning("quantity exceeds stock")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="quantity exceeds available stock")

    cart=db.query(Cart).filter(Cart.user_id==current_user.id).first()

    if not cart:
        logger.info("creating new cart")
        cart=Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    existing_item=db.query(CartItem).filter(CartItem.cart_id==cart.id,CartItem.product_id==cart_item.product_id).first()

    if existing_item:

        if existing_item.quantity+cart_item.quantity>product.stock:
            logger.warning("total quantity exceeds stock")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="quantity exceeds available stock")

        existing_item.quantity+=cart_item.quantity

        logger.info("cart quantity updated")

    else:

        new_item=CartItem(cart_id=cart.id,product_id=cart_item.product_id,quantity=cart_item.quantity)

        db.add(new_item)

        logger.info("new cart item added")

    db.commit()

    return {"message":"product added to cart successfully"}

# get cart service

def get_cart_service(current_user:User,db:Session):

    logger.info(f"fetching cart for user {current_user.id}")

    cart=db.query(Cart).options(joinedload(Cart.cart_items).joinedload(CartItem.product)).filter(Cart.user_id==current_user.id).first()

    if not cart:
        logger.warning("cart not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cart not found")

    items=[]
    total_amount=0

    for item in cart.cart_items:

        if not item.product.is_active:
            continue

        subtotal=item.quantity*item.product.price

        total_amount+=subtotal

        items.append({"product_id":item.product.id,"product_name":item.product.name,"price":item.product.price,"quantity":item.quantity,"subtotal":subtotal})

    logger.info("cart fetched successfully")

    return {"id":cart.id,"user_id":cart.user_id,"total_amount":total_amount,"items":items}


# remove cart item service

def remove_cart_item_service(product_id:int,current_user:User,db:Session):

    logger.info(f"removing product {product_id} from user {current_user.id} cart")

    cart=db.query(Cart).filter(Cart.user_id==current_user.id).first()

    if not cart:
        logger.warning("cart not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cart not found")

    cart_item=db.query(CartItem).filter(CartItem.cart_id==cart.id,CartItem.product_id==product_id).first()

    if not cart_item:
        logger.warning("product not found in cart")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found in cart")

    db.delete(cart_item)

    db.commit()

    logger.info("cart item removed successfully")

    return {"message":"product removed from cart successfully"}