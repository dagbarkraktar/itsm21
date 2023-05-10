"""Utils and helper functions"""

import requests
from datetime import datetime
import os

# import logging
# import log.log_config

# retrieve logger
# ngs_logger = logging.getLogger('nagios_log')

def get_nagios_status_json_cgi(host, service_description):
    """
    Make request to Nagios Status JSON CGI

    :param host: string hostname
    :param service_description: string monitored service name
    :return: dict
    """

    # TODO: move Nagios auth key to environment setup
    NAGIOS_AUTH_KEY = os.environ.get('NAGIOS_AUTH_KEY') or 'SOME_AUTH_KEY'
    # nagios_headers = {'Authorization': NAGIOS_AUTH_KEY}
    nagios_headers = {'Authorization': 'Basic bmFnaW9zYWRtaW46bmFnaW9z'}

    try:
        nagios_url = f'http://192.168.10.210:8080/nagios/cgi-bin/statusjson.cgi?query=service&formatoptions=enumerate \
        &hostname={host}&servicedescription={service_description}'

        r = requests.get(nagios_url, headers=nagios_headers, timeout=5)
        # TODO: check r.status_code here

        # parse JSON from Response object and return dict
        return r.json()  # May raise ValueError

    except Exception as e:
        # TODO: log and process exception message here
        print('Request error! (service) ' + str(e))
        # ngs_logger.error(f'Request error! (service) {e}')
        # return empty dict if some errors occurs
        return {}


# sample perf_data strings
# perf_data_hdd_sample = ''c:\\ Used Space'=32.54Gb;79.92;89.91;0.00;99.90'
# perf_data_ping_sample = 'rta=0.528000ms;100.000000;500.000000;0.000000 pl=0%;20;60;0'
# perf_data_memory_usage_sample = ''Memory usage'=1178.88MB;2750.08;3093.84;0.00;3437.60'
# perf_data_cpu_load_sample = ''5 min avg Load'=7%;80;90;0;100'
# perf_data_uptime_sample = 'uptime=25052'  # uptime in hours


def parse_hdd_perf_data(perf_data_str):
    """
    Parse HDD perf_data parameters from Nagios json-cgi response

    :param perf_data_str: string with perf_data
    :return: total space, used space in GB (parsed from perf_data string)
    """
    # Sample perf_data: ''c:\\ Used Space'=32.54Gb;79.92;89.91;0.00;99.90'

    try:
        perf_data_list = perf_data_str.split('=')[1].split(';')
        hdd_used = float(perf_data_list[0][:-2])
        hdd_total = float(perf_data_list[4])

        return hdd_total, hdd_used

    except Exception as e:

        # TODO: log and process exception message here
        # return 0.0 if some error occurs
        return 0.0, 0.0


def parse_ping_perf_data(perf_data_str):
    """
    Parse PING perf_data parameters from Nagios json-cgi response

    :param perf_data_str: string with perf_data
    :return: ping in ms, packet loss %
    """
    # Sample perf_data: 'rta=0.528000ms;100.000000;500.000000;0.000000 pl=0%;20;60;0'

    try:
        perf_data_list = perf_data_str.split('=')
        ping_ms = float(perf_data_list[1].split(';')[0][:-2])
        ping_packet_loss = float(perf_data_list[2].split(';')[0][:-1])

        return ping_ms, ping_packet_loss

    except Exception as e:

        # TODO: log and process exception message here
        # return 0.0 if some error occurs
        return 0.0, 0.0


def parse_mem_use_perf_data(perf_data_str):
    """
    Parse memory usage perf_data parameters from Nagios json-cgi response

    :param perf_data_str: string with perf_data
    :return: memory total, memory used in MB
    """
    # Sample perf_data: ''Memory usage'=1178.88MB;2750.08;3093.84;0.00;3437.60'

    try:
        perf_data_list = perf_data_str.split('=')[1].split(';')
        mem_used = float(perf_data_list[0][:-2])
        mem_total = float(perf_data_list[4])

        return mem_total, mem_used

    except Exception as e:

        # TODO: log and process exception message here
        # return 0.0 if some error occurs
        return 0.0, 0.0


def parse_cpu_load_perf_data(perf_data_str):
    """
    Parse CPU Load perf_data parameters from Nagios json-cgi response

    :param perf_data_str: string with perf_data
    :return: cpu load in percent
    """
    # Sample perf_data: ''5 min avg Load'=7%;80;90;0;100'

    try:
        perf_data_list = perf_data_str.split('=')[1].split(';')
        cpu_load = int(perf_data_list[0][:-1])

        return cpu_load

    except Exception as e:

        # TODO: log and process exception message here
        # return 0.0 if some error occurs
        return 0


def parse_uptime_perf_data(perf_data_str):
    """
    Parse Uptime perf_data parameters from Nagios json-cgi response

    :param perf_data_str: string with perf_data
    :return: uptime im hours
    """
    # Sample perf_data: 'uptime=25052'

    try:
        uptime_hours = int(perf_data_str.split('=')[1])

        return uptime_hours

    except Exception as e:

        # TODO: log and process exception message here
        # return 0.0 if some error occurs
        return 0


def parse_nagios_time(nagios_timestamp):
    """ Convert Nagios timestamp string to datetime """

    timestamp = int(nagios_timestamp) / 1000  # strip unnecessary 1k
    datetime_local = datetime.utcfromtimestamp(timestamp + 10800)  # +3 hours for local tz

    return datetime_local

