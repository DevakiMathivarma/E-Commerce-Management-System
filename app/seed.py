import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db import SessionLocal
from app.models import User,Product,Cart,CartItem,Order,OrderItem,Payment,UserRole,OrderStatus,PaymentMethod,PaymentStatus
from app.utils.hash import hash_password


db=SessionLocal()


# admin

admin=db.query(User).filter(User.email=="admin@gmail.com").first()

if not admin:
    admin=User(full_name="Admin",email="admin@gmail.com",password=hash_password("Admin@123"),role=UserRole.ADMIN,is_active=True)
    db.add(admin)


# customer

customer=db.query(User).filter(User.email=="john@gmail.com").first()

if not customer:
    customer=User(full_name="John Doe",email="john@gmail.com",password=hash_password("John@123"),role=UserRole.CUSTOMER,is_active=True)
    db.add(customer)

db.commit()
db.refresh(customer)


# products

if db.query(Product).count()==0:

    laptop=Product(name="Laptop",description="Gaming Laptop",price=75000,stock=10,category="Electronics",is_active=True)

    keyboard=Product(name="Keyboard",description="Mechanical Keyboard",price=2500,stock=20,category="Electronics",is_active=True)

    mouse=Product(name="Mouse",description="Wireless Mouse",price=1200,stock=30,category="Electronics",is_active=True)

    monitor=Product(name="Monitor",description="24 Inch Monitor",price=15000,stock=8,category="Electronics",is_active=True)

    chair=Product(name="Office Chair",description="Ergonomic Chair",price=8000,stock=5,category="Furniture",is_active=True)

    db.add_all([laptop,keyboard,mouse,monitor,chair])

    db.commit()


products=db.query(Product).all()


# cart

cart=db.query(Cart).filter(Cart.user_id==customer.id).first()

if not cart:

    cart=Cart(user_id=customer.id)

    db.add(cart)

    db.commit()

    db.refresh(cart)


# cart items

if db.query(CartItem).count()==0:

    db.add(CartItem(cart_id=cart.id,product_id=products[0].id,quantity=1))

    db.add(CartItem(cart_id=cart.id,product_id=products[1].id,quantity=2))

    db.commit()


# order

order=db.query(Order).first()

if not order:

    total=products[0].price+(products[1].price*2)

    order=Order(customer_id=customer.id,total_amount=total,order_status=OrderStatus.CONFIRMED)

    db.add(order)

    db.commit()

    db.refresh(order)

    db.add(OrderItem(order_id=order.id,product_id=products[0].id,quantity=1,price=products[0].price,subtotal=products[0].price))

    db.add(OrderItem(order_id=order.id,product_id=products[1].id,quantity=2,price=products[1].price,subtotal=products[1].price*2))

    db.commit()


# payment

payment=db.query(Payment).filter(Payment.order_id==order.id).first()

if not payment:

    payment=Payment(order_id=order.id,amount=order.total_amount,payment_method=PaymentMethod.UPI,payment_status=PaymentStatus.SUCCESS)

    db.add(payment)

    db.commit()


db.close()

