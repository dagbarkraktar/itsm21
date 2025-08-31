from flask_restful import Resource, Api
from flask_cors import CORS

from app_setup import create_app

from modules.monitoring.sensors_data import Sensors
from modules.monitoring.nagios_data import NagiosAggregator
from modules.monitoring.backups_data import Backups
from modules.hwdb.rest import (
    HwUnitsList,
    HwUnitSingle,
    HwUnitActionMaintenance,
    HwUnitsFormularList
)
from modules.tickets.rest import (
    TicketsList,
    TicketSingle,
    TicketsPreviewFromExcel,
    TicketsListFormular,
    TicketsNotes
)
from modules.maintenance.rest import (
    MaintenanceRecordsList
)

app = create_app()
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


class HelloWorld(Resource):
    def get(self):
        return dict(hello='Hello from project template!'), 200


api.add_resource(HelloWorld, '/')
api.add_resource(Sensors, '/api/v1/sensors/<int:sensor_id>/')
api.add_resource(NagiosAggregator, '/api/v1/nagios/<int:host_id>/')
api.add_resource(Backups, '/api/v1/backups/')
api.add_resource(HwUnitsList, '/api/v1/hwunits/')
api.add_resource(HwUnitSingle, '/api/v1/hwunits/<int:unit_id>/')
api.add_resource(HwUnitActionMaintenance, '/api/v1/hwunits/<int:unit_id>/action')
api.add_resource(HwUnitsFormularList, '/api/v1/hwunits/formular/')
api.add_resource(TicketsList, '/api/v1/tickets/', methods=['GET', 'POST'])
api.add_resource(TicketSingle, '/api/v1/tickets/<int:ticket_id>/')
api.add_resource(TicketsPreviewFromExcel, '/api/v1/preview_tickets_from_excel/')
api.add_resource(TicketsListFormular, '/api/v1/tickets/formular/')
api.add_resource(TicketsNotes, '/api/v1/tickets/notes/')
api.add_resource(MaintenanceRecordsList, '/api/v1/maintenance/<int:doc_id>/')

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(host='', port=8031, debug=True)
