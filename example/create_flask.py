#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# TIME ： 2022-07-21
from flask_cors import CORS
from flask_restx import Namespace, Resource

from fourcats_flask import Api
from fourcats_flask import Token
from fourcats_flask import Argument
from fourcats_flask import RequestParser
from fourcats_flask import Flask, FlaskInit
from fourcats_flask import CreateSuccess, UpdateSuccess, GainSuccess, DeleteSuccess

flask_app = Flask(__name__)
CORS(flask_app)

api = Api(title="Flask Base", description="Flask Base Document", doc="/api/docs")

auth = Token(secret="1")
api.init_app(flask_app)
FlaskInit.register_hook(app=flask_app, api=api)

test_api = Namespace("Test", description="Testing")


@auth.verify_permission
def verify_permission(user):
    print(123)
    print(user)
    return


@test_api.route("/<int:pid>")
class TestView(Resource):
    """"""

    parser_post = RequestParser(argument_class=Argument)
    parser_post.add_argument(name="a", type=str, location=('json', 'form',), help="A", required=True)
    parser_post.add_argument(name="b", type=str, location=('json', 'form',), help="B", required=True)
    parser_post.add_argument(name="c", type=str, location=("args",), help="C", required=True)
    # parser_post.add_argument(name="file", type=FileStorage, location="files", help="C", required=True)

    parser_put = RequestParser(argument_class=Argument)
    parser_put.add_argument(name="a", type=str, location=('json', 'form',), help="A", required=True)
    parser_put.add_argument(name="b", type=str, location=('json', 'form',), help="B", required=True)
    parser_put.add_argument(name="c", type=str, location=("args",), help="C", required=True)

    parser_patch = RequestParser(argument_class=Argument)
    parser_patch.add_argument(name="a", type=str, location=('json', 'form',), help="A")
    parser_patch.add_argument(name="b", type=str, location=('json', 'form',), help="B")
    parser_patch.add_argument(name="c", type=str, location=("args",), help="C")

    parser_get = RequestParser(argument_class=Argument)
    parser_get.add_argument(name="a", type=str, location=("args",), help="A")
    parser_get.add_argument(name="b", type=str, location=("args",), help="B")
    parser_get.add_argument(name="c", type=str, location=("args",), help="C")

    parser_delete = RequestParser(argument_class=Argument)
    parser_delete.add_argument(name="a", type=str, location=("args",), help="A")
    parser_delete.add_argument(name="b", type=str, location=("args",), help="B")
    parser_delete.add_argument(name="c", type=str, location=("args",), help="C")

    # @auth.auth.login_required
    @test_api.expect(parser_post)
    def post(self, pid):
        """
        Testing POST
        :return:
        """
        params = self.parser_post.parse_args()
        params["pid"] = pid
        params.pop("file", "")
        return CreateSuccess(data=params)

    @test_api.expect(parser_put)
    def put(self, pid):
        """
        Testing PUT
        :return:
        """
        print(auth.generate_token())
        params = self.parser_put.parse_args()
        params["pid"] = pid
        return UpdateSuccess(data=params)

    @test_api.expect(parser_patch)
    def patch(self, pid):
        """
        Testing PATCH
        :return:
        """
        params = self.parser_put.parse_args()
        params["pid"] = pid
        return UpdateSuccess(data=params)

    @test_api.expect(parser_get)
    def get(self, pid):
        """
        Testing GET
        :return:
        """
        params = self.parser_get.parse_args()
        params["pid"] = pid
        return GainSuccess(data=params)

    @test_api.expect(parser_delete)
    def delete(self, pid):
        """
        Testing DELETE
        :return:
        """
        params = self.parser_delete.parse_args()
        params["pid"] = pid
        return DeleteSuccess(data=params)


api.add_namespace(test_api, path="/api/test")

if __name__ == '__main__':
    flask_app.run(host="localhost", port=5051, debug=True)
