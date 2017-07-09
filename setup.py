# coding=utf-8

"""
pycodesim
=========

A Python Code Similarity Detection Doll， just for fun.
用于计算python代码相似度的玩具。

背景
----

基于抽象语法树，有三种方法，第一种是最简单的jaccard相似度，第二种是树的编辑距离，第三种是遍历合适大小的子树计算anti-unification(不完全是)

demo
----

::

    code_sim('codes/code1.py', 'codes/code2.py', 'jaccard')
    code_sim('codes/code1.py', 'codes/code2.py', 'tree_edit')
    code_sim('codes/code1.py', 'codes/code2.py', 'fake_anti_uni')


"""

from setuptools import setup

setup(
    name='pycodesim',
    version='0.0.2',
    packages=['pycodesim'],
    url='https://github.com/inuyasha2012/pycodesim',
    license='MIT',
    author='inuyasha2012',
    author_email='inuyasha021@163.com',
    description='A Python Code Similarity Detection Doll, just for fun. ',
    long_description=__doc__,
    install_requires=['zss'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)