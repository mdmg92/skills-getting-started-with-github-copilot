from src import app as app_module


def test_get_activities_returns_all(client):
    # Arrange
    expected_activity_names = set(app_module.activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_names


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_success(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    assert email in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in app_module.activities[activity_name]["participants"]


def test_unregister_not_registered_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    assert email not in app_module.activities[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_activity_not_found_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "foo@mergington.edu"

    # Act
    response_signup = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    response_unregister = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response_signup.status_code == 404
    assert response_signup.json()["detail"] == "Activity not found"
    assert response_unregister.status_code == 404
    assert response_unregister.json()["detail"] == "Activity not found"


def test_root_redirects_to_static(client):
    # Arrange - no extra setup needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (301, 307)
    assert response.headers["location"] == "/static/index.html"
