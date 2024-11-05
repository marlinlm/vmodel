# vmodel
一个用于对所有后端模型对接的接口规范。


## 后端服务的适配
目前有两种协议：标准协议及简化协议

### 标准协议（standard_protocol）
规定了每个后端服务必须实现以下接口:
-	信息获取接口（@get_service_info_func）：可在获取后端服务的名称、服务功能描述、资源需求以及功能列表。功能列表包括功能列表名称、接口映射方法、功能描述及包含参数具体定义和描述的参数列表。其中功能列表中的每一项为应用程序可单独使用的服务，其功能描述及参数信息将作为应用程序进行动态任务规划的基础。服务的资源需求信息包含cpu、内存、显卡等资源的限制，用于后端服务管理。

- 初始化接口（@prepare_func）：初始化阶段为后端服务检测相应资源、准备数据集和模型等操作。

-	加载接口（@load_func）：将模型加载到内存，加载完成后，将暴露业务服务接口。未加载时，业务服务接口不可用。

-	业务服务接口（@service_func）：根据后端服务提供的接口名称，实现对后端服务的实际调用。该接口只有在加载成功后才可使用。

-	自动测试接口（@test_func）：后端服务应使用测试数据集运行自动测试程序，并返回测试结果。自动测试会在加载完成后自动触发。如果自动测试接口返回测试失败的结果，该服务会被标记为无法使用。该接口只有在加载成功后才可使用。

- 卸载接口（@unload_func）：将后端服务的模型从内存中卸载，但保留已保存的数据文件，卸载后业务服务接口需要重新加载才可使用。

-	清理接口（@cleanup_func）：删除服务所下载的所有文件。

### 简化协议（simpler_protocol）
仅要求服务实现以下接口：
- 信息获取接口（@get_service_info_func）
- 初始化接口（@prepare_func）
- 业务服务接口（@service_func）
- 清理接口（@cleanup_func）

使用简化协议，初始化接口需要负责模型及数据文件下载及模型数据加载到内存。清理接口需要卸载内存及删除文件。

### 极简协议（wabi_protocol）
仅要求服务实现以下接口：
- 信息获取接口（@get_service_info_func）
- 业务服务接口（@service_func）

使用极简协议，需要在业务服务接口实现所有模型加载、数据加载及卸载等逻辑。

## 安装

直接克隆代码：

https://github.com/marlinlm/vmodel.git
安装包就在 vmodel/dist/下。

或者下载安装包：

https://github.com/marlinlm/vmodel/blob/main/dist/vmodel-0.0.1-py3-none-any.whl

安装 
```bash
python -m pip install dist/vmodel-0.0.1-py3-none-any.whl --force-reinstall
```

## 如何编写后端服务接口
实现协议的方式需要按协议要求编写方法，并为方法加上协议里相关方法的@注解。注解的方式如下
```python
# 这是一个标准协议的实例
from vmodel.protocol.standard_protocol import cleanup_func, get_service_info_func, load_func, prepare_func, test_func, unload_func, service_func

# 如果使用简化协议 请导入 
# vmodel.from protocol.simpler_protocol import cleanup_func, get_service_info_func, prepare_func, service_func

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
```
标准协议的使用样例可以在 ./service_example/service_example.py中找到。

简化协议的样例在 ./service_example/service_example_2.py。

同一个后端服务只能使用一种协议。使用不同协议的后端服务可以一起用。

## 如何使用vmodel

```python
# 导入vmodel包
from vmodel.vmodel import VModel
    
if __name__ == '__main__':
    # 创建VModel类
    vm = VModel( # 传入所有服务的清单（主要是包名）
                [
                    {
                        'package':'vmodel.service_example.service_example',
                    },{
                        'package':'vmodel.service_example.service_example_2'
                    }
                ])
    # 调用run_and_dump方法，第一个参数是服务名，第二个参数是方法名，第三个参数是以dict格式表示的接口调用参数。注意dict里的key要与服务接口的参数名保持一致。
    print('调用服务完成，结果：',vm.run_and_dump('service_1', 'func_1', {'a':1,'b':2}))
    print('调用服务完成，结果：',vm.run_and_dump('service_2', 'func_1', {'a':1,'b':2}))
```
