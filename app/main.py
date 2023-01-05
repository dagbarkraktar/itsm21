from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return dict(hello="Hello from project template!"), 200


api.add_resource(HelloWorld, '/')

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="", port=8031, debug=True)
