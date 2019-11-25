from dataclasses import dataclass, field
from pathlib import Path
from random import randint
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







def generate_random_id():
    return randint(1, 1_000_000)


@dataclass
class TesstMethod:
    name: str
    node_id: str
    executed: bool
    passed: bool
    error: str

    @classmethod
    def from_report(cls, report, executed: bool):
        return cls(
            name=report.location[2],
            passed=report.passed if executed else False,
            node_id=report.nodeid,
            error=report.longrepr if executed else None,
            executed=executed,
        )

    @property
    def klass_name(self):
        parts = self.node_id.split('::')
        if len(parts) == 2:
            raise ValueError('No class detected, use TesstFunction instead?')

        return parts[1]

    @property
    def json(self):
        return {
            'name': self.name,
            'id': self.node_id,
            'isSingleTest': True,
            'wasExecuted': self.executed,
            'passed': self.passed,
            'errorRepr': self.error,
        }


class TesstFunction(TesstMethod):
    @property
    def klass_name(self):
        return None


@dataclass
class TesstKlass:
    name: str
    _id: int = field(default_factory=generate_random_id)

    def __post_init__(self):
        self.methods = list()

    def add_method(self, method: TesstMethod):
        assert method.klass_name == self.name
        self.methods.append(method)

    @property
    def json(self):
        return {
            'name': self.name,
            'id': self._id,
            'isKlass': True,
            'children': [method.json for method in self.methods]
        }


@dataclass
class TesstModule:
    name: str
    _id: int = field(default_factory=generate_random_id)
    children: list = field(default_factory=list)

    def add_function(self, func: TesstFunction):
        self.children.append(func)

    def get_or_add_klass(self, class_name: str) -> TesstKlass:
        child_found = self._find_klass_by_name(class_name)
        if child_found:
            test_class = child_found
        else:
            test_class = TesstKlass(class_name)
            self.children.append(test_class)

        return test_class

    def _find_klass_by_name(self, class_name: str) -> TesstKlass:
        for child in self.children:
            if isinstance(child, TesstKlass):
                if child.name == class_name:
                    return child

    @property
    def json(self):
        return {
            'name': self.name,
            'id': self._id,
            'isModule': True,
            'children': [child.json for child in self.children]
        }


@dataclass
class TesstPackage:
    name: str
    _id: int = field(default_factory=generate_random_id)
    children: list = field(default_factory=list)

    def get_or_create_module(self, path_to_test_module: str) -> TesstModule:
        package_name = Path(path_to_test_module).parts[0]
        if package_name != self.name:
            raise ValueError(f'Trying to add module {path_to_test_module} to the wrong package {package_name}')

        if len(Path(path_to_test_module).parts) != 2:  # this is a nested path, so sub-package should add module
            one_level_nested_path = str(Path(*Path(path_to_test_module).parts[1:]))

            for child in self.children:  # check if sub-package already exists
                if isinstance(child, TesstPackage):
                    if child.name == Path(path_to_test_module).parts[1]:

                        return child.get_or_create_module(one_level_nested_path)

            # sub-package doesn't exist
            sub_package = TesstPackage(Path(one_level_nested_path).parts[0])
            self.children.append(sub_package)
            return sub_package.get_or_create_module(one_level_nested_path)

        # not a nested path, this package should add the module
        module_name: str = Path(path_to_test_module).parts[-1]
        for child in self.children:
            if isinstance(child, TesstModule):
                if child.name == module_name:
                    return child

        test_module = TesstModule(module_name)
        self.children.append(test_module)
        return test_module

    @property
    def json(self):
        return {
            'name': self.name,
            'id': self._id,
            'isPackage': True,
            'children': [child.json for child in self.children]
        }


@dataclass
class TreeRoot:
    children: list = field(default_factory=list)

    def get_or_create_module(self, path_to_test_module: str) -> TesstModule:
        if self._module_is_at_root(path_to_test_module):
            # add TesstModule obj by self.children.append() or return existing one
            module_name = Path(path_to_test_module).parts[0]
            for child in self.children:
                if isinstance(child, TesstModule) and child.name == module_name:
                    return child

            module = TesstModule(module_name)
            self.children.append(module)
            return module

        # not at root, so see if an existing TesstPackage can be returned
        package_name = Path(path_to_test_module).parts[0]
        for child in self.children:
            if isinstance(child, TesstPackage):
                if child.name == package_name:
                    return child.get_or_create_module(path_to_test_module)

        # not an existing package so create a new TesstPackage
        package = TesstPackage(package_name)
        self.children.append(package)
        return package.get_or_create_module(path_to_test_module)

    def _module_is_at_root(self, path_to_test_module: str):
        return len(Path(path_to_test_module).parts) == 1

    @property
    def json(self):
        return [child.json for child in self.children]


def add_test_to_test_tree(report, flask_g, test_executed=True):
    if test_executed:
        if 'tests_tree' not in flask_g:
            flask_g.tests_tree = tree = TreeRoot()
        else:
            tree = flask_g.tests_tree
    else:
        if 'collected_tests_tree' not in flask_g:
            flask_g.collected_tests_tree = tree = TreeRoot()
        else:
            tree = flask_g.collected_tests_tree

    test_module_path = report.location[0]
    module = tree.get_or_create_module(test_module_path)

    if len(report.nodeid.split('::')) == 3:  # this is a test method, i.e. it's within a class
        test_method = TesstMethod.from_report(report, test_executed)
        test_class = module.get_or_add_klass(test_method.klass_name)
        test_class.add_method(test_method)
    else:  # this is a test function
        test_function = TesstFunction.from_report(report, test_executed)
        module.add_function(test_function)
