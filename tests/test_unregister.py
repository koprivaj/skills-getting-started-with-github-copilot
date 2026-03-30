from src.app import activities


def test_unregister_removes_participant(client):
    email = activities["Chess Club"]["participants"][0]

    response = client.delete("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete("/activities/Unknown Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant_returns_404(client):
    response = client.delete("/activities/Chess Club/signup", params={"email": "not.registered@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
