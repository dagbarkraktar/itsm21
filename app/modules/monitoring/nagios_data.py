from flask import jsonify
from flask_restful import Resource

from modules.monitoring import nagios_utils

import logging
# import log.log_config

# some constants
SRV_PING = 0
HDD_DISK_C = 1
HDD_DISK_D = 2
HDD_DISK_E = 3
SRV_MEM_USAGE = 4
SRV_CPU_LOAD = 5
SRV_UPTIME = 6

MAX_SERVER_ID = 5

hosts = ['ASU-1', 'SERVER1', 'BUH-NEWSRV', 'GLAS', 'DELL420', 'VOSTOK1']
services = [
            'PING',
            'Drive Space C:',
            'Drive Space D:',
            'Drive Space E:',
            'Memory Usage',
            'CPU Load',
            'Uptime'
            ]

# hosts_services = {
#     'ASU-1':['PING','Drive Space C:','Drive Space D:'],
#     'SERVER1':['PING','Drive Space C:','Drive Space D:'],
#     'GLAS':['PING','Drive Space C:','Drive Space D:']
# }

ngs_logger = logging.getLogger('nagios_log')


class NagiosAggregator(Resource):
    """ Endpoint '/api/v1/nagios/<int:host_id>' implementation """

    def get(self, host_id):

        if host_id > MAX_SERVER_ID:
            return {'message': 'Unknown server id!'}, 404

        response = {}
        storage_data = []
        services_data = []

        # Get monitoring data
        # storage
        storage_data.append(get_nagios_service_data(host_id, HDD_DISK_C))
        storage_data.append(get_nagios_service_data(host_id, HDD_DISK_D))
        storage_data.append(get_nagios_service_data(host_id, HDD_DISK_E))
        # ping, memory usage, CPU load, uptime
        services_data.append(get_nagios_service_data(host_id, SRV_PING))
        services_data.append(get_nagios_service_data(host_id, SRV_MEM_USAGE))
        services_data.append(get_nagios_service_data(host_id, SRV_CPU_LOAD))
        services_data.append(get_nagios_service_data(host_id, SRV_UPTIME))

        response['server_name'] = hosts[host_id]
        response['storage'] = storage_data
        response['services'] = services_data

        return jsonify(response)


def get_nagios_service_data(host_id, service_id):
    """
    Selects from Nagios response desired data and returns it as dict

    :param host_id: Id of monitored host
    :param service_id: Id of monitored service on this host
    :return: dict with desired monitoring data
    """

    nagios_response = nagios_utils.get_nagios_status_json_cgi(hosts[host_id], services[service_id])

    try:
        result_message = nagios_response['result']['type_text']
        # TODO: Add debug logging
        # print(f'Request result: {result_message} ({services[service_id]})')
        ngs_logger.debug(f'Request: {result_message}, Host: {hosts[host_id]} ({services[service_id]})')
        service_dict = {}
        if result_message == 'Success':
            # save service name
            service_dict['name'] = services[service_id]
            # save last update datetime
            service_dict['lastupdate'] = nagios_utils.parse_nagios_time(nagios_response['result']['last_data_update'])
            # save service status
            service_dict['status'] = nagios_response['data']['service']['status']

            perf_data = nagios_response['data']['service']['perf_data']

            # parse perf_data for HDD
            if 'Drive' in services[service_id]:
                hdd_total, hdd_used = nagios_utils.parse_hdd_perf_data(perf_data)
                service_dict['total'] = hdd_total
                service_dict['used'] = hdd_used
                service_dict['free'] = round(hdd_total-hdd_used, 2)
            # parse perf_data for PING
            if 'PING' in services[service_id]:
                ping_ms, ping_packet_loss = nagios_utils.parse_ping_perf_data(perf_data)
                service_dict['ping_ms'] = ping_ms
                service_dict['ping_packet_loss'] = ping_packet_loss
            # parse perf_data for MEMORY USAGE
            if 'Memory' in services[service_id]:
                mem_total, mem_used = nagios_utils.parse_mem_use_perf_data(perf_data)
                service_dict['total'] = mem_total
                service_dict['used'] = mem_used
                service_dict['free'] = round(mem_total-mem_used,2)
            # parse perf_data for CPU LOAD
            if 'CPU' in services[service_id]:
                cpu_load = nagios_utils.parse_cpu_load_perf_data(perf_data)
                service_dict['cpu_load'] = cpu_load
            # parse perf_data for UPTIME
            if 'Uptime' in services[service_id]:
                uptime = nagios_utils.parse_uptime_perf_data(perf_data)
                service_dict['uptime'] = uptime

            # return monitoring data
            return service_dict

        return {}

    except Exception as e:
        # TODO: log and process exception message here
        # print('Get Nagios data error! ' + str(e))
        ngs_logger.error(f'Get Nagios data error! {e}')
        # return empty dict if some errors occurs
        return {}
