import json
from pprint import pformat


class Storage():
    '''
    This is a concrete class that should be used like a storage for existing
    IxNetwork resources, like vports, topologies,devices groups and interfaces.
    '''

    # Class-level private attributes, listed in Storage.__dict__
    __vports = []
    __topologies = []
    __device_groups = []
    __ethernets = []
    __ipv4 = []

    # This attributes is part of interface of Storage class
    # (protected instance-level attributes)
    @property
    def vports(self):
        return self._vports

    @property
    def topologies(self):
        return self._topologies

    @property
    def device_groups(self):
        return self._device_groups

    @property
    def ethernets(self):
        return self._ethernets

    @property
    def ipv4(self):
        return self._ipv4

    def __setattr__(self, name, value):
        '''
        We can set only those attributes, that were defined
        like class private above (but we are create them like protected,
        instance-level attributes)
        '''
        if f'_{type(self).__name__}__{name}' in eval(
                f'{type(self).__name__}.__dict__'):
            # Using __setattr__ from object()
            super().__setattr__(f'_{name}', self.save_href(value))
        else:
            raise AttributeError(f'"{name}" is not allowed attribute',)

    @staticmethod
    def save_href(value):
        '''
        The method gets hrefs (full api paths) to the IxNetwork resource
        from server response
        '''
        try:
            hrefs = [
                resource['href']
                for entry in value
                for resource in json.loads(entry)['links']]
        except Exception:
            raise TypeError(f'"{value}" is not properly formated JSON')
        return hrefs

    def __repr__(self):
        # Rename key in self.__dict__ so
        # it will be type(self).__name__.__dict__
        renamed_dict = {
            f'{self.__class__}.{key[1:]}': self.__dict__[key]
            for key in self.__dict__}
        # Pretty formatting renamed_dict
        representation = pformat(renamed_dict)
        return representation
