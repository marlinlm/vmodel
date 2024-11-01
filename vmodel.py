from importlib import import_module

from protocol.service_protocol import ServiceProtocol
from protocol.service_registory import get_service_protocol

class VModel:
    def __init__(self, config:list):
        for service_conf in config:
            package = service_conf['package']
            import_module(name=package)
    
    def run_and_dump(self, service:str, func_name:str, param:dict):
        protocol:ServiceProtocol = get_service_protocol(service)
        if not protocol:
            raise NotImplementedError(f'Service with name {service} does not exists.')
        return protocol.run_and_dump(func_name=func_name, param = param)    