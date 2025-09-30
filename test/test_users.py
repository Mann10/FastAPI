from ..routers import users
from .utils import *

app.dependency_overrides[users.get_db]=override_get_db
app.dependency_overrides[auth.get_current_user]==override_get_current_user

def test_authenticated_users_details(dummy_user):
    response=client.get("/users")
    payload=response.json()
    print(payload)
    assert response.status_code==status.HTTP_200_OK
    hashed_passwprd=payload.pop('hashed_passwprd')
    assert bcrypt_context.verify("pass123",hashed_passwprd) == True
    print(payload)
    assert payload=={
        "email":"xyzMike.com",
        "username":"Mike",
        'id':1,
        "first_name":"xyz",
        "last_name":"Mike",
        "is_active":True,
        "role":"",
        "phone_number":'9724663588'
    }
    
def test_change_password_authorized(dummy_user):
    request_data={
        'password':'pass123',
        'new_password':'pass1234'
    }
    response=client.put('/change_password',json=request_data)
    assert response.status_code==status.HTTP_200_OK
    db=TestingSessionLocal()
    user1=db.query(Users).filter(Users.id==1).first()
    assert bcrypt_context.verify("pass1234",user1.hashed_passwprd) == True
    

def test_change_password_authorized_invalid(dummy_user):
    request_data={
        'password':'xyzxyz12341234',
        'new_password':'pass1234'
    }
    response=client.put('/change_password',json=request_data)
    assert response.status_code==status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':'Error on password change'}
    
def test_change_phone_number_authorized(dummy_user):
    response=client.put('/change_number',json={'new_number':'9824663588'})
    response.status_code==status.HTTP_202_ACCEPTED
    