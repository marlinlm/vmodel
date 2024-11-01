from protocol.service_protocol import ServiceProtocol


service_registries = {}

def get_service_protocol(service:str):
    if service in service_registries:
        return service_registries[service]
    return None

def register_service(service:str, protocol:ServiceProtocol):
    if service in service_registries:
        raise KeyError(f'Service with name {service} already exits.')
    
    service_registries[service] = protocol
    
def check_service_exists(service:str):
    return service in service_registries