from abc import ABCMeta, abstractmethod
from collections import deque
from state import State

class Heuristic(metaclass=ABCMeta):
    def __init__(self, initial_state: 'State'):
        super().__init__()
        self.goals = deque()
        for i in range(State.MAX_ROW):
            for j in range(State.MAX_COL):
                if initial_state.goals[i][j] is not None:
                    self.goals.append((i,j))

    def h(self, state: 'State') -> 'int':
        return self.h1(state)
        # return self.h2(state)
        # return self.h3(state)

    def h1(self, state: 'State') -> 'int':
        goals = self.goals.copy()
        cost = 0
        for _ in range(len(goals)):
            goal = goals.pop()
            indexI = goal[0]
            indexJ = goal[1]
            cost = cost + abs(state.agent_row - indexI) + abs(state.agent_col - indexJ)
            goals.append((indexI,indexJ))
        return cost

    def h2(self, state: 'State') -> 'int':
        goals = self.goals.copy()
        cost = 0
        for _ in range(len(goals)):
            goal = goals.pop()
            indexI = goal[0]
            indexJ = goal[1]
            if state.boxes[indexI][indexJ] is not None and state.boxes[indexI][indexJ].lower() != state.goals[indexI][indexJ] or state.boxes[indexI][indexJ] is None:
                cost = cost + 1
            goals.append((indexI,indexJ))
        return cost

    def h3(self, state: 'State') -> 'int':
        goals = self.goals.copy()
        cost = 0
        for _ in range(len(goals)):
            goal = goals.pop()
            indexI = goal[0]
            indexJ = goal[1]
            for i in range(State.MAX_ROW):
                for j in range(State.MAX_COL):
                    if state.boxes[i][j] is not None and state.boxes[i][j].lower() == state.goals[indexI][indexJ]:
                        cost = cost + abs(i - indexI) + abs(j - indexJ)
            goals.append((indexI,indexJ))
        return cost

    @abstractmethod
    def f(self, state: 'State') -> 'int': pass

    @abstractmethod
    def __repr__(self): raise NotImplementedError


class AStar(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return state.g + self.h(state)

    def __repr__(self):
        return 'A* evaluation'


class WAStar(Heuristic):
    def __init__(self, initial_state: 'State', w: 'int'):
        super().__init__(initial_state)
        self.w = w

    def f(self, state: 'State') -> 'int':
        return state.g + self.w * self.h(state)

    def __repr__(self):
        return 'WA* ({}) evaluation'.format(self.w)


class Greedy(Heuristic):
    def __init__(self, initial_state: 'State'):
        super().__init__(initial_state)

    def f(self, state: 'State') -> 'int':
        return self.h(state)

    def __repr__(self):
        return 'Greedy evaluation'
