from vmodel.protocol.service_protocol import _meta_func, _service_func, decorate
from vmodel.protocol.wabi_protocol import META_FUNC_NAME_GET_INFO, WabiProtocol

META_FUNC_NAME_PREPARE = 'prepare'
META_FUNC_NAME_CLEANUP = 'cleanup'

class SimplerProtocol(WabiProtocol):
    def __init__(self, name):
        super().__init__(name)

    def run_and_dump(self, func_name:str, param:dict):

        if not self.involk_meta_func(name = META_FUNC_NAME_PREPARE):
            raise RuntimeError('Error occurs while preparing.')
        
        output = self.involk_service_func(func_name, param)
        
        if not self.involk_meta_func(name = META_FUNC_NAME_CLEANUP):
            raise RuntimeError('Error occurs while cleaning up.')

        return output

def service_func(name:str, service:str):
    return _service_func(name, service, SimplerProtocol)

def get_service_info_func(service:str):
    return _meta_func(name=META_FUNC_NAME_GET_INFO, service=service, protocol=SimplerProtocol)

def prepare_func(service:str):
    return _meta_func(name=META_FUNC_NAME_PREPARE, service=service, protocol=SimplerProtocol)

def cleanup_func(service:str):
    return _meta_func(name=META_FUNC_NAME_CLEANUP, service=service, protocol=SimplerProtocol)
    