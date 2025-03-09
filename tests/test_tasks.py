from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Session, StaticPool, create_engine
from tasklist.main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    """Provides an in-memory SQLite database for test fixtures to use.
    A blank database with tables already created is passed to each test
    so tests can assume the database does not contain any tests before
    they run.
    """

    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Provides a testing client to the Task List app for test fixtures to
    use. The database dependency of the app has already been overridden to use
    an in-memory SQLite database.
    """

    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear() 


def test_add_task(client: TestClient):
    """Test that a POST request with a new task succeeds and returns
    the correct fields.
    Input and Output specification taken from Backend Engineer Technical
    Test document.
    """

    request = {
        "title": "Task Title",
        "description": "Task Description",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00"
    }

    expected = {
        "id": 1,
        "title": "Task Title",
        "description": "Task Description",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00",
        "completed": False
    }
    
    response = client.post("/tasks", json=request)
    actual = response.json()

    assert expected == actual

def test_get_missing_task_returns_404(client: TestClient):
    """Test that a GET request for a task ID that doees not exist
    correctly returns a 404 status code
    """

    response = client.get("/tasks/1")
    assert response.status_code == 404

def test_delete_existing_task(client: TestClient):
    """Test that a DELETE request for an existing task returns the
    correct message and also that attempting to GET the deleted task
    results in a 404, indicating it is no longer in the database.
    Message contents taken from Backend Engineer Technical Test document.
    """

    task = {
        "title": "Task Title",
        "description": "Task Description",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00"
    }

    client.post("/tasks/", json=task)
    delete_response = client.delete("/tasks/1")
    delete_result = delete_response.json()
    
    assert delete_result["message"] == "Task deleted successfully."

    get_response = client.get("/tasks/1")
    assert get_response.status_code == 404

def test_get_all_tasks_returns_empty_array(client: TestClient):
    """Test that a GET request to /tasks/ before any tasks have
    been inserted succeeds and returns an empty array.
    """
    response = client.get("/tasks/")
    assert response.status_code == 200

    tasks = response.json()
    assert tasks == []


def test_get_all_tasks(client: TestClient):
    """Test that a GET request to /tasks/ with no further parameters
    returns all tasks.
    """

    client.post("/tasks/", json = {
        "title": "Task 1",
        "description": "First Task",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00"
    })

    client.post("/tasks/", json = {
        "title": "Task 2",
        "description": "Second Task",
        "priority": 2,
        "due_date": "2000-01-30T15:00:00"
    })
    
    response = client.get("/tasks/")
    tasks = response.json()

    assert len(tasks) == 2

def test_get_by_priority(client: TestClient):
    client.post("/tasks/", json = {
        "title": "Task 1",
        "description": "First Task",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00"
    })

    client.post("/tasks/", json = {
        "title": "Task 2",
        "description": "Second Task",
        "priority": 2,
        "due_date": "2000-01-30T15:00:00"
    })
    
    response = client.get("/tasks/?priority=2")
    tasks = response.json()

    assert len(tasks) == 1
    assert tasks[0]["id"] == 2

def test_get_by_completion(client: TestClient):
    client.post("/tasks/", json = {
        "title": "Task 1",
        "description": "First Task",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00"
    })

    client.put("/tasks/1", json={
        "completed": True
    })

    uncompleted_response = client.get("/tasks/?completed=false")
    uncompleted_tasks = uncompleted_response.json()
    assert len(uncompleted_tasks) == 0

    completed_response = client.get("/tasks/?completed=true")
    completed_tasks = completed_response.json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["id"] == 1

