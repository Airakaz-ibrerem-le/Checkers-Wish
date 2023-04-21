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
    
    def __repr__(self) -> str:
        self.dotgraph = "graph minmax \{\n"
        self.__id = 0
        def dfs(graph: 'Graph', parent: str):
            id = f"C_{self.__id}"
            self.dotgraph += f"\t{id} [label={graph.value}];\n"
            self.dotgraph += f"\t{parent} -- {id};"
            self.__id += 1
            for c in graph.children:
                dfs(c, id)
        
        self.dotgraph += f"\troot [label={self.value}];"
        for child in self.children:
            dfs(child, "root")
        return self.dotgraph +"\n}"