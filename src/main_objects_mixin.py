import json
from src.session_abc import IxNetworkSession


class MainObjectsMixin(IxNetworkSession):
    '''
    This is a mixin class. It only contains specific methods
    and can't be instantiate (due to inheritance from ABC class).

    This class contains methods for creating basic IxNetwork objects like
    virtual ports, topologies, device and network groups
    '''

    def assign_ports(self, chassis_ip: str, ports: dict, storage):
        '''
        The method provides chassis selection and ports assignation in purpose
        of setting up IxNetwork configuration.
        '''
        # Select hardware chassis
        chassis_dict_json = json.dumps(
            {'hostname': chassis_ip},
            ensure_ascii=True)
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/availableHardware/chassis']),
            data=chassis_dict_json)
        self.logger()
        # Assign ports mentioned in the "ports" dictionary
        chassis_href = '/api/v1/sessions/1/ixnetwork/availableHardware/chassis/1/'
        ports_dict_json = json.dumps(
            [
                {
                    'connectedTo': ''.join([
                        chassis_href, 'card/', ports[port]['card'], '/port/', ports[port]['port']]),
                    'name': ports[port]['link_id']
                }
                for port in ports
            ],
            ensure_ascii=True)
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/vport']),
            data=ports_dict_json)
        # Save vports hrefs for future usage
        storage.vports = [self.response.text]
        self.logger()

    def create_topology(self, storage, existed_vports=None):
        '''
        This module creates IxNetowrk topology based on previously created ports
        '''
        if not existed_vports:
            existed_vports = storage.vports
        cummulative_hrefs = []
        # Create new topology with existed vports
        for port_href in existed_vports:
            vport_dict_json = json.dumps(
                [
                    {
                        'ports': [port_href]
                    }
                ])
            self.response = self.session.post(
                url=''.join([
                    self.entry_point,
                    '/api/v1/sessions/1/ixnetwork/topology']),
                data=vport_dict_json)
            cummulative_hrefs.append(self.response.text)
            self.logger()
        # Save topology hrefs for future usage
        storage.topologies = cummulative_hrefs

    def create_device_groups(
            self,
            storage,
            existed_topologies=None,
            multiplier: int=1):
        '''
        This module creates DeviceGroups based on previously created topologies
        '''
        if not existed_topologies:
            existed_topologies = storage.topologies
        cummulative_hrefs = []
        # Create new DeviceGroups for existed topologies
        for topology_href in existed_topologies:
            devicegroup_dict_json = json.dumps(
                [
                    {
                        'multiplier': multiplier,
                        'name': topology_href[-1]
                    }
                ])
            self.response = self.session.post(
                url=''.join([
                    self.entry_point,
                    topology_href,
                    '/deviceGroup']),
                data=devicegroup_dict_json)
            cummulative_hrefs.append(self.response.text)
            self.logger()
        # Save DeviceGroups hrefs for future usage
        storage.device_groups = cummulative_hrefs
