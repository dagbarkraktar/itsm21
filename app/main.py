from flask_restful import Resource, Api

from app_setup import create_app

from modules.monitoring.sensors_data import Sensors
from modules.monitoring.nagios_data import NagiosAggregator
from modules.monitoring.backups_data import Backups
from modules.hwdb.rest import HwUnitsList, HwUnitSingle

app = create_app()
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return dict(hello='Hello from project template!'), 200


api.add_resource(HelloWorld, '/')
api.add_resource(Sensors, '/api/v1/sensors/<int:sensor_id>/')
api.add_resource(NagiosAggregator, '/api/v1/nagios/<int:host_id>/')
api.add_resource(Backups, '/api/v1/backups/')
api.add_resource(HwUnitsList, '/api/v1/hwunits/')
api.add_resource(HwUnitSingle, '/api/v1/hwunits/<int:unit_id>/')

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='', port=8031, debug=True)
