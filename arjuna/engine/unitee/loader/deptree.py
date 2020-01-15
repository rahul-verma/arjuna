'''
This file is a part of Test Mile Arjuna
Copyright 2018 Test Mile Software Testing Pvt Ltd

Website: www.TestMile.com
Email: support [at] testmile.com
Creator: Rahul Verma

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import abc


class TestNode(metaclass=abc.ABCMeta):

    def __init__(self, name):
        self.name = name
        self.edges = []
        self.scheduled = None

    def is_dummy(self):
        return False

    def add_edge(self, node):
        self.edges.append(node)

    def get_edges(self):
        return self.edges

    def enumerate(self):
        for edge in self.edges:
            if edge is None:
                ArjunaCore.console.display("None")
            else:
                ArjunaCore.console.display(edge.name)

class NonTestNode(TestNode):
    def __init__(self):
        super().__init__("Dummy")

    def is_dummy(self):
        return True


class DependencyTree:
    def __init__(self, names, nodes_map):
        self.name_queue = names
        self.name_set = {i for i in nodes_map}
        self.all_nodes_map = nodes_map

    def dep_exists(self, name):
        return name in self.name_set

    def get_node_count(self):
        return len(self.name_queue)

    def is_empty(self):
        return not self.name_queue

    def __iter__(self):
        return iter(self.name_queue)

    def remove_dep(self, name):
        self.name_set.remove(name)

    def remove_all_from_queue(self, names):
        self.name_queue = [i for i in self.name_queue if i not in set(names)]

    def get_node(self, name):
        return self.all_nodes_map[name]

class DepTreeBuilder:
    def __init__(self):
        self.base_node = NonTestNode()
        self.all_nodes_map = {}
        self.dependency_map = {}

        self.all_filtered_methods = set()
        self.resolved = set()
        self.unresolved = set()

    def create_node(self, name, dependency):
        node = TestNode(name)
        self.all_nodes_map[name] = node
        if dependency is not None:
            self.dependency_map[name] = [du.name for du in dependency if not du.should_ignore()]
        else:
            self.dependency_map[name] = None

    def process_dependencies(self):
        for tname in self.all_nodes_map:
            tnode = self.all_nodes_map[tname]
            tdeps = self.dependency_map[tname]
            if tdeps:
                for tdep in tdeps:
                    tnode.add_edge(self.all_nodes_map[tdep])
            self.base_node.add_edge(tnode)

    def validate(self):
        self.__resolve_deps(self.base_node)


    def __resolve_deps(self, node):
        self.unresolved.add(node)
        edges = node.get_edges()
        if edges:
            for edge in edges:
                if not edge: continue
                if edge not in self.resolved:
                    if edge in self.unresolved:
                        raise Exception("Circular reference: {} {}".format(node.name, edge.name))
                    else:
                        self.__resolve_deps(edge)

        self.resolved.add(node)
        self.unresolved.remove(node)

    def __build_dep_tree(self, scheduled_names):
        node_map = {}
        for name in scheduled_names:
            node_map[name] = TestNode(name)

        for name in scheduled_names:
            source = self.all_nodes_map[name]
            target = node_map[name]
            for edge in source.get_edges():
                if not edge: continue
                if edge.name in node_map:
                    target.add_edge(node_map[edge.name])

        return DependencyTree(scheduled_names, node_map)

    def slot_names(self, scheduled_names):
        tree = self.__build_dep_tree(scheduled_names)
        current_slot_num = 1
        slots = []
        name_slot_map = {}
        done = []

        def is_done(node):
            edges = node.get_edges()
            if edges:
                return True
            else:
                for edge in edges:
                    if not edge: continue
                    if tree.dep_exists(edge.name):
                        return False
                    else:
                        if name_slot_map[edge.name] == current_slot_num:
                            return False
                return True

        while not tree.is_empty():
            slot = []
            for name in tree:
                node = tree.get_node(name)
                dep_met = is_done(node)
                if dep_met:
                    slot.append(name)
                    name_slot_map[name] = current_slot_num
                    tree.remove_dep(name)
                    done.append(name)

            tree.remove_all_from_queue(done)
            current_slot_num += 1
            slots.append(slot)

        return slots





