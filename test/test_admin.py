from .utils import *
from ..routers import admin


app.dependency_overrides[admin.get_db]=override_get_db
app.dependency_overrides[admin.get_current_user]=override_get_current_user


def test_admin_todos(dummy_todo):
    response=client.get('/todos')
    assert response.status_code==status.HTTP_200_OK
    print(response.json())
    assert response.json()== [{"title":"Learn to code!!",
            "description":"It's about coding!!",
            "priority":4,
            "complete":False,
            'id': 1,
            "owner_id":1, }]
    
def test_admin_delete_todos(dummy_todo):
    response=client.delete('/admin/1')
    assert response.status_code==status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    model=db.query(Todos).filter(Todos.id==1).first()
    assert model is None
    
def test_admin_delete_todo_not_exists(dummy_todo):
    reponse=client.delete('/admin/199')
    assert reponse.status_code==status.HTTP_404_NOT_FOUND
    assert reponse.json()=={'detail':'Todo not found.'}