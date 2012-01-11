from kombu import BrokerConnection

#import logging
#logger = logging.getLogger(__name__)

class Connection:
    def __init__(self):
        self.connection = None
        self._running = True
        self.channel = self.get_new_channel()
    
    def get_broker_connection(self):
        if self.connection is None:
            self.reconnect()
            
        return self.connection
    
    def get_channel(self):
        if self.channel is None:
            self.channel = self.get_new_channel()
        return self.channel
    
    def get_new_channel(self):
        if self.connection is None:
            self.reconnect()
        return self.connection.channel()
    
    def reconnect(self):
        self.connection = BrokerConnection("amqp://guest:guest@localhost:5672/nokkhum")
        
    def drain_events(self):
        while self._running:
            self.connection.drain_events()
            
    
    def release(self):
        self._running = False
        self.connection.release()
        self.connection = None
        
default_connection = Connection()