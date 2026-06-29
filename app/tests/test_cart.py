# customer token

def get_customer_token():

    response=client.post("/api/v1/auth/login",json={"email":"customer@gmail.com","password":"Customer@123"})

    return response.json()["access_token"]


# add to cart

def test_add_to_cart():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/cart/add",headers=headers,json={"product_id":1,"quantity":2})

    assert response.status_code==201

    assert response.json()["message"]=="product added to cart successfully"


# product not found

def test_add_invalid_product():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/cart/add",headers=headers,json={"product_id":999,"quantity":1})

    assert response.status_code==404

    assert response.json()["detail"]=="product not found"


# inactive product

def test_add_inactive_product():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/cart/add",headers=headers,json={"product_id":2,"quantity":1})

    assert response.status_code==400

    assert response.json()["detail"]=="product is inactive"


# quantity greater than stock

def test_quantity_exceeds_stock():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/cart/add",headers=headers,json={"product_id":1,"quantity":1000})

    assert response.status_code==400

    assert response.json()["detail"]=="quantity exceeds available stock"


# update existing cart item

def test_update_cart_quantity():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/cart/add",headers=headers,json={"product_id":1,"quantity":1})

    assert response.status_code==201

    assert response.json()["message"]=="product added to cart successfully"


# get cart

def test_get_cart():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/cart",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert "items" in data

    assert "total_amount" in data

    assert data["user_id"]>0


# remove cart item

def test_remove_cart_item():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.delete("/api/v1/cart/remove/1",headers=headers)

    assert response.status_code==200

    assert response.json()["message"]=="product removed from cart successfully"


# remove invalid product

def test_remove_invalid_cart_item():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.delete("/api/v1/cart/remove/999",headers=headers)

    assert response.status_code==404

    assert response.json()["detail"]=="product not found in cart"


# empty cart

def test_empty_cart():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    client.delete("/api/v1/cart/remove/1",headers=headers)

    response=client.get("/api/v1/cart",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert data["items"]==[]

    assert data["total_amount"]==0


# unauthorized access

def test_cart_without_token():

    response=client.get("/api/v1/cart")

    assert response.status_code==401

    assert response.json()["detail"]=="Not authenticated"
