from vmodel.protocol.simpler_protocol import get_service_info_func, prepare_func, service_func, cleanup_func

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
    

# 准备方法，后端服务应该在这个方法里下载所需文件
# 参数是服务名称，必须保证和上边的服务名称一致
@prepare_func('service_2')
def my_prepare_func() -> bool:
    """准备服务接口
            
        下载服务运行所需的模型以及数据集等文件。

        Parameters
        ----------
        无

        Returns
        -------
        bool
            如果准备过程成功，返回True，否则返回False
            
        """
        
    # 下载模型文件以及数据文件到本地
    print("service_1.这是my_prepare_func")
    return True


# 清理方法，后端服务要把下载的文件删掉
# 参数是服务名称，必须保证和上边的服务名称一致
@cleanup_func('service_2')
def my_cleanup_func():
    """卸载服务接口
            
        将所有下载的文件删除。

        Parameters
        ----------
        无

        Returns
        -------
        bool
            如果清理过程成功，返回True，否则返回False
            
        """
    
    print("service_1.这是my_cleanup_func")
    return True

