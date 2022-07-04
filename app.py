import json
from urllib.parse import unquote

from chalice import Chalice
import requests
import boto3

app = Chalice(app_name='helloworld')


@app.route('/')
def index():
    try:
        r = requests.get("http://worldtimeapi.org/api/timezone/America/Los_Angeles")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return {"error": e.text}


@app.route('/guess_my_name/{name}')
def guess_secret(name):
    if name:
        secret_name = "test/my_name"
        region_name = "us-west-2"
        secret_value = get_secret_value(secret_name, region_name)
        secret_json = json.loads(secret_value)
        secret_fullname = secret_json["first_name"] + " " + secret_json["last_name"]
        if secret_fullname == unquote(name):
            return {
                "Guess Status": "Correct"
                }
        else:
            return {
                "Guess Status": "Incorrect",
                "Your Guess": name,
                "Correct Answer": secret_fullname
                }
    else:
        return {"error": "Did you forget to guess a name?"}


def get_secret_value(secret_name, region_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret_value = get_secret_value_response['SecretString']
    return secret_value


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
