from os.path import dirname
import sys
print(dirname(dirname(dirname(__file__))))
sys.path.append(dirname(dirname(dirname(__file__))))
from vmodel.vmodel import VModel
    
if __name__ == '__main__':
    vm = VModel([
                    {
                        'package':'vmodel.service_example.wabi_example',
                    },{
                        'package':'vmodel.service_example.simpler_example'
                    },{
                        'package':'vmodel.service_example.standard_example'
                    },
                ])
    print('调用服务完成，结果：',vm.run_and_dump('service_1', 'func_1', {'a':1,'b':2}))
    print('调用服务完成，结果：',vm.run_and_dump('service_1', 'func_2', {'a':'hello','b':'world'}))
    print(vm.get_service_info('service_1'))