import json
from src.session_abc import IxNetworkSession


class CoreNetworkObjectsMixin(IxNetworkSession):
    '''
    This is a mixin class. It only contains specific methods
    and can't be instantiate (due to inheritance from ABC class).

    This class contains methods for creating core IxNetwork objects, like
    Ethernet, IPv4 and IPv6 instances inside DeviceGroups.
    '''

    def create_ethernet(self, storage, existed_device_groups=None):
        '''
        The method creates Ethernet instances for provided DeviceGroups
        '''
        if not existed_device_groups:
            existed_device_groups = storage.device_groups
        cummulative_hrefs = []
        # Currently we just send empty JSON
        ethernet_properties_dict_json = json.dumps([{}])
        # For each DeviceGroup within each topology
        for device_group_href in existed_device_groups:
            self.response = self.session.post(
                url=''.join([
                    self.entry_point,
                    device_group_href,
                    '/ethernet']),
                data=ethernet_properties_dict_json)
            cummulative_hrefs.append(self.response.text)
            self.logger()
        # Save Ethernets hrefs for future usage
        storage.ethernets = cummulative_hrefs

    def create_ipv4(
            self,
            storage,
            existed_ethernets=None):
        '''
        The method is very similar to create_ethernet()
        '''
        if not existed_ethernets:
            existed_ethernets = storage.ethernets
        cummulative_hrefs = []
        # Currently we just send empty JSON
        ipv4_properties_dict_json = json.dumps([{}])
        # For each provided Ethernet object
        for ethernet_href in existed_ethernets:
            self.response = self.session.post(
                url=''.join([
                    self.entry_point,
                    ethernet_href,
                    '/ipv4']),
                data=ipv4_properties_dict_json)
            cummulative_hrefs.append(self.response.text)
            self.logger()
        # Save IPv4 hrefs for future usage
        storage.ipv4 = cummulative_hrefs

    def change_ipv4_address(self, storage, addresses: list):
        '''
        The method gets hrefs for IPv4 address, prefix and gateway from
        IPv4 IxNetwork object and then changes them according to provided
        arguments.
        '''
        for index, pair in enumerate(addresses):
            # Get searching hrefs
            self.response = self.session.get(
                url=''.join([
                    self.entry_point,
                    storage.ipv4[index]]))
            self.logger()
            hrefs_dictionary = self.response.json()
            # Set address
            ipv4_dict_json = json.dumps(
                [
                    {
                        'value': str(pair[0].ip)
                    }
                ])
            self.response = self.session.post(
                url=''.join([
                    self.entry_point,
                    hrefs_dictionary['address'],
                    '/singleValue']),
                data=ipv4_dict_json)
            self.logger()
            # Set network mask
            prefix_dict_json = json.dumps(
                {
                    'value': str(pair[1].with_prefixlen.split('/')[1])
                })
            self.response = self.session.patch(
                url=''.join([
                    self.entry_point,
                    hrefs_dictionary['prefix'],
                    '/singleValue']),
                data=prefix_dict_json)
            self.logger()
            # Set gateway
            gateway_dict_json = json.dumps(
                [
                    {
                        'value': str(pair[1].ip)
                    }
                ])
            self.response = self.session.post(
                url=''.join([
                    self.entry_point,
                    hrefs_dictionary['gatewayIp'],
                    '/singleValue']),
                data=gateway_dict_json)
            self.logger()
