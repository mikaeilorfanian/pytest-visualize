from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ObjTest:  # TODO need another class method constructor for creating
    # TODO: this object from "item" which is a pytest session.items, this is for collected tests
    full_path: str
    name: str
    passed: bool
    node_id: str
    error_log: str = None
    executed: bool = False
    path_obj: Path = None

    def __post_init__(self):
        self.path_obj = Path(self.full_path)

    @classmethod
    def from_report(cls, report):
        return cls(
            full_path=report.location[0],
            name=report.location[2],
            passed=report.passed,
            node_id=report.nodeid,
            error_log=report.longrepr
        )

    @property
    def json(self):
        return {
            'singleTest': True,
            'file': False,
            'testRan': self.executed,
            'name': self.name,
            'passed': self.passed,
            'id': self.node_id,
            'errorRepr': self.error_log,
        }

    @property
    def is_at_root(self):
        return len(self.path_obj.parts) == 1

    @property
    def has_test_class(self):
        if len(self.node_id.split('::')) < 2:
            raise ValueError(f'Bad nodeId {self.node_id}')

        return len(self.node_id.split('::')) > 2

    @property
    def test_class_name(self):
        if self.has_test_class:
            return self.node_id.split('::')[1]

    @property
    def is_within_package(self):
        return len(self.path_obj.parts) > 1

    # @property
    # def py_module(self) -> Optional[str]:
    #     return self.path_obj.name if self.path_obj.name.endswith('.py') else None


class Tree:
    def __init__(self):
        self.ds: list = list()

    def add(self, test_obj: ObjTest):
        current_list = self.ds

        if test_obj.is_within_package:
            if test_obj.path_obj.parts[0] in self._names(current_list):
                pass
            else:
                current_list.append({
                    'package': True,
                    'name': test_obj.path_obj.parts[0],
                    'id': test_obj.path_obj.parts[0],
                    'children': []
                                                                                                                                                                                                                                                                                })

        if test_obj.is_at_root:
            # if test module has already been added to the test tree
            if test_obj.full_path in self._names(current_list):
                existing_node = self._find_node_by_name(current_list, test_obj.full_path)
                if test_obj.has_test_class:
                    current_list = existing_node['children']
                    # if test class has already been added to this test module
                    if test_obj.test_class_name in self._names(current_list):
                        existing_test_class_node = self._find_node_by_name(current_list, test_obj.test_class_name)
                        existing_test_class_node['children'].append(test_obj.json)

                    # if test class not in current test module already
                    else:
                        existing_node['children'].append({
                            'name': test_obj.test_class_name,
                            'testKlass': True,
                            'children': [test_obj.json],
                            'id': test_obj.test_class_name,
                        })
                else:
                    existing_node['children'].append(test_obj.json)
            else:
                self.ds.append({
                    'name': test_obj.full_path,
                    'file': True,
                    'children': [],
                    'id': 0
                })
                if test_obj.has_test_class:
                    self.ds[0]['children'].append({
                        'name': test_obj.test_class_name,
                        'testKlass': True,
                        'children': [test_obj.json],
                        'id': test_obj.test_class_name,
                    })
                else:
                    self.ds[0]['children'].append(test_obj.json)

    def _names(self, _list: list):
        return [node['name'] for node in _list]

    def _find_node_by_name(self, nodes: list, node_name: str):
        for node in nodes:
            if node['name'] == node_name:
                return node

        raise ValueError(f'Node with name {node_name} not found!')

    @property
    def json(self):
        return self.ds


def add_test_to_test_tree(report, flask_g):
    return
    if 'tests_tree' not in flask_g:
        flask_g.tests_tree = tree = []

    id_counter = 0

    if report.when == 'call':
        test = ObjTest.from_report(report)

        if len(test.is_at_root) == 1: # TODO test module at root
            if test.path_obj.name in [folder['name'] for folder in tree]:
                filter(  # START HERE
                    lambda foldr: foldr['name'] == test.path_obj.name,
                    tree
                )[0]
                
            # if test module is not already in the tree
            tree.append({
                'name': test.path_obj.name,  # TODO rename to test.module_name
                'children': [{
                    'name': test.name,
                    'singleTest': True,
                    'testRan': False,  # TODO this is ONLY for collected tests
                    'id': test.node_id,
                }],
                'file': True,
                'id': id_counter,
            })
            id_counter += 1

        else:
            current_list = tree
            for path_component in test.path_obj.parts[:-1]:
                # all of these are directories
                # so create this directory tree in tests
                folders = [folder['name'] for folder in current_list]
                existing_folder = filter(
                    lambda folder_name: folder_name == path_component,
                    folders
                )
                if len(existing_folder) > 1:
                    raise ValueError('Folder duplicated')
                elif len(existing_folder) == 1:
                    current_list = existing_folder[0]
                else:
                    current_list.append({
                        'name': path_component,
                        'children': [],
                        'directory': True,
                    })
