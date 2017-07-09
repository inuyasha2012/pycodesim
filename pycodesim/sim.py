# coding=utf-8
import ast
from collections import deque
from zss import Node, simple_distance


def _jaccard_distance(self):
    # jaccard相似度
    node_list1, node_list2 = self._get_node_lists()
    node_set1 = set(node_list1)
    node_set2 = set(node_list2)
    return 1.0 * len(node_set1 & node_set2) / len(node_set1 | node_set2)


def _fake_anti_uni_distance(node1, node2):
    stack1 = deque([node1])
    stack2 = deque([node2])
    same = 0
    diff = 0
    while stack1 or stack2:
        if stack1:
            _node1 = stack1.popleft()
            if type(_node1).__name__ == 'Load':
                try:
                    _node1 = stack1.popleft()
                except IndexError:
                    _node1 = None
        else:
            _node1 = None
        if stack2:
            _node2 = stack2.popleft()
            if type(_node2).__name__ == 'Load':
                try:
                    _node2 = stack2.popleft()
                except IndexError:
                    _node2 = None
        else:
            _node2 = None
        if type(_node1).__name__ == type(_node2).__name__:
            same += 1
        else:
            diff += 1
        if _node1 and _node2:
            stack1.extend(ast.iter_child_nodes(_node1))
            stack2.extend(ast.iter_child_nodes(_node2))
    return 1.0 * same / (same + diff)


def _tree_edit_distance(node1, node2):

    def get_dtc_tree(node):
        distance_node = Node(type(node).__name__)
        tree_size = _dfs(node, distance_node)
        return distance_node, tree_size

    distance_node1, tree_size1 = get_dtc_tree(node1)
    distance_node2, tree_size2 = get_dtc_tree(node2)
    distance = simple_distance(distance_node1, distance_node2)
    return 1 - 1.0 * distance / max(tree_size1, tree_size2)


def _dfs(root, dtc_node=None):
    _tree_size = 0
    nodes = ast.iter_child_nodes(root)
    for _node in nodes:
        if type(root).__name__ == 'Load':
            continue
        _tree_size += 1
        if dtc_node is not None:
            _dtc_node = Node(type(_node).__name__)
            dtc_node.addkid(_dtc_node)
        else:
            _dtc_node = None
        _tree_size += _dfs(_node, _dtc_node)
    return _tree_size


def _bfs(root, mass):
    stack = deque([root])
    big_nodes = []
    while stack:
        node = stack.popleft()
        node_name = type(node).__name__
        if node_name == 'Load':
            continue
        distance_node = Node(node_name)
        tree_size = _dfs(node, distance_node)
        if tree_size >= mass:
            big_nodes.append(node)
        stack.extend(ast.iter_child_nodes(node))
    return big_nodes


class _NodeList(ast.NodeVisitor, list):

    #  深度优先遍历抽象语法树保存到列表

    def visit_Load(self, node):
        pass

    def visit_Name(self, node):
        self.append('Name')

    def generic_visit(self, node):
        self.append(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)


class _CodeSim:

    def __init__(self, file_name1, file_name2):
        with open(file_name1) as f:
            self._code1 = f.read()
        with open(file_name2) as f:
            self._code2 = f.read()

    def _get_node_lists(self):
        node1, node2 = self._get_nodes()
        node_list1, node_list2 = _NodeList(), _NodeList()
        node_list1.generic_visit(node1)
        node_list2.generic_visit(node2)
        return node_list1, node_list2

    @property
    def fake_anti_uni_distance(self):
        node1, node2 = self._get_nodes()
        root1_size = _dfs(node1)
        root2_size = _dfs(node2)
        mass = min(root1_size, root2_size) / 3
        sub_node1_list = _bfs(node1, mass)
        sub_node2_list = _bfs(node2, mass)
        sims = []
        for sub_node1 in sub_node1_list:
            for sub_node2 in sub_node2_list:
                sims.append( _fake_anti_uni_distance(sub_node1, sub_node2))
        return max(sims)

    def _get_nodes(self):
        node1, node2 = ast.parse(self._code1), ast.parse(self._code2)
        return node1, node2

    @property
    def jaccard_distance(self):
        # jaccard相似度
        node_list1, node_list2 = self._get_node_lists()
        node_set1 = set(node_list1)
        node_set2 = set(node_list2)
        return 1.0 * len(node_set1 & node_set2) / len(node_set1 | node_set2)

    @property
    def tree_edit_distance(self):
        node1, node2 = self._get_nodes()
        return _tree_edit_distance(node1, node2)


def code_sim(file_name1, file_name2, method='tree_edit'):
    if method not in ('jaccard', 'tree_edit', 'fake_anti_uni'):
        raise ValueError('method must be jaccard or tree_edit or fake_anti_uni')
    return getattr(_CodeSim(file_name1, file_name2), method + '_distance')