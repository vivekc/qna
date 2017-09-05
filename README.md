The Columns for Question, Answer, User and Tenant Table is as follows:
Question table consist of columns Title, private, user_id
Answer table consist of columns body, question_id, user_id
Tenant table consist of name and api_key
User table consist of name
# Populate the fake data in all tables using any library available in python/Django or any other framework.
# Accomplish the following tasks using Django or any other framework in python:

·  Add a RESTful, read-only API to allow consumers to retrieve Questions with Answers as JSON (no need to retrieve Answers on their own). The response should include Answers inside their Question as well as include the id and name of the Question and Answer users.
·  Don't return private Questions in the API response.
·  Require every API request to include a valid Tenant API key, and return an HTTP code of your choice if the request does not include a valid key.
·  Track API request counts per Tenant.
·  Add an HTML dashboard page as the root URL that shows the total number of Users, Questions, and Answers in the system, as well as Tenant API request counts for all Tenants. Style it enough to not assault a viewer's sensibilities.
·  Add tests around the code you write as you deem appropriate. Assume that the API cannot be changed once it's released and test accordingly.
·  You are welcome to add any models or other code you think you need, as well as any gems.
·  Allow adding a query parameter to the API request to select only Questions that contain the query term(s). Return an appropriate HTML status code if no results are found.
·  Add a piece of middleware to throttle API requests on a per-Tenant basis. After the first 100 requests per day, throttle to 1 request per 10 seconds.
·  Use git as SCM tool and commit the code with proper commit messages

# Populated data:
1. Added data using django admin interface and
2. python manage.py dumpdata qa |  python -m json.tool > qa/fixtures/initial.json

# How to Setup:
1. pip install -r requirements.txt
2. Change database credentials in settings.py
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py loaddata qa/fixtures/initial.json
6. python manage.py runserver
7. http://localhost:8000