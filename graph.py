from enum import Enum

class State(Enum):
    MIN = 0
    MAX = 1

class Graph:
    def __init__(self, value : int, state : State, children: list['Graph'] = None) -> None:
        self.value = value
        self.state : State = state
        if children is None:
            children = []
        self.children = children

    def addChildren(self, value = 0, state: State = State.MIN) -> 'Graph':
        graph = Graph(value, state, [])
        self.children.append(graph)
        return graph