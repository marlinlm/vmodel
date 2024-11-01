from vmodel.protocol.simpler_protocol import cleanup_func, get_service_info_func, prepare_func, service_func

@service_func('func_1','service_2')
def my_service_func_1(a:int, b:int):
    print("这是service_2.my_service_func_1")
    return a+b

@service_func('func_2','service_2')
def my_service_func_2(a:str, b:str):
    print("这是service_2.my_service_func_2")
    return a + ' ' + b

@get_service_info_func('service_2')
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
    
@prepare_func('service_2')
def my_prepare_func():
    # 下载模型文件以及数据文件到本地
    print("这是service_2.my_prepare_func")
    return True

@cleanup_func('service_2')
def my_unload_func():
    print("service_2.这是my_cleanup_func")
    return True

