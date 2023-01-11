# `FourCats-Flask`

### Statement

 - `FourCats-Flask` is a module with personal habits based on `Flask` and `Flask-RESTX` encapsulation. The main purpose of encapsulation is to provide a more convenient initialization method for partners.

### Simple Example

#### Init Flask

- The encapsulated flask object package contains JSON serialization processing, which has overloaded the request function.

```python
from fourcats_flask import Flask

flask_app = Flask(__name__)

if __name__ == '__main__':
    flask_app.run(host="localhost", port=5051, debug=True)

```

#### Init All Plug-in

```python
from fourcats_flask import Api
from fourcats_flask import Flask, FlaskInit

flask_app = Flask(__name__)

api = Api(title="Flask Base", description="Flask Base Document", doc="/api/docs")

# create_all - Whether to create a data table through Flask-Sqlalchemy. The default is false.

FlaskInit.register_api(app=flask_app, api=api)
FlaskInit.register_hook(app=flask_app, api=api)
FlaskInit.register_config(configs=["<your_path>/setting"], app=flask_app)
FlaskInit.register_sqlalchemy(app=flask_app, create_all=True)

```

#### Use Token

```python
from fourcats_flask import Token

auth = Token(secret="secret", scheme="JWT", algorithm="H265", message="Authentication failed.")

# with permission
# Using this decorator, the method will be called to execute the corresponding permission processing after the token passes the verification.
@auth.verify_permission
def verify_permission(user):
    # do something
    _ = user
    pass


```

#### About better function

- [Flask](https://flask.palletsprojects.com/en/2.1.x/)
- [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)

### Completion example

Please [click](./example/create_flask.py) to view the completed sample code.
