import json
from src.session_abc import IxNetworkSession


class ServiceOperationsMixin(IxNetworkSession):
    '''
    This is a mixin class. It only contains specific methods
    and can't be instantiate (due to inheritance from ABC class).

    The class contains methods for service operations, like save/load
    configuration, start/stop topology and/or separate protocols etc.
    '''

    IXIA_CONFIG_NAME: str = 'ixia_config.ixncfg'

    def save_and_download_config(self):
        '''
        The method saves IxNetowrk configuration to the file
        and downloads it from IxNetwork to HFTS.
        '''
        # Save configuration
        filename_dict_json = json.dumps(
            {'arg1': ServiceOperationsMixin.IXIA_CONFIG_NAME},
            ensure_ascii=True)
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/operations/saveconfig']),
            data=filename_dict_json)
        self.logger()
        # Get config from IxNetwork
        self.response = self.session.get(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/files?filename=' +
                f'{ServiceOperationsMixin.IXIA_CONFIG_NAME}']))
        self.logger()
        # Write retrieved config to the file (in bytes)
        with open(ServiceOperationsMixin.IXIA_CONFIG_NAME, 'wb') as file:
            file.write(self.response.content)

    def start_all_protocols(self):
        '''
        The method starts all protocols for all topologies in the active
        IxNetwork scenario
        '''
        # Here we just prepare an empty JSON
        operations_dict_json = json.dumps([{}])
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/operations/startallprotocols']),
            data=operations_dict_json)
        self.logger()

    def stop_all_protocols(self):
        '''
        The method stops all protocols for all topologies in the active
        IxNetwork scenario
        '''
        # Here we just prepare an empty JSON
        operations_dict_json = json.dumps([{}])
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/operations/stopallprotocols']),
            data=operations_dict_json)
        self.logger()
