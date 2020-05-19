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
    session = IxNetworkRESTAPI('192.168.1.1', '443', 'username', 'password')
    # Get representation of session
    # (just for demonstration and logging purposes)
    logging.warning(f'Create instance of {repr(session)}')
    # Demonstration dictionary
    ports = {
        'port1/1': {
            'card': '1',
            'port': '1',
            'link_id': 'left_side'},
        'port1/2': {
            'card': '1',
            'port': '2',
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
    session.change_ipv4_address(
        storage=session.storage,
        addresses=addressing_scheme)
    # Create, start&stop traffic stream
    session.create_traffic_item(
        hrefs=session.storage.ipv4)
    session.generate_traffic_item()
    session.apply_traffic_item()
    session.start_all_traffic_items()
    session.stop_all_traffic_items()
    session.save_and_download_config()
    session.close_rest_session()
