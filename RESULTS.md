# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18
- Step 0.3, status code of the request without a token: 401
- Step 0.4, the name of your pizza: The Clever Marinara
- Step 0.12, results of the three runs without a session (optional): Skipped
- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, 3

## Defect report
- Title: Defect 1: Excluding all three tools returns 500 instead of 400
- Request: POST /api/pizza with excludedTools containing Knife, Pizza cutter and Scissors
- Expected result: 400 Bad Request with a JSON error message
- Actual result: 500 Internal Server Error with an empty response body
- Severity: Medium

## Part A
- Step A4, status codes when the other user reads, changes and deletes: read = 404, update = 400, delete = 400

## Part B

1. API tests can find failures in the real web server and failures in the real interaction with stored data, because they send requests to the running system. A unit test with stubs does not exercise those real components.

   Unit tests with stubs are still useful because they test one function in isolation and can run faster and more independently than API integration tests.

2. Each test creates its own user so that its ratings belong to that test and cannot be changed by another student's test. The public token is shared, so data created with it could be changed by other people.

   I would apply the same idea to the shared shop or hotel in Project 2 by creating or using data owned by my own test and cleaning it up when the test finishes, instead of changing shared data.

3. The tests send requests through one session because the session keeps the cookies returned by the server. QuickPizza uses a load balancer, so keeping the session cookie helps the requests stay with the same server. This makes the tests more reliable. Step 0.12 was skipped.

4. The defect was revealed by the block where all three tools were excluded. QuickPizza returned HTTP 500 with an empty body. This is worse than a 400 with an error message because an application calling the API cannot clearly understand that the request was invalid or why it was rejected.

   The test remains as xfail so that the defect stays visible in the test suite. With strict=True, the test will also alert us when the defect is fixed, so we can remove the xfail marker.

5. Base choice coverage needs 9 tests:

   1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9

   All combinations coverage needs:

   3 × 4 × 2 × 3 = 72 tests.

6. The other user received 404 when reading the rating, 400 when changing it, and 400 when deleting it.

   I would expect all three attempts to be refused with a 4xx status code. The difference between 404 for reading and 400 for changing or deleting is not necessarily a defect, because the important authorization requirement is that the other user cannot access or modify the owner's rating. The API is still refusing all three operations.

7. The request returns HTTP 200 and a JSON list of ratings. Yes, I consider this a security defect because a made-up token can be used to read ratings. On a real system, a stranger who obtained or guessed such a token could read data belonging to other users.

8. An API test checks API status codes, response fields and error responses more directly than a web-page test. A web-page test can check things that the API cannot see, such as whether the user interface displays the correct page, buttons and messages to the user.