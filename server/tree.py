from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ObjTest:
    full_path: str
    name: str
    passed: bool
    node_id: str
    path_obj: Path

    def __post_init__(self):
        self.path_obj = Path(self.full_path)

    @property
    def json(self):
        return {
            'fullPath': test.full_path,
            'name': test.name, 
            'passed': test.passed,
            'nodeId': test.node_id,
        }

    @property
    def py_module(self):
        return self.path_obj.name if self.path_obj.name.endswith('.py') else None


def add_test_to_test_tree(report, flask_g):
    if 'tests_tree' not in flask_g:
        flask_g.tests_tree = tree = []

    id_counter = 0

    if report.when == 'call':
        test = ObjTest(  # TODO add ObjTest.from_report class method constructor
            full_path=report.location[0], 
            name=report.location[2], 
            passed=report.passed, 
            node_id=report.nodeid,
        )

        if len(test.path_obj.parts) == 1: # TODO test module at root
            if test.path_obj.name in [folder['name'] for folder in current_list]:
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
                        'id': id_counter
                    })
                    id_counter += 1
