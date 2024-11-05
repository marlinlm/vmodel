from vmodel.protocol.service_protocol import _meta_func, _service_func, decorate
from vmodel.protocol.simpler_protocol import META_FUNC_NAME_CLEANUP, META_FUNC_NAME_PREPARE, SimplerProtocol
from vmodel.protocol.wabi_protocol import META_FUNC_NAME_GET_INFO

META_FUNC_NAME_LOAD = 'load'
META_FUNC_NAME_TEST = 'test'
META_FUNC_NAME_UNLOAD = 'unload'

class StandardProtocol(SimplerProtocol):
    def __init__(self, name):
        super().__init__(name)
        
   
    def run_and_dump(self, func_name:str, param:dict):

        if not self.involk_meta_func(name = META_FUNC_NAME_PREPARE):
            raise RuntimeError('Error occurs while preparing.')
        if not self.involk_meta_func(name = META_FUNC_NAME_LOAD):
            raise RuntimeError('Error occurs while loading.')
        if not self.involk_meta_func(name = META_FUNC_NAME_TEST):
            raise RuntimeError('Error occurs while testing.')
        output = self.involk_service_func(func_name, param)
        if not self.involk_meta_func(name = META_FUNC_NAME_UNLOAD):
            raise RuntimeError('Error occurs while unloading.')
        if not self.involk_meta_func(name = META_FUNC_NAME_CLEANUP):
            raise RuntimeError('Error occurs while cleaning up.')

        return output
    
def service_func(name:str, service:str):
    return _service_func(name, service, StandardProtocol)

def get_service_info_func(service:str):
    return _meta_func(name=META_FUNC_NAME_GET_INFO, service=service, protocol=StandardProtocol)

def prepare_func(service:str):
    return _meta_func(name=META_FUNC_NAME_PREPARE, service=service, protocol=StandardProtocol)

def cleanup_func(service:str):
    return _meta_func(name=META_FUNC_NAME_CLEANUP, service=service, protocol=StandardProtocol)
    
def load_func(service:str):
    return _meta_func(name=META_FUNC_NAME_LOAD, service=service, protocol=StandardProtocol)

def test_func(service:str):
    return _meta_func(name=META_FUNC_NAME_TEST, service=service, protocol=StandardProtocol)

def unload_func(service:str):
    return _meta_func(name=META_FUNC_NAME_UNLOAD, service=service, protocol=StandardProtocol)

    