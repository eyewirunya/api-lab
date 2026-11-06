import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Boundary values: 0 and 6 are rejected; 1 and 5 are accepted.
@pytest.mark.parametrize(
    "stars, expected_status",
    [
        (0, 400),
        (1, 200),
        (5, 200),
        (6, 400),
    ],
)
def test_update_rating_boundaries(
    api,
    auth,
    rating,
    stars,
    expected_status,
):
    path = f"/api/ratings/{rating['id']}"

    res = api.put(
        path,
        json={"stars": stars},
        headers=auth,
    )

    assert res.status_code == expected_status

    if expected_status == 200:
        assert res.json()["stars"] == stars
    else:
        res = api.get(path, headers=auth)

        assert res.status_code == 200
        assert res.json()["stars"] == rating["stars"]