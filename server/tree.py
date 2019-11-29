from dataclasses import dataclass, field
from pathlib import Path
from random import randint
from typing import List, Optional, Union


def generate_random_id():
    return randint(1, 1_000_000)  # TODO: UUID would be a proper solution here


@dataclass
class TesstMethod:
    name: str
    node_id: str
    executed: bool
    passed: bool
    error: str  # ExceptionChainRepr from pytest

    @classmethod
    def from_report(cls, report, was_executed: bool):
        return cls(
            name=report.location[2],
            passed=report.passed if was_executed else False,
            node_id=report.nodeid,
            error=report.longrepr if was_executed else '',
            executed=was_executed,
        )

    @property
    def klass_name(self):
        parts = self.node_id.split('::')
        if len(parts) == 2:
            raise ValueError('No class detected, use `TesstFunction` instead?')

        if len(parts) != 3:
            raise ValueError(f'Bad nodeid: {self.node_id}')

        return parts[1]

    @property
    def json(self):
        return {
            'name': self.name,
            'id': self.node_id,
            'isSingleTest': True,
            'wasExecuted': self.executed,
            'passed': self.passed,
            'errorRepr': str(self.error),
        }


class TesstFunction(TesstMethod):
    @property
    def klass_name(self):
        raise NotImplementedError("Test functions don't are not parts of a test class! Maybe use `TesstMethod` instead?")


@dataclass
class TesstKlass:
    name: str
    _id: int = field(default_factory=generate_random_id)
    methods: List[TesstMethod] = field(default_factory=list)

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
    children: List[Union[TesstKlass, TesstFunction]] = field(default_factory=list)

    def add_function(self, func: TesstFunction):
        self.children.append(func)

    def get_or_add_klass(self, class_name: str) -> TesstKlass:
        existing_klass = self._find_klass_by_name(class_name)
        if existing_klass:
            test_class = existing_klass
        else:
            test_class = TesstKlass(class_name)
            self.children.append(test_class)

        return test_class

    def _find_klass_by_name(self, class_name: str) -> Optional[TesstKlass]:
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
    children: List[Union['TesstPackage', TesstModule]] = field(default_factory=list)

    def get_or_create_module(self, path_to_test_module: str) -> TesstModule:
        test_module_path = Path(path_to_test_module)
        package_name = test_module_path.parts[0]
        if package_name != self.name:
            raise ValueError(f'Trying to add module {path_to_test_module} to the wrong package {package_name}')

        if len(test_module_path.parts) != 2:  # this is a nested path, so sub-package should add module
            nested_path = str(Path(*test_module_path.parts[1:]))

            for child in self.children:  # check if sub-package already exists
                if isinstance(child, TesstPackage):
                    if child.name == test_module_path.parts[1]:
                        return child.get_or_create_module(nested_path)

            # sub-package doesn't exist
            sub_package = TesstPackage(Path(nested_path).parts[0])
            self.children.append(sub_package)
            return sub_package.get_or_create_module(nested_path)

        # not a nested path, this package should add the module
        module_name: str = test_module_path.parts[-1]
        for child in self.children:  # check if module already exists
            if isinstance(child, TesstModule):
                if child.name == module_name:
                    return child

        # module doesn't exist so create it
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
    children: List[Union[TesstModule, TesstPackage]] = field(default_factory=list)

    def get_or_create_module(self, path_to_test_module: str) -> TesstModule:
        if self._module_is_at_root(path_to_test_module):
            # add TesstModule obj to children or return existing one
            module_name = Path(path_to_test_module).parts[0]
            for child in self.children:  # check if module already exists
                if isinstance(child, TesstModule) and child.name == module_name:
                    return child

            # create module since it doesn't exist
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

    def _module_is_at_root(self, path_to_test_module: str) -> bool:
        return len(Path(path_to_test_module).parts) == 1

    @property
    def json(self):
        return [child.json for child in self.children]


def add_test_to_test_tree(report, flask_g, was_executed=True):
    """
    This function is used during test collection and execution.
    It builds a tree structure suitable for rendering on the front-end.
    It also keeps count of how many tests were collected or executed.
    All this data is stored in flask's g object which stays the same between calls to the different
    pytest hooks we're using. `g` is a per request object, meaning it won't get mixed up with `g`s in other requests.
    """
    if was_executed:
        if 'tests_tree' not in flask_g:
            flask_g.tests_tree = tree = TreeRoot()
        else:
            tree = flask_g.tests_tree

        if 'executed_tests_counter' not in flask_g:
            flask_g.executed_tests_counter = 0
    else:
        if 'collected_tests_tree' not in flask_g:
            flask_g.collected_tests_tree = tree = TreeRoot()
        else:
            tree = flask_g.collected_tests_tree

    test_module_path = report.location[0]
    module = tree.get_or_create_module(test_module_path)

    if len(report.nodeid.split('::')) == 3:  # this is a test method, i.e. it's within a class
        test_method = TesstMethod.from_report(report, was_executed)
        test_class = module.get_or_add_klass(test_method.klass_name)
        test_class.add_method(test_method)
    else:  # this is a test function
        test_function = TesstFunction.from_report(report, was_executed)
        module.add_function(test_function)

    if was_executed:
        flask_g.executed_tests_counter += 1
