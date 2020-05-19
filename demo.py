import logging
from ipaddress import ip_interface
# Import custom aggregate class
from src.ixnetwork_aggregate import IxNetworkRESTAPI


# Simple demo
if __name__ == '__main__':
    # Configure logging module
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        format=(
            '%(asctime)s' +
            '%(levelname)12s module: %(filename)-12s ' +
            'line: %(lineno)4d message: %(message)s'))
    # Instantiate session to IxNetwork
    session = IxNetworkRESTAPI('10.27.200.3', '11009', 'admin', 'admin')
    # Get representation of session
    # (just for demonstration and logging purposes)
    logging.warning(f'Create instance of {repr(session)}')
    # Demonstration dictionary
    ports = {
        'port1/1': {
            'card': '1',
            'port': '1',
            'link_id': 'left_side'},
        'port1/3': {
            'card': '1',
            'port': '3',
            'link_id': 'right_side'}}
    # Select chassis and assign ports and save vports (below in analogy)
    session.assign_ports('10.27.193.3', ports, session.storage)
    session.create_topology(session.storage)
    session.create_device_groups(session.storage)
    session.create_ethernet(session.storage)
    session.create_ipv4(session.storage)
    # List of IPv4 address&gateway pair
    addressing_scheme = [
        (address + 10, address)
        for address in
        [ip_interface('10.100.0.10/24'), ip_interface('10.200.0.10/24')]]
    instance.ixia.change_ipv4_address(
        storage=instance.ixia.storage,
        addresses=addressing_scheme)
    instance.ixia.create_traffic_item(
        hrefs=instance.ixia.storage.ipv4)
    session.save_and_download_config()
    session.close_rest_session()
