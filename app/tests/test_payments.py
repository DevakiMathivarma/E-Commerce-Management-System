# customer token

def get_customer_token():

    response=client.post("/api/v1/auth/login",json={"email":"customer@gmail.com","password":"Customer@123"})

    return response.json()["access_token"]


# create payment

def test_create_payment():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/payments/1",headers=headers,json={"amount":80000,"payment_method":"UPI"})

    assert response.status_code==201

    data=response.json()

    assert data["order_id"]==1

    assert data["amount"]==80000

    assert data["payment_method"]=="UPI"

    assert data["payment_status"]=="Success"


# duplicate payment

def test_duplicate_payment():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/payments/1",headers=headers,json={"amount":80000,"payment_method":"UPI"})

    assert response.status_code==400

    assert response.json()["detail"]=="payment already completed"


# invalid payment amount

def test_invalid_payment_amount():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/payments/1",headers=headers,json={"amount":1000,"payment_method":"UPI"})

    assert response.status_code==400

    assert response.json()["detail"]=="payment amount must match order amount"


# invalid order id

def test_invalid_order_payment():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/payments/999",headers=headers,json={"amount":1000,"payment_method":"UPI"})

    assert response.status_code==404

    assert response.json()["detail"]=="order not found"

# get payment by id

def test_get_payment_by_id():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/payments/1",headers=headers)

    assert response.status_code==200

    data=response.json()

    assert data["id"]==1

    assert data["payment_status"]=="Success"


# payment not found

def test_payment_not_found():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/payments/999",headers=headers)

    assert response.status_code==404

    assert response.json()["detail"]=="payment not found"


# payment without token

def test_payment_without_token():

    response=client.get("/api/v1/payments/1")

    assert response.status_code==401


# another customer cannot access payment

def test_other_customer_cannot_access_payment():

    client.post("/api/v1/auth/register",json={"full_name":"Customer Two","email":"customer2@gmail.com","password":"Customer@123"})

    response=client.post("/api/v1/auth/login",json={"email":"customer2@gmail.com","password":"Customer@123"})

    token=response.json()["access_token"]

    headers={"Authorization":f"Bearer {token}"}

    response=client.get("/api/v1/payments/1",headers=headers)

    assert response.status_code==404

    assert response.json()["detail"]=="payment not found"


# another customer cannot pay another user's order

def test_other_customer_cannot_pay_order():

    response=client.post("/api/v1/auth/login",json={"email":"customer2@gmail.com","password":"Customer@123"})

    token=response.json()["access_token"]

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/payments/1",headers=headers,json={"amount":80000,"payment_method":"UPI"})

    assert response.status_code==403

    assert response.json()["detail"]=="you can pay only for your own orders"


# invalid payment amount validation

def test_payment_zero_amount():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/payments/1",headers=headers,json={"amount":0,"payment_method":"UPI"})

    assert response.status_code in [400,422]


# invalid payment method

def test_invalid_payment_method():

    token=get_customer_token()

    headers={"Authorization":f"Bearer {token}"}

    response=client.post("/api/v1/payments/1",headers=headers,json={"amount":80000,"payment_method":"BITCOIN"})

    assert response.status_code==422