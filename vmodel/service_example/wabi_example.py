from vmodel.protocol.wabi_protocol import get_service_info_func, service_func

@service_func('func_3','service_1')
def my_service_func_1(a:int, b:int):
    print("这是service_2.my_service_func_1")
    return a+b

@service_func('func_4','service_2')
def my_service_func_2(a:str, b:str):
    print("这是service_2.my_service_func_2")
    return a + ' ' + b

@get_service_info_func('service_3')
def my_get_info():
    print("这是service_2.my_get_info")
    return {
                'service_name':'服务名称',
                'service_desc':'服务描述',
                'resources':{ # 资源限制，可选，不提供该信息则认为无资源限制
                    'cpu':3,# 服务所需cpu核数
                    'memory':1024 * 1024 * 1024, # 内存限制，以B(Byte)为单位 
                    'gpu': '0,1', # 使用GPU显卡号
                },
                'methods':[
                    {
                        'name':'方法名称',
                        'desc':'方法的描述',
                        'params':[
                            {
                                'name':'参数名称',
                                'type':'参数类型', # 如：str, int, float, list, dict...
                                'type_desc':'用一段文字描述参数类型', 
                                'desc':'用一段文字描述参数的作用'
                            },
                        ],
                        'return':{
                            'type': '返回值类型', # 如：str, int, float, list, dict...
                            'type_desc':'用一段文字描述返回值的类型，或者结构',
                            'desc':'用一段文字描述返回值的作用'
                        }
                    },
                ],
            }
    
