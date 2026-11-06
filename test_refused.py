import uuid


# A second user with an existing username is refused.
def test_duplicate_username(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {
        "username": name,
        "password": "Pizza-2026"
    }

    res = api.post("/api/users", json=user)
    assert res.status_code == 201

    res = api.post("/api/users", json=user)

    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}

# Logging in with a wrong password is refused.
def test_wrong_password(api):
    name = "lab-" + uuid.uuid4().hex[:12]

    user = {
        "username": name,
        "password": "Pizza-2026"
    }

    res = api.post("/api/users", json=user)
    assert res.status_code == 201

    wrong_user = {
        "username": name,
        "password": "Wrong-Password"
    }

    res = api.post(
        "/api/users/token/login",
        json=wrong_user
    )

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}

# A user with an empty username is refused.
def test_empty_username(api):
    user = {
        "username": "",
        "password": "Pizza-2026"
    }

    res = api.post("/api/users", json=user)

    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}

