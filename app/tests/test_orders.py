# customer token

def get_customer_token():

    response=client.post("/api/v1/auth/login",json={"email":"customer@gmail.com","password":"Customer@123"})

    return response.json()["access_token"]


# create order

def test_create_order():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/orders/",headers=headers)

    assert response.status_code==201

    data=response.json()

    assert data["customer_id"]>0

    assert data["total_amount"]>0

    assert data["order_status"]=="Confirmed"


# empty cart

def test_create_order_empty_cart():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/orders/",headers=headers)

    assert response.status_code==400

    assert response.json()["detail"]=="cart is empty"


# get all orders

def test_get_orders():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert "data" in data

    assert "total_records" in data

    assert data["current_page"]==1


# get order by id

def test_get_order_by_id():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/1",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert data["id"]==1

    assert "items" in data


# invalid order id

def test_invalid_order():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/999",headers=headers)

    assert response.status_code==404

    assert response.json()["detail"]=="order not found"

# status filter

def test_order_status_filter():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/?status=Confirmed",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert "data" in data


# pagination

def test_order_pagination():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/?page=1&limit=5",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert data["current_page"]==1

    assert data["limit"]==5

    assert "total_records" in data


# invalid status filter

def test_invalid_status_filter():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/?status=InvalidStatus",headers=headers)

    assert response.status_code==400

    assert response.json()["detail"]=="invalid order status"


# unauthorized access

def test_orders_without_token():

    response=client.get("/api/v1/orders/")

    assert response.status_code==401


# another customer cannot access order

def test_other_customer_cannot_access_order():

    client.post("/api/v1/auth/register",json={"full_name":"Customer Two","email":"customer2@gmail.com","password":"Customer@123"})

    response=client.post("/api/v1/auth/login",json={"email":"customer2@gmail.com","password":"Customer@123"})

    token=response.json()["access_token"]

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/1",headers=headers)

    assert response.status_code==404

    assert response.json()["detail"]=="order not found"


# create order without token

def test_create_order_without_token():

    response=client.post("/api/v1/orders/")

    assert response.status_code==401


# invalid pagination

def test_invalid_order_pagination():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/orders/?page=0&limit=0",headers=headers)

    assert response.status_code==422