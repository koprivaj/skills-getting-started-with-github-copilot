from src.app import activities


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_returns_400(client):
    existing_email = activities["Chess Club"]["participants"][0]

    response = client.post("/activities/Chess Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_full_activity_returns_400(client):
    max_participants = activities["Chess Club"]["max_participants"]
    activities["Chess Club"]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]

    response = client.post("/activities/Chess Club/signup", params={"email": "extra@mergington.edu"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
