from typing import Callable
from vmodel.protocol.service_protocol import ServiceProtocol
from vmodel.protocol.service_registory import check_service_exists, get_service_protocol, register_service

class StandardProtocol(ServiceProtocol):
    def __init__(self, name):
        super().__init__(name)
        self._service_funcs:dict[str,Callable] = {}
        self._get_info_func:Callable = None
        self._prepare_func:Callable = None
        self._load_func:Callable = None
        self._test_func:Callable = None
        self._unload_func:Callable = None
        self._cleanup_func:Callable = None
        
    def register_service_func(self, name, func):
        if name in self._service_funcs:
            exist_func = self._service_funcs[name]
            raise KeyError(f'Service function name {name} already registed by method {exist_func.__name__}.')
        self._service_funcs[name] = func
    
    def register_get_info_func(self, func):
        self._get_info_func = func
    
    def register_prepare_func(self, func):
        self._prepare_func = func
        
    def register_load_func(self, func):
        self._load_func = func
    
    def register_test_func(self, func):
        self._test_func:Callable = func
    
    def register_unload_func(self, func):
        self._unload_func:Callable = func
        
    def register_cleanup_func(self, func):
        self._cleanup_func:Callable = func
        
    def involk_service_func(self, name:str, params:dict):
        if name in self._service_funcs:
            args = ()
            return self._service_funcs[name](*args, **params)
        
        raise NotImplementedError(f'Service {name} is not implemented.')
    
    def get_service_info(self):
        if not self._get_info_func: 
            return NotImplementedError('Get info function not implemented. Please add @get_service_info_func to your function.')
        
        return self._get_info_func()
    
    def run_and_dump(self, func_name:str, param:dict):
        if not self._prepare_func: 
            return NotImplementedError('Prepare function not implemented. Please add @prepare_func to your function.')
        if not self._load_func:
            return NotImplementedError('Load function not implemented. Please add @load_func to your function.')
        if not self._test_func:
            return NotImplementedError('Test function not implemented. Please add @test_func to your function.')
        if not self._unload_func:
            return NotImplementedError('Unload function not implemented. Please add @unload_func to your function.')
        if not self._cleanup_func:
            return NotImplementedError('Cleanup function not implemented. Please add @cleanup_func to your function.')


        if not self._prepare_func():
            raise RuntimeError('Error occurs while preparing.')
        if not self._load_func():
            raise RuntimeError('Error occurs while loading.')
        if not self._test_func():
            raise RuntimeError('Error occurs while testing.')
        output = self.involk_service_func(func_name, param)
        if not self._unload_func():
            raise RuntimeError('Error occurs while unloading.')
        if not self._cleanup_func():
            raise RuntimeError('Error occurs while cleaning up.')

        return output
    
    def involk_get_info_func(self):
        return self._get_info_func()
    
    def involk_prepare_func(self):
        return self._prepare_func()
    
    def involk_load_func(self):
        return self._load_func()
    
    def involk_test_func(self):
        return self._test_func()
    
    def involk_unload_func(self):
        return self._unload_func()
        

def get_or_create_service_reg(service:str):
    if not check_service_exists(service):
        protocol = StandardProtocol(service)
        register_service(service, protocol)
    return get_service_protocol(service)

def decorate(service:str, handler:Callable):
    if service is None:
        raise ValueError('Parameter service can not be None!')
    
    def decorator(func:Callable):
        def inner(*arg, **kwargs):
            return func(*arg, **kwargs)
        handler(func, get_or_create_service_reg(service))
        return inner
    
    return decorator

def service_func(name:str, service:str):
    if name is None:
        raise ValueError('Parameter name can not be None!')
    if service is None:
        raise ValueError('Parameter service can not be None!')
    
    return decorate(service=service, handler=lambda func, registry : registry.register_service_func(name = name if not name is None else func.__name__, func = func))


def get_service_info_func(service:str):
    return decorate(service=service, handler=lambda func, registry : registry.register_get_info_func(func))

def prepare_func(service:str):
    return decorate(service=service, handler=lambda func, registry : registry.register_prepare_func(func))

def load_func(service:str):
    return decorate(service=service, handler=lambda func, registry : registry.register_load_func(func))

def test_func(service:str):
    return decorate(service=service, handler=lambda func, registry : registry.register_test_func(func))

def unload_func(service:str):
    return decorate(service=service, handler=lambda func, registry : registry.register_unload_func(func))

def cleanup_func(service:str):
    return decorate(service=service, handler=lambda func, registry : registry.register_cleanup_func(func))
    