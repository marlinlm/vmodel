from pyclbr import Class
from typing import Callable

service_registries = {}

def get_service_protocol(service:str):
    if service in service_registries:
        return service_registries[service]
    return None

def register_service(service:str, protocol:object):
    if service in service_registries:
        raise KeyError(f'Service with name {service} already exits.')
    
    service_registries[service] = protocol

    
def check_service_exists(service:str):
    return service in service_registries


class ServiceProtocol:
    def __init__(self, name):
        self.name = name
        self._service_funcs:dict[str,Callable] = {}
        self._meta_funcs:dict[str, Callable] = {}

    def run_and_dump(self, func_name:str, param:dict):
        raise NotImplementedError(f'Method run_and_dump is not implemented in protocol {self.__class__.__name__}.')        
    
    def get_service_info(self):
        return NotImplementedError(f'Method run_and_dump is not implemented in protocol {self.__class__.__name__}.')

    def involk_service_func(self, name:str, params:dict):
        if name in self._service_funcs:
            args = ()
            return self._service_funcs[name](*args, **params)
        
        raise NotImplementedError(f'Service {self.name} has no function with name {name}.')
    
    def involk_meta_func(self, name:str, params:dict = {}):
        if name in self._meta_funcs:
            args = ()
            return self._meta_funcs[name](*args, **params)
        
        raise NotImplementedError(f'Service {self.name} has no function with name {name}.')
    
    def register_service_func(self, name, func):
        if name is None:
            raise ValueError(f'Service function name can not be None. Regestering method {func.__name__} for class {self.__class__.__name__} without function name.')
        if name in self._service_funcs:
            exist_func = self._service_funcs[name]
            raise KeyError(f'Service function name {name} already registed by method {exist_func.__name__}.')
        self._service_funcs[name] = func
    
    def register_meta_func(self, name, func):
        if name is None:
            raise ValueError(f'Meta function name can not be None. Regestering method {func.__name__} for class {func.__module__} without function name.')
        if name in self._meta_funcs:
            exist_func = self._meta_funcs[name]
            raise KeyError(f'Meta function name confliction. Meta function name {name} registed by {exist_func.__name__} for class {exist_func.__module__} and {func.__name__} for class {func.__module__}.')
        self._meta_funcs[name] = func
    
    
def get_or_create_service_reg(service:str, protocol:Class):
    if not check_service_exists(service):
        new_protocol = protocol(service)
        register_service(service, new_protocol)
    ret_protocol = get_service_protocol(service)
    if isinstance(ret_protocol, protocol):
        # new protocol is a super class of exisiting protocol. Use the existing protocol.
        return ret_protocol
    raise ValueError(f'Protocol confliction. Service {service} is registed with protocols {ret_protocol.__class__.__name__} and {protocol.__name__}. Please make sure one service name only registed one protocol.') 

def decorate(service:str, handler:Callable, protocol:Class):
    if service is None:
        raise ValueError('Parameter service can not be None!')
    
    def decorator(func:Callable):
        def inner(*arg, **kwargs):
            return func(*arg, **kwargs)
        handler(func, get_or_create_service_reg(service, protocol))
        return inner
    
    return decorator

def _service_func(name:str, service:str, protocol:Class):
    return decorate(service=service, 
                    handler=lambda func, protocol : protocol.register_service_func(name = name if not name is None else func.__name__, func = func),
                    protocol = protocol
                    )
    
def _meta_func(name:str, service:str, protocol:Class):
    return decorate(service=service, 
                    handler=lambda func, protocol : protocol.register_meta_func(name, func),
                    protocol = protocol
                    )
