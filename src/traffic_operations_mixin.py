import json
from src.session_abc import IxNetworkSession


class TrafficOperationsMixin(IxNetworkSession):
    '''
    This is a mixin class. It only contains specific methods
    and can't be instantiate (due to inheritance from ABC class).

    This class contains methods for creating TrafficItems, set and change
    their properties.
    '''

    def create_traffic_item(
            self,
            hrefs,
            name='Test',
            trafficType='ipv4',
            frame_parameters={
                'rate': 100, 'type': 'percentLineRate', 'fixedSize': 1500},
            flow_groups=['ipv4SourceIp0', 'ipv4DestIp0']):
        '''
        The method creates traffic item with appropriate settings:
         * 100% line rate
         * frame size is 1500 bytes
         * bidirectional IPv4 (by default) traffic
        '''
        # Create traffic item with basic settings
        traffic_properties_dict_json = json.dumps([
            {
                "biDirectional": True,
                "enabled": True,
                "name": name,
                "routeMesh": "fullMesh",
                "trafficType": trafficType
            }])
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/trafficItem']),
            data=traffic_properties_dict_json)
        self.logger()
        # Set source and destinations (it uses provided hrefs).
        # You should provide here two hrefs, left side and right side.
        # At least for now it is hardcoded.
        end_points_dict_json = json.dumps([
            {
                "destinations": [
                    hrefs[0]
                ],
                "sources": [
                    hrefs[1]
                ]
            }])
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/endpointSet']),
            data=end_points_dict_json)
        self.logger()
        # Set frame parameters
        frame_rate_dict_json = json.dumps(
            {
                "rate": frame_parameters['rate'],
                "type": frame_parameters['type']
            })
        self.response = self.session.patch(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1/frameRate']),
            data=frame_rate_dict_json)
        self.logger()
        frame_size_dict_json = json.dumps(
            {
                "fixedSize": frame_parameters['fixedSize'],
            })
        self.response = self.session.patch(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1/frameSize']),
            data=frame_size_dict_json)
        self.logger()
        # Set Flow groups
        flow_groups_dict_json = json.dumps(
            {
                "distributions": flow_groups,
            })
        self.response = self.session.patch(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/configElement/1/transmissionDistribution']),
            data=flow_groups_dict_json)
        self.logger()
        # Set tracking
        tracking_dict_json = json.dumps(
            {
                "trackBy": [
                    "ethernetIiSourceaddress0",
                    "ethernetIiDestinationaddress0"]
            })
        self.response = self.session.patch(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1/tracking']),
            data=tracking_dict_json)
        self.logger()

    def start_all_traffic_items(self):
        '''
        The method starts all traffic items in the active IxNetwork scenario
        '''
        # Hardcoded only one session
        operations_dict_json = json.dumps(
            {
                "arg1": "/api/v1/sessions/1/ixnetwork/traffic"
            })
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/operations/start']),
            data=operations_dict_json)
        self.logger()

    def stop_all_traffic_items(self):
        '''
        The method stops all traffic items in the active IxNetwork scenario
        '''
        # Hardcoded only one session
        operations_dict_json = json.dumps(
            {
                "arg1": "/api/v1/sessions/1/ixnetwork/traffic"
            })
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/operations/stop']),
            data=operations_dict_json)
        self.logger()

    def generate_traffic_item(self):
        '''
        The method generates traffic items i.e. it triggers update procedure
        so that traffic item fields gets fresh data from topologies.
        '''
        # Hardcoded only one traffic item
        operations_dict_json = json.dumps(
            {
                "arg1": [
                    "/api/v1/sessions/1/ixnetwork/traffic/trafficItem/1"]
            })
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/trafficItem/operations/generate']),
            data=operations_dict_json)
        self.logger()

    def apply_traffic_item(self):
        '''
        The method applies traffic item settings.
        After this procedure in can be started.
        '''
        # Hardcoded only one traffic item
        operations_dict_json = json.dumps(
            {
                "arg1": "/api/v1/sessions/1/ixnetwork/traffic"
            })
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/traffic/operations/apply']),
            data=operations_dict_json)
        self.logger()
