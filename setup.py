from setuptools import setup, find_packages

setup(
    name='vmodel',  # 包名
    version='0.0.2',  # 版本号
    packages=find_packages(),  # 自动查找子包
    install_requires=[  # 依赖包
        # 'numpy',  # 示例依赖
    ],
    description='一个用于对所有后端模型对接的接口规范。',  # 包描述
    long_description=open('README.md').read(),  # 长描述
    long_description_content_type='text/markdown',  # 描述类型
    url='https://github.com/marlinlm/vmodel',  # 项目地址
    author='林茂',  # 作者
    author_email='406043808@qq.com',  # 作者邮箱
    classifiers=[  # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    py_modules=['vmodel.protocol','vmodel.vmodel'],
    python_requires='>=3.11',  # Python 版本要求
)
