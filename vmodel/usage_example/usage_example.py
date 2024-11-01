from os.path import dirname
import sys

sys.path.append(dirname(dirname(__file__)))
from vmodel.vmodel import VModel


    
if __name__ == '__main__':
    vm = VModel([
                            {
                                'package':'service_example.service_example',
                            },{
                                'package':'service_example.service_example_2'
                            }
                        ])
    print('调用服务完成，结果：',vm.run_and_dump('service_1', 'func_1', {'a':1,'b':2}))
    print('调用服务完成，结果：',vm.run_and_dump('service_2', 'func_1', {'a':1,'b':2}))