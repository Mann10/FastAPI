from .utils import *
from ..routers import auth
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException
import pytest



app.dependency_overrides[auth.get_db]=override_get_db
app.dependency_overrides[auth.get_current_user]=override_get_current_user



def test_authenticate_user(dummy_user):
    db=TestingSessionLocal()
    authenticated_user=auth.authenticate(dummy_user.username,'pass123',db)
    
    assert authenticated_user is not None
    assert authenticated_user.username==dummy_user.username
    
    non_exsisting_user=auth.authenticate('MIKEY','pass12345',db)
    assert non_exsisting_user is False
    
    wrong_user_pass=auth.authenticate(dummy_user.username,'pass1234567',db)
    assert wrong_user_pass is False
    
def test_create_access_token(dummy_user):
    username=dummy_user.username
    user_id=dummy_user.id
    role=dummy_user.role
    expire_delta=timedelta(days=1)
    
    token=auth.create_access_token(username,user_id=user_id,role=role,expires_delta=expire_delta)
    decode_token=jwt.decode(token,auth.SECRET_KEY,auth.ALGORITHM)
    assert decode_token['sub']==username
    assert decode_token['id']==user_id
    assert decode_token['role']==role
    
@pytest.mark.asyncio    
async def test_get_current_user():
    encode={
        'sub':'username',
        'id':1,
        'role':'admin'
    }
    token=jwt.encode(encode,auth.SECRET_KEY,auth.ALGORITHM)
    user = await auth.get_current_user(token)
    
    assert user == {
            'username':'username',
            'id':1,
            'user_role':'admin'
        }

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode={
        'role':'admin'
    }
    token=jwt.encode(encode,auth.SECRET_KEY,auth.ALGORITHM)
    
    with pytest.raises(HTTPException) as exceinfo:
        await auth.get_current_user(token=token)
        
    assert exceinfo.value.status_code==401
    assert exceinfo.value.detail == 'Could not validate user.'