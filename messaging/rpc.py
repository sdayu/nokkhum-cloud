'''
Created on Jan 11, 2012

@author: boatkrap
'''

import kombu.utils

from . import publisher
from . import consumer

import logging
logger = logging.getLogger(__name__)

import time

class RPC():
    def __init__(self):
        self._publisher = None
        self._consumer = None
        
        self.message_pool = {}
        
        self.initial()
        
        
    def initial(self):
        self._publisher = publisher.PublisherFactory().get_publisher("nokkhum_compute.*.rpc_request")
        self._consumer = consumer.ConsumerFactory().get_consumer("nokkhum_compute.*.rpc_response")
        self.regist_default_consumer_callback()
    
    def regist_default_consumer_callback(self):
        def process_message(body, message):
            message.ack()
            if 'message_id' in body:
                self.message_pool[body['message_id']] = body
            else:
                logger.debug('message ignore by RPC: %s'%body)
                
        self._consumer.register_callback(process_message)
                
    def call(self, message, routing_key):
        message_id = kombu.utils.uuid()
        message['message_id'] = message_id
        
        self.send(message, routing_key)
        
        while message_id not in self.message_pool.keys():
            time.sleep(0.01)
            
        response = self.message_pool[message_id]
        return response
        
    def send(self, message, routing_key):
        self._publisher.send(message, routing_key)
        
class RpcClient(RPC):
    def __init__(self):    
        RPC.__init__(self)
        
    def initial(self):
        self._publisher = publisher.PublisherFactory().get_publisher("nokkhum_compute.*.rpc_request")
        self._consumer = consumer.ConsumerFactory().get_consumer("nokkhum_compute.*.rpc_response")
        self.regist_default_consumer_callback()
        logger.debug("initial RPC Client")
    
class RpcServer(RPC):
    def __init__(self, ip):
        self.__publisher_rounting_key    = "nokkhum_compute.%s.rpc_response"%ip.replace('.', ":")
        self.__consumer_rounting_key     = "nokkhum_compute.%s.rpc_request"%ip.replace('.', ":")
        
        RPC.__init__(self)
        
    def initial(self):
        self.__publisher = publisher.PublisherFactory().get_publisher(self.__publisher_rounting_key)
        self.__consumer = consumer.ConsumerFactory().get_consumer(self.__consumer_rounting_key)
        
        logger.debug("initial RPC Server")
        
    def register_callback(self, callback):
        self.__consumer.register_callback(callback)
        
    def reply(self, message):
        self.__publisher.send(message, self.__publisher_rounting_key)

class RpcFactory():
    def __init__(self):
        self.default_rpc_client = None
        self.default_rpc_server = None
        
    def get_default_rpc_client(self):
        if self.default_rpc_client is None:
            self.default_rpc_client = RpcClient()
        return self.default_rpc_client
    
    def get_default_rpc_server(self, ip):
        if self.default_rpc_server is None:
            self.default_rpc_server = RpcServer(ip)
        return self.default_rpc_server
    
        

    