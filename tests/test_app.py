from fastapi import status


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity: known activity is present
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    email = "tester@example.com"

    # signup
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == status.HTTP_200_OK
    assert "Signed up" in resp.json().get("message", "")

    # verify participant added
    data = client.get("/activities").json()
    assert email in data["Chess Club"]["participants"]

    # duplicate signup should fail
    resp2 = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp2.status_code == status.HTTP_400_BAD_REQUEST

    # unregister
    resp3 = client.post(f"/activities/Chess Club/unregister?email={email}")
    assert resp3.status_code == status.HTTP_200_OK
    data2 = client.get("/activities").json()
    assert email not in data2["Chess Club"]["participants"]


def test_signup_invalid_activity(client):
    resp = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
