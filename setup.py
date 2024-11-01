from setuptools import setup, find_packages

setup(
    name='my_package',  # 包名
    version='0.1.0',  # 版本号
    packages=find_packages(),  # 自动查找子包
    install_requires=[  # 依赖包
        # 'numpy',  # 示例依赖
    ],
    description='My sample Python package',  # 包描述
    long_description=open('README.md').read(),  # 长描述
    long_description_content_type='text/markdown',  # 描述类型
    url='https://github.com/yourusername/my_package',  # 项目地址
    author='Linmao',  # 作者
    author_email='406043808@qq.com',  # 作者邮箱
    classifiers=[  # 分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',  # Python 版本要求
)
