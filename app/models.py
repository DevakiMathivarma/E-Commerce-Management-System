# imports

from sqlalchemy import Column,Integer,String,Float,Boolean,DateTime,ForeignKey,Enum,CheckConstraint,UniqueConstraint,Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db import Base


# user role enum

class UserRole(str,enum.Enum):
    ADMIN="Admin"
    CUSTOMER="Customer"


# order status enum

class OrderStatus(str,enum.Enum):
    PENDING="Pending"
    CONFIRMED="Confirmed"
    CANCELLED="Cancelled"
    DELIVERED="Delivered"


# payment status enum

class PaymentStatus(str,enum.Enum):
    PENDING="Pending"
    SUCCESS="Success"
    FAILED="Failed"


# payment method enum

class PaymentMethod(str,enum.Enum):
    CASH="Cash"
    CARD="Card"
    UPI="UPI"
    NETBANKING="NetBanking"


# user model

class User(Base):

    __tablename__="users"

    __table_args__=(UniqueConstraint("email",name="uq_user_email"),Index("idx_user_email","email"))

    id=Column(Integer,primary_key=True,index=True)

    full_name=Column(String(100),nullable=False)

    email=Column(String(150),nullable=False,unique=True,index=True)

    password=Column(String(255),nullable=False)

    role=Column(Enum(UserRole),nullable=False,default=UserRole.CUSTOMER)

    is_active=Column(Boolean,default=True,nullable=False)

    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)

    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    cart=relationship("Cart",back_populates="user",uselist=False,cascade="all,delete")

    orders=relationship("Order",back_populates="customer",cascade="all,delete")


# product model

class Product(Base):

    __tablename__="products"

    __table_args__=(UniqueConstraint("name",name="uq_product_name"),CheckConstraint("price>0",name="check_product_price"),CheckConstraint("stock>=0",name="check_product_stock"),Index("idx_product_name","name"),Index("idx_product_category","category"))

    id=Column(Integer,primary_key=True,index=True)

    name=Column(String(150),nullable=False,unique=True)

    description=Column(String(500),nullable=False)

    price=Column(Float,nullable=False)

    stock=Column(Integer,nullable=False)

    category=Column(String(100),nullable=False,index=True)

    is_active=Column(Boolean,default=True,nullable=False)

    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)

    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    cart_items=relationship("CartItem",back_populates="product")

    order_items=relationship("OrderItem",back_populates="product")

# cart model

class Cart(Base):
    __tablename__="carts"
    __table_args__=(UniqueConstraint("user_id",name="uq_cart_user"),)

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    user=relationship("User",back_populates="cart")
    cart_items=relationship("CartItem",back_populates="cart",cascade="all,delete-orphan")


# cart item model

class CartItem(Base):
    __tablename__="cart_items"
    __table_args__=(UniqueConstraint("cart_id","product_id",name="uq_cart_product"),CheckConstraint("quantity>0",name="check_cart_quantity"))

    id=Column(Integer,primary_key=True,index=True)
    cart_id=Column(Integer,ForeignKey("carts.id",ondelete="CASCADE"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    quantity=Column(Integer,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)

    cart=relationship("Cart",back_populates="cart_items")
    product=relationship("Product",back_populates="cart_items")


# order model

class Order(Base):
    __tablename__="orders"
    __table_args__=(CheckConstraint("total_amount>=0",name="check_total_amount"),Index("idx_order_status","order_status"))

    id=Column(Integer,primary_key=True,index=True)
    customer_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    total_amount=Column(Float,nullable=False,default=0)
    order_status=Column(Enum(OrderStatus),default=OrderStatus.PENDING,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    customer=relationship("User",back_populates="orders")
    order_items=relationship("OrderItem",back_populates="order",cascade="all,delete-orphan")
    payment=relationship("Payment",back_populates="order",uselist=False,cascade="all,delete-orphan")


# order item model

class OrderItem(Base):
    __tablename__="order_items"
    __table_args__=(CheckConstraint("quantity>0",name="check_order_quantity"),CheckConstraint("price>0",name="check_order_price"),CheckConstraint("subtotal>=0",name="check_order_subtotal"))

    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id",ondelete="CASCADE"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    quantity=Column(Integer,nullable=False)
    price=Column(Float,nullable=False)
    subtotal=Column(Float,nullable=False)

    order=relationship("Order",back_populates="order_items")
    product=relationship("Product",back_populates="order_items")


# payment model

class Payment(Base):
    __tablename__="payments"
    __table_args__=(UniqueConstraint("order_id",name="uq_payment_order"),CheckConstraint("amount>0",name="check_payment_amount"),Index("idx_payment_status","payment_status"))

    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey("orders.id",ondelete="CASCADE"),nullable=False)
    amount=Column(Float,nullable=False)
    payment_method=Column(Enum(PaymentMethod),nullable=False)
    payment_status=Column(Enum(PaymentStatus),default=PaymentStatus.PENDING,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    order=relationship("Order",back_populates="payment")