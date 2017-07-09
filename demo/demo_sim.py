from __future__ import print_function
from pycodesim import code_sim

print('========jaccard============')
print(code_sim('codes/code1.py', 'codes/code2.py', 'jaccard'))
print(code_sim('codes/code1.py', 'codes/code3.py', 'jaccard'))
print(code_sim('codes/code2.py', 'codes/code4.py', 'jaccard'))

print('========tree edit============')
print(code_sim('codes/code1.py', 'codes/code2.py',  'tree_edit'))
print(code_sim('codes/code1.py', 'codes/code3.py',  'tree_edit'))
print(code_sim('codes/code2.py', 'codes/code4.py',  'tree_edit'))

print('========fake anti unification============')
print(code_sim('codes/code1.py', 'codes/code2.py', 'fake_anti_uni'))
print(code_sim('codes/code1.py', 'codes/code3.py', 'fake_anti_uni'))
print(code_sim('codes/code2.py', 'codes/code4.py', 'fake_anti_uni'))
