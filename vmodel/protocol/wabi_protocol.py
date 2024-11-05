from vmodel.protocol.service_protocol import ServiceProtocol, _meta_func, _service_func

META_FUNC_NAME_GET_INFO = 'get_service_info'

class WabiProtocol(ServiceProtocol):
    def __init__(self, name):
        super().__init__(name)
        
    def get_service_info(self):
        return self.involk_meta_func(META_FUNC_NAME_GET_INFO)
        
    def run_and_dump(self, func_name:str, param:dict):
        return self.involk_service_func(func_name, param)
    
def service_func(name:str, service:str):
    return _service_func(name, service, WabiProtocol)

def get_service_info_func(service:str):
    return _meta_func(name=META_FUNC_NAME_GET_INFO, service=service, protocol=WabiProtocol)

