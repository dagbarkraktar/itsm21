from flask_restful import Resource, Api

from app_setup import create_app

from modules.monitoring.sensors_data import Sensors
from modules.monitoring.nagios_data import NagiosAggregator
from modules.monitoring.backups_data import Backups

app = create_app()
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return dict(hello='Hello from project template!'), 200


api.add_resource(HelloWorld, '/')
api.add_resource(Sensors, '/api/v1/sensors/<int:sensor_id>')
api.add_resource(NagiosAggregator, '/api/v1/nagios/<int:host_id>')
api.add_resource(Backups, '/api/v1/backups')

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='', port=8031, debug=True)
