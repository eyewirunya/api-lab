# API lab

## How to install

Create and activate a Python virtual environment, then install the required packages:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## How to run the tests

Run the complete test suite with:

```powershell
pytest -v
```

Generate the HTML test report with:

```powershell
pytest -v --html=report.html --self-contained-html
```

## Part A: Input Space Partitioning

### Input Domain Model for POST /api/ratings

| Characteristic | Blocks | Values in the tests |
|---|---|---|
| C1 Value of stars | below 1, 1 to 5 (base), above 5 | 0, 3, 6 |
| C2 Type of stars | whole number (base), decimal, text, no field | 3, 3.5, "3", missing |
| C3 Pizza | exists (base), does not exist | a new pizza, 999999999 |
| C4 Token | the user's own (base), none, wrong | from auth, no header, token length short |

### Base Choice Coverage

The base choice is:

- C1: 3 stars
- C2: whole number
- C3: an existing pizza
- C4: the user's own token

| Characteristic | Block | Test |
|---|---|---|
| C1 Value of stars | below 1 | `test_stars_out_of_range[0]` |
| C1 Value of stars | 1 to 5 (base) | `test_base_choice_is_saved` |
| C1 Value of stars | above 5 | `test_stars_out_of_range[6]` |
| C2 Type of stars | whole number (base) | `test_base_choice_is_saved` |
| C2 Type of stars | decimal | `test_decimal_stars_are_refused` |
| C2 Type of stars | text | `test_text_stars_are_refused` |
| C2 Type of stars | no field | `test_missing_stars_are_refused` |
| C3 Pizza | exists (base) | `test_base_choice_is_saved` |
| C3 Pizza | does not exist | `test_nonexistent_pizza_is_refused` |
| C4 Token | user's own (base) | `test_base_choice_is_saved` |
| C4 Token | none | `test_rating_without_token_is_refused` |
| C4 Token | wrong | `test_rating_with_wrong_token_is_refused` |

Base choice coverage requires 9 tests:

```text
1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9
```

### Boundary Values

For `PUT /api/ratings/{id}`, the boundary values for stars are:

| Stars | Expected status |
|---:|---:|
| 0 | 400 |
| 1 | 200 |
| 5 | 200 |
| 6 | 400 |

Test: `test_update_rating_boundaries`

A refused update must leave the rating unchanged.

### Test Independence

The tests create the data they need through pytest fixtures. Each test gets its own user and rating where required, so tests do not depend on the order in which other tests run.