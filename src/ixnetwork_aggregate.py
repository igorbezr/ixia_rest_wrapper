import os
import ssl
import json
import logging
import warnings
import requests
import subprocess
from urllib3.exceptions import SubjectAltNameWarning
# Custom mixin classes with IxNetwork specific methods
from src.service_operations_mixin import ServiceOperationsMixin
from src.main_objects_mixin import MainObjectsMixin
from src.core_network_mixin import CoreNetworkObjectsMixin
from src.traffic_macroses_mixin import TrafficMacrosesMixin
# Custom component class for storing IxNetwork Resources
from src.storage_component import Storage


class IxNetworkRESTAPI(
        ServiceOperationsMixin,
        MainObjectsMixin,
        CoreNetworkObjectsMixin,
        TrafficMacrosesMixin):
    '''
    It is a concrete realization of IxNetworkSession abstract base class.

    This class provides interaction with IxNetwork GUI client on
    Windows machine through native REST API. So it is an aggregate
    class, ready for use to end user.

    Here and anywhere bellow we are implicit that IxNetwork has only
    self-signed certificate
    '''
    def __init__(
            self,
            rest_host: str,
            rest_port: str,
            user: str,
            password: str):
        # Conversion to the string for safety
        self.__rest_host = str(rest_host)
        self.__rest_port = str(rest_port)
        self.__username = str(user)
        self.__password = str(password)
        self.__hostname = 'ixnetwork-self-host'
        self.__entry_point = f'https://{self.hostname}:{self.rest_port}'
        # Essential methods invoking
        self.certificate_preparation()
        self.resolve_hostname_mismatch()
        self.make_rest_session()
        # Initialize storage
        self.storage = Storage()

    # These attributes are private and should not been change during
    # all the object life.
    @property
    def rest_host(self):
        return self.__rest_host

    @property
    def rest_port(self):
        return self.__rest_port

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def hostname(self):
        return self.__hostname

    @property
    def entry_point(self):
        return self.__entry_point

    def __repr__(self):
        '''
        Representation should allow developer construct identically
        instance of class base on it.
        So we want to eval(repr(self)) == self
        '''
        representation: str = ''.join([
            type(self).__name__,
            '(',
            ', '.join([
                repr(self.rest_host), repr(self.rest_port),
                repr(self.username), repr(self.password)]),
            ')'])
        return representation

    def logger(self):
        '''
        Simple wrapper around logging with few format strings preset for
        pretty printing INFO logging messages.

        Also, here we implicit, that main module already have logger, so
        we just get it with its config.
        '''
        if self.response.request.body is not None:
            body = ''.join([
                '\n', json.dumps(
                    json.loads(
                        self.response.request.body), indent=4)])
        else:
            body = 'None'
        status = ' '.join([
            str(self.response.status_code), self.response.reason])
        # Not all response content has a valid JSON representation, especially if
        # it is binary file. So here we must catch and handle exceptions.
        try:
            self.response_json = ''.join([
                '\n', json.dumps(
                    self.response.json(), indent=4)])
        except json.decoder.JSONDecodeError:
            self.response_json = 'Binary content'
        fmt_info = (
            f'\nREQUEST'
            f'\nURL:     {self.response.request.url}'
            f'\nHeaders: {self.response.request.headers}'
            f'\nJSON:    {body}'
            f'\nRESPONSE'
            f'\nStatus:  {status}'
            f'\nHeaders: {self.response.headers}'
            f'\nJSON:    {self.response_json}')
        logging.getLogger(__name__).info(fmt_info)

    def certificate_preparation(self):
        '''
        The method gets self-signed certificate from remote IxNetwork server
        and sets it as trusted CA. It prevents security warnings from appearing.
        '''
        # Get server self-signed certificate
        ixia_self_signed_sert = ssl.get_server_certificate(
            (self.rest_host, self.rest_port))
        with open('/root/cert.pem', 'w', encoding='utf-8') as cert_file:
            cert_file.write(ixia_self_signed_sert)
        # Set retrieved certificate as trusted for requests library
        # through specific env attribute
        os.environ['REQUESTS_CA_BUNDLE'] = '/root/cert.pem'

    def resolve_hostname_mismatch(self):
        '''
        Due to default IxNetwork self-signed certificate has hostname
        'IxNetwork-Self-Host', that doesn't match his real DNS name,
        here we use workaround - just putting it into the /etc/hosts,
        if it not exists there already.
        '''
        # Set mapping between IP and hostname in certificate
        cmd = ['echo', self.rest_host, self.hostname, '>>', '/etc/hosts']
        with open('/etc/hosts', 'r') as hosts_file:
            unique_hosts = set(hosts_file.read().split('\n'))
        if ' '.join([self.rest_host, self.hostname]) not in unique_hosts:
            # It seems that shell is must be here, through it is unsafe
            subprocess.call(' '.join(cmd), shell=True)
        # Supress warning about absence of subjectAltName in the certificate
        # "Certificate for ixnetwork-self-host has no `subjectAltName`"
        warnings.simplefilter('ignore', SubjectAltNameWarning)

    def make_rest_session(self):
        '''
        The method provides user authentication and sets up Ixnetwork
        configuration to the default state.
        '''
        # For authentication we are using simple dictionary
        auth_dict_json = json.dumps(
            {'username': self.username, 'password': self.password},
            ensure_ascii=True)
        # Create session and set default headers
        self.session = requests.Session()
        self.session.headers = {'Content-Type': 'application/json; charset=us-ascii'}
        # Authenticate user
        self.response = self.session.post(
            url=''.join([self.entry_point, '/api/v1/auth/session']),
            data=auth_dict_json)
        self.logger()
        # Set retrieved auth token
        self.session.headers['apiKey'] = self.response.json()['apiKey']
        self.session.headers['username'] = self.response.json()['username']
        # Erase previous config and setting up new one
        self.response = self.session.post(
            url=''.join([
                self.entry_point,
                '/api/v1/sessions/1/ixnetwork/operations/newconfig']))
        self.logger()

    def close_rest_session(self):
        '''
        The method closes session to the IxNetwork host
        and deletes reference to the main session object
        '''
        self.session.close()
        del self.session
