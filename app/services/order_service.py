from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException,status
from app.models import Cart,CartItem,Order,OrderItem,Product,User,OrderStatus
import logging


# logger

logger=logging.getLogger(__name__)


# create order service

def create_order_service(current_user:User,db:Session):

    logger.info(f"creating order for user {current_user.id}")

    cart=db.query(Cart).options(joinedload(Cart.cart_items).joinedload(CartItem.product)).filter(Cart.user_id==current_user.id).first()

    if not cart:
        logger.warning("cart not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cart not found")

    if not cart.cart_items:
        logger.warning("cart is empty")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="cart is empty")

    total_amount=0

    for item in cart.cart_items:

        if not item.product:
            logger.warning("product not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")

        if not item.product.is_active:
            logger.warning("inactive product")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{item.product.name} is inactive")

        if item.quantity>item.product.stock:
            logger.warning("insufficient stock")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"insufficient stock for {item.product.name}")

        total_amount+=item.quantity*item.product.price

    order=Order(customer_id=current_user.id,total_amount=total_amount,order_status=OrderStatus.CONFIRMED)

    db.add(order)
    db.flush()

    logger.info(f"order created : {order.id}")

    for item in cart.cart_items:

        subtotal=item.quantity*item.product.price

        order_item=OrderItem(order_id=order.id,product_id=item.product.id,quantity=item.quantity,price=item.product.price,subtotal=subtotal)

        db.add(order_item)

        item.product.stock-=item.quantity

        db.delete(item)

    db.commit()

    db.refresh(order)

    logger.info(f"order placed successfully : {order.id}")

    return order

# get orders service

def get_orders_service(current_user:User,db:Session,status_filter:str=None,page:int=1,limit:int=10):

    logger.info(f"fetching orders for user {current_user.id}")

    query=db.query(Order).options(joinedload(Order.order_items).joinedload(OrderItem.product)).filter(Order.customer_id==current_user.id)

    if status_filter:
        try:
            status_enum=OrderStatus(status_filter.capitalize())
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid order status")
    query=query.filter(Order.order_status==status_enum)

    total_records=query.count()

    orders=query.offset((page-1)*limit).limit(limit).all()

    data=[]

    for order in orders:

        items=[]

        for item in order.order_items:
            items.append({"product_id":item.product_id,"product_name":item.product.name,"price":item.price,"quantity":item.quantity,"subtotal":item.subtotal})

        data.append({"id":order.id,"customer_id":order.customer_id,"total_amount":order.total_amount,"order_status":order.order_status,"items":items})

    logger.info(f"{len(data)} orders fetched")

    return {"total_records":total_records,"current_page":page,"limit":limit,"data":data}


# get order by id service

def get_order_by_id_service(order_id:int,current_user:User,db:Session):

    logger.info(f"fetching order {order_id}")

    order=db.query(Order).options(joinedload(Order.order_items).joinedload(OrderItem.product)).filter(Order.id==order_id,Order.customer_id==current_user.id).first()

    if not order:
        logger.warning("order not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="order not found")

    items=[]

    for item in order.order_items:
        items.append({"product_id":item.product_id,"product_name":item.product.name,"price":item.price,"quantity":item.quantity,"subtotal":item.subtotal})

    logger.info(f"order {order_id} fetched successfully")

    return {"id":order.id,"customer_id":order.customer_id,"total_amount":order.total_amount,"order_status":order.order_status,"items":items}