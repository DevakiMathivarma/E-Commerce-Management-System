import pytest
from app.models import UserRole


# admin token

def get_admin_token():

    client.post("/api/v1/auth/register",json={"full_name":"Admin","email":"admin@gmail.com","password":"Admin@123"})

    db=TestingSessionLocal()

    admin=db.query(User).filter(User.email=="admin@gmail.com").first()

    admin.role=UserRole.ADMIN

    db.commit()

    db.close()

    response=client.post("/api/v1/auth/login",json={"email":"admin@gmail.com","password":"Admin@123"})

    return response.json()["access_token"]


# customer token

def get_customer_token():

    client.post("/api/v1/auth/register",json={"full_name":"Customer","email":"customer@gmail.com","password":"Customer@123"})

    response=client.post("/api/v1/auth/login",json={"email":"customer@gmail.com","password":"Customer@123"})

    return response.json()["access_token"]


# create product

def test_create_product():

    token=get_admin_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/products/",headers=headers,json={"name":"Laptop","description":"Gaming Laptop","price":75000,"stock":10,"category":"Electronics"})

    assert response.status_code==201

    data=response.json()

    assert data["name"]=="Laptop"

    assert data["price"]==75000

    assert data["stock"]==10

    assert data["category"]=="Electronics"


# duplicate product

def test_duplicate_product():

    token=get_admin_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/products/",headers=headers,json={"name":"Laptop","description":"Gaming Laptop","price":70000,"stock":5,"category":"Electronics"})

    assert response.status_code==400

    assert response.json()["detail"]=="product name already exists"


# get all products

def test_get_products():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/products/",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert "data" in data

    assert "total_records" in data

    assert data["current_page"]==1


# get product by id

def test_get_product_by_id():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/products/1",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert data["id"]==1

    assert data["name"]=="Laptop"

# update product

def test_update_product():

    token=get_admin_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.put("/api/v1/products/1",headers=headers,json={"name":"Laptop Updated","description":"Updated Laptop","price":80000,"stock":15,"category":"Electronics","is_active":True})

    assert response.status_code==200

    data=response.json()

    assert data["name"]=="Laptop Updated"

    assert data["price"]==80000

    assert data["stock"]==15


# soft delete product

def test_delete_product():

    token=get_admin_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.delete("/api/v1/products/1",headers=headers)

    assert response.status_code==200

    assert response.json()["message"]=="product deleted successfully"


# pagination

def test_product_pagination():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/products/?page=1&limit=5",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert data["current_page"]==1

    assert data["limit"]==5

    assert "total_records" in data


# category filter

def test_product_category_filter():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/products/?category=Electronics",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert "data" in data


# customer cannot create product

def test_customer_cannot_create_product():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/products/",headers=headers,json={"name":"Phone","description":"Smart Phone","price":25000,"stock":10,"category":"Electronics"})

    assert response.status_code==403

    assert response.json()["detail"]=="admin access required"


# customer cannot update product

def test_customer_cannot_update_product():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.put("/api/v1/products/1",headers=headers,json={"name":"Phone","description":"Phone","price":25000,"stock":5,"category":"Electronics","is_active":True})

    assert response.status_code==403

    assert response.json()["detail"]=="admin access required"


# customer cannot delete product

def test_customer_cannot_delete_product():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.delete("/api/v1/products/1",headers=headers)

    assert response.status_code==403

    assert response.json()["detail"]=="admin access required"


# invalid product id

def test_invalid_product():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/products/999",headers=headers)

    assert response.status_code==404

    assert response.json()["detail"]=="product not found"