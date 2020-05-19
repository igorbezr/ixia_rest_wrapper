import json
from time import sleep

from src.traffic_operations_mixin import TrafficOperationsMixin


class TrafficMacrosesMixin(TrafficOperationsMixin):
    '''
    This is a mixin class. It only contains specific methods
    and can't be instantiate (due to inheritance from ABC class).

    This class contains macroses for simplify traffic items creation
    '''

    def traffic_item_macros(self, duration=60):
        '''
        The method combines several traffic items operations to perform
        traffic item creation, starting, waiting traffic duration time,
        gathering statistics and finally stopping traffic stream.
        '''
        self.generate_traffic_item()
        self.apply_traffic_item()
        self.start_all_traffic_items()
        sleep(duration)
        handy_statistics, formatted_statistics = self.gathering_flow_statistics()
        self.stop_all_traffic_items()
        return handy_statistics, formatted_statistics

    def gathering_flow_statistics(self):
        '''
        The method gets view ID from /statistics node and the gathering
        flow statistics data from this view.
        '''
        select_dict_json = json.dumps(
            {
                "selects": [
                    {
                        "from": "/statistics",
                        "properties": [],
                        "children": [
                            {
                                "child": "view",
                                "properties": [
                                    "*"
                                ],
                                "filters": []
                            }
                        ],
                        "inlines": []
                    }
                ]
            })
        # Get statistics views IDs
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/operations/select']),
            data=select_dict_json)
        view_ids = self.response.json()['result'][0]['view']
        # Finding flow statistics view id
        for view in view_ids:
            if view['csvFileName'] == 'Flow Statistics.csv':
                flow_statistics_view_id = view['id']
                break
        # Get data from founded view
        select_dict_json = json.dumps(
            {
                "selects": [
                    {
                        "from": f"/statistics/view/{flow_statistics_view_id}/data",
                        "properties": [
                            "pageValues",
                            "columnCaptions",
                        ],
                        "children": [],
                        "inlines": []
                    }
                ]
            })
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/operations/select']),
            data=select_dict_json)
        flow_statistics_row_data = self.response.json()['result'][0]
        flow_statistics_row_data.pop('href')
        # Construct two statistics: handy dictionary and pretty formatted str
        handy_statistics = {}
        TITLE = 'FLOW STATISTICS'
        formatted_statistics = f'{TITLE:^130}'
        directions = ['Straight direction', 'Backward direction']
        formatted_statistics += f'\n\n{directions[0]:<65} {directions[1]:<65}\n'
        # Sub-dictionaries for both traffic direction
        handy_statistics['straight_direction'] = {}
        handy_statistics['backward_direction'] = {}
        for index, key in enumerate(flow_statistics_row_data['columnCaptions']):
            handy_statistics['straight_direction'][key] = flow_statistics_row_data[
                'pageValues'][0][0][index]
            handy_statistics['backward_direction'][key] = flow_statistics_row_data[
                'pageValues'][1][0][index]
            # Pretty formatting output
            formatted_statistics += ''.join([
                f'\n{key:<40} {flow_statistics_row_data["pageValues"][0][0][index]:<25}',
                f' {key:<40} {flow_statistics_row_data["pageValues"][1][0][index]:<25}'])
        return handy_statistics, formatted_statistics
