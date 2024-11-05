from vmodel.protocol.standard_protocol import cleanup_func, get_service_info_func, load_func, prepare_func, test_func, unload_func, service_func

# 如果使用简化协议 请导入 from vmodel.protocol.simpler_protocol import cleanup_func, get_service_info_func, prepare_func, service_func

# 服务接口注解
@service_func('func_1','service_1')
# 方法内的参数没有任何要求，调用的用dict作为参数，把dict里的key和参数名对应即可。
def my_service_func_1(a:int, b:int):
    """服务接口实现
            
        通过给方法添加@service_func注解来实现服务接口。
        @service_func的第一个参数为映射之后的方法名，第二个参数为服务名。一个服务可以有多个方法。服务名必须保证全局唯一，方法名服务内唯一。
        
        Parameters
        ----------
        可根据实际需要决定需要多少参数以及什么参数。这个方法的参数只是一个例子。

        Returns
        -------
        Any
            可根据实际需要返回
    """

    print("这是service_1.my_service_func_1")
    return a+b

# 这是同一个服务里的另一个接口
@service_func('func_2','service_1')
def my_service_func_2(a:str, b:str):
    print("这是service_1.my_service_func_2")
    return a + ' ' + b

# 获取服务信息接口，返回参数格式请见return
# 参数是服务名称，必须保证和上边的服务名称一致
@get_service_info_func('service_1')
def my_get_info():
    """获取服务信息接口
            
        获取服务详细信息，以字典格式返回，包括服务名称，服务总体功能描述，服务资源需求，以及服务接口列表。

        Parameters
        ----------
        无

        Returns
        -------
        dict
            返回以下格式的字典
            
                {
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
                            'desc':'方法的描述'
                            'params':[
                                {
                                    'name':'参数名称',
                                    'type':'参数类型', # 如：str, int, float, list, dict...
                                    'type_desc':'用一段文字描述参数类型', 
                                    'desc':'用一段文字描述参数的作用'
                                },
                                ...
                            ],
                            'return':{
                                'type': '返回值类型', # 如：str, int, float, list, dict...
                                'type_desc':'用一段文字描述返回值的类型，或者结构',
                                'desc':'用一段文字描述返回值的作用'
                            }
                        },
                        ...
                    ],
                }
            
    """
    print("这是service_1.my_get_info")
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
@prepare_func('service_1')
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


# 加载方法，后端服务应该在这个方法里把模型加载到内存
# 参数是服务名称，必须保证和上边的服务名称一致
# 只有standard protocol 有这个接口，simpler protocol没有这个接口，要把这部分逻辑在@prepare_func里实现
@load_func('service_1')
def my_load_func() -> bool:
    """加载服务接口
            
        将服务所需的模型或者数据加载到内存或显存。

        Parameters
        ----------
        无

        Returns
        -------
        bool
            如果加载过程成功，返回True，否则返回False
            
        """
    
    # 加载模型到内存
    print("service_1.这是my_load_func")
    return True

# 测试方法，在模型启动后会执行
# 参数是服务名称，必须保证和上边的服务名称一致
# 只有standard protocol 有这个接口，simpler protocol没有这个接口，不用实现
@test_func('service_1')
def my_test_func():
    """测试接口
            
        在服务的方法执行前运行几个测试用例，确保服务可用。

        Parameters
        ----------
        无

        Returns
        -------
        bool
            如果测试过程成功，返回True，否则返回False
            
        """
        
    print("service_1.这是my_test_func")
    return True

# 卸载方法，后端服务要把模型从内存清理掉
# 参数是服务名称，必须保证和上边的服务名称一致
# 只有standard protocol 有这个接口，simpler protocol没有这个接口，要把这部分逻辑在@cleanup_func里实现
@unload_func('service_1')
def my_unload_func():
    """卸载服务
            
        将服务所需的模型或者数据从内存卸载。

        Parameters
        ----------
        无

        Returns
        -------
        bool
            如果卸载过程成功，返回True，否则返回False
            
        """
    
    print("service_1.这是my_unload_func")
    return True

# 清理方法，后端服务要把下载的文件删掉
# 参数是服务名称，必须保证和上边的服务名称一致
@cleanup_func('service_1')
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

