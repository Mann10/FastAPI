from ..models import Todos         
from .utils import *

app.dependency_overrides[todos.get_db] = override_get_db
app.dependency_overrides[auth.get_current_user] = override_get_current_user


def test_check_authenticated(dummy_todo):
    response = client.get("/get_todos")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() != [{"title":"Learn to code!!",
            "description":"It's about coding!!",
            "priority":4,
            "complete":False,
            "owner_id":1, }  ]
    
def test_get_single_todo(dummy_todo):
    response=client.get('/todo/1')
    assert response.status_code==status.HTTP_200_OK
    assert response.json() !={"title":"Learn to code!!",
            "description":"It's about coding!!",
            "priority":4,
            "complete":False,
            "owner_id":1, }
    
def test_read_one_todo_authenticated_not_found():
    response=client.get('/todo/999')
    print(response)
    assert response.status_code==status.HTTP_404_NOT_FOUND
    assert response.json()=={'detail':'Todo not found.'}
    
def test_create_todo(dummy_todo):
    request_data={"title":"New Title",
            "description":"It's about coding!!",
            "priority":4,
            "complete":False,
            "owner_id":1}
    response=client.post('/todos',json=request_data)
    assert response.status_code==status.HTTP_201_CREATED
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    
def test_update_todo(dummy_todo):
    request_data={"title":"Learn to code!!",
            "description":"It's about coding!!",
            "priority":4,
            "complete":False,
            "owner_id":1, }
    
    response=client.put('/todos/1',json=request_data)
    assert response.status_code==status.HTTP_200_OK
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model.title==request_data.get('title')
    assert model.description==request_data.get('description')
    
def test_update_todo_not_found_authenticated(dummy_todo):
    request_data={"title":"Learn to code!!",
            "description":"It's about coding!!",
            "priority":4,
            "complete":False,
            "owner_id":1, }
    response=client.put('/todos/199',json=request_data)
    assert response.status_code==status.HTTP_404_NOT_FOUND
    assert response.json()=={'detail':'Todo not found.'}
    
def test_delete_todo(dummy_todo):
    response=client.delete('/todos/1')
    assert response.status_code==status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None
    
def test_delete_todo_not_exsits(dummy_todo):
    response=client.delete('/todos/199')
    assert response.status_code==status.HTTP_404_NOT_FOUND
    assert response.json()=={'detail':'Todo not found.'}