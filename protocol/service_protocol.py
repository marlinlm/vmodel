class ServiceProtocol:
    def __init__(self, name):
        self.name = name

    def run_and_dump(self, func_name:str, param:dict):
        raise NotImplementedError(f'Method run_and_dump is not implemented in protocol {self.__class__.__name__}.')        
    
        