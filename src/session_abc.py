import abc


class IxNetworkSession(abc.ABC):
    '''
    Internal base class.

    It only defines interfaces that each concrete class should implement.
    '''

    @abc.abstractmethod
    def __init__(self):
        '''
        In the __init__ method concrete class should assign provided arguments
        to private attributes, make all the preparation work and begin new
        IxNetwork with method make_rest_session().
        In another words, the method should provide completely ready to use
        class for end user.
        '''

    @abc.abstractmethod
    def make_rest_session(self):
        '''
        Concrete class should provide user authentication and setting up
        IxNetwork configuration to the default state.
        Here should be main session object through that end user will be
        doing all his tasks.
        '''

    @abc.abstractmethod
    def close_rest_session(self):
        '''
        Here concrete class should close session to the IxNetwork host
        and delete reference to the main session object.
        '''

    @abc.abstractmethod
    def logger(self):
        '''
        For troubleshooting, debugging and simple for informational purposes
        compatible concrete class should implement some wrapper around logging
        module that can print pretty formated log messaged into stdout.
        '''
