from setuptools import setup

setup(
    name='pycodesim',
    version='0.0.1',
    packages=['pycodesim'],
    url='https://github.com/inuyasha2012/pycodesim',
    license='MIT',
    author='inuyasha2012',
    author_email='inuyasha021@163.com',
    description='A Python Code Similarity Detection Doll, just for fun. ',
    long_description=open('doc/index.rst').read(),
    install_requires=['zss'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)