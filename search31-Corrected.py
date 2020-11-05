"""Search 

The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions."""

import math, random, sys, time, bisect, string
from copy import deepcopy



#______________________________________________________________________________
# Simple Data Structures: infinity, Dict, Struct
                
infinity = 1.0e400

def Dict(**entries):  
    """Create a dict out of the argument=value arguments. 
    >>> Dict(a=1, b=2, c=3)
    {'a': 1, 'c': 3, 'b': 2}
    """
    return entries

def distance(ax_ay, bx_by):
    "The distance between two (x, y) points."
    ax, ay = ax_ay
    bx, by = bx_by
    return math.hypot((ax - bx), (ay - by))

#_____________________________________________________________________________
def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)   
    else:
        x.__dict__.update(entries) 
    return x 

#______________________________________________________________________________

# Queues: Stack, FIFOQueue, PriorityQueue

class Queue:
    """Queue is an abstract class/interface. There are three types:
        Stack(): A Last In First Out Queue.
        FIFOQueue(): A First In First Out Queue.
        PriorityQueue(lt): Queue where items are sorted by lt, (default <).
    Each type supports the following methods and functions:
        q.append(item)  -- add an item to the queue
        q.extend(items) -- equivalent to: for item in items: q.append(item)
        q.pop()         -- return the top item from the queue
        len(q)          -- number of items in q (also q.__len())
    Note that isinstance(Stack(), Queue) is false, because we implement stacks
    as lists.  If Python ever gets interfaces, Queue will be an interface."""

    def __init__(self): 
        abstract

    def extend(self, items):
        for item in items: self.append(item)

def Stack():
    """Return an empty list, suitable as a Last-In-First-Out Queue."""
    return []

class FIFOQueue(Queue):
    """A First-In-First-Out Queue."""
    def __init__(self):
        self.A = []; self.start = 0
    def append(self, item):
        self.A.append(item)
    def __len__(self):
        return len(self.A) - self.start
    def extend(self, items):
        self.A.extend(items)     
    def pop(self):        
        e = self.A[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.A)/2:
            self.A = self.A[self.start:]
            self.start = 0
        return e

class PriorityQueue(Queue):
    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x)."""
    def __init__(self, order=min, f=lambda x: x):
        update(self, A=[], order=order, f=f)
    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))
    def __len__(self):
        return len(self.A)
    def pop(self):
        if self.order == min:
            return self.A.pop(0)[1]
        else:
            return self.A.pop()[1]





#______________________________________________________________________________
class Problem:
    """The abstract class for a formal problem.  You should subclass this and
    implement the method successor, and possibly __init__, goal_test, and
    path_cost. Then you will create instances of your subclass and solve them
    with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial; self.goal = goal
        
    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        abstract
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Implement this
        method if checking against a single self.goal is not enough."""
        return state == self.goal
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        abstract
#______________________________________________________________________________
    
class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""
    allNodes = []
    def __init__(self, state, parent=None, action=None, path_cost=0):
        "Create a search tree Node, derived from a parent by an action."
        update(self, state=state, parent=parent, action=action, 
               path_cost=path_cost, depth=0)
        self.__class__.allNodes.append(self)
        if parent:
            self.depth = parent.depth + 1
            
    def __repr__(self):
        return "<Node %s>" % (self.state,)
    
    def path(self):
        "Create a list of nodes from the root to this node."
        x, result = self, [self]
        count = 1
        while x.parent:
            result.append(x.parent)
            x = x.parent
        print("Nodes generated: " + str(len(self.allNodes)))
        return result

    def expand(self, problem):
        "Return a list of nodes reachable from this node. "
        return [Node(next, self, act,
                     problem.path_cost(self.path_cost, self.state, act, next))
                for (act, next) in problem.successor(self.state)]

#______________________________________________________________________________
## Uninformed Search algorithms

def tree_search(problem, fringe):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue.
    Don't worry about repeated paths to a state."""
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state):
            return node
        fringe.extend(node.expand(problem))
    return None

def breadth_first_tree_search(problem):
    "Search the shallowest nodes in the search tree first. "
    return tree_search(problem, FIFOQueue())
    
def depth_first_tree_search(problem):
    "Search the deepest nodes in the search tree first. "
    return tree_search(problem, Stack())

def graph_search(problem, fringe):
    """Search through the successors of a problem to find a goal.
    The argument fringe should be an empty queue.
    If two paths reach a state, only use the best one."""
    closed = {}
    fringe.append(Node(problem.initial))
    while fringe:
        node = fringe.pop()
        if problem.goal_test(node.state): 
            return node
        if node.state not in closed:
            closed[node.state] = True
            fringe.extend(node.expand(problem))    
    return None

def breadth_first_graph_search(problem):
    "Search the shallowest nodes in the search tree first. [p 74]"
    return graph_search(problem, FIFOQueue())
    
def depth_first_graph_search(problem):
    "Search the deepest nodes in the search tree first. [p 74]"
    return graph_search(problem, Stack())

def depth_limited_search(problem, limit=50):
    ""
    def recursive_dls(node, problem, limit):
        cutoff_occurred = False
        if problem.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            for successor in node.expand(problem):
                result = recursive_dls(successor, problem, limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result != None:
                    return result
        if cutoff_occurred:
            return 'cutoff'
        else:
            return None
    # Body of depth_limited_search:
    return recursive_dls(Node(problem.initial), problem, limit)

def iterative_deepening_search(problem):
    ""
    for depth in range(sys.maxsize):
        result = depth_limited_search(problem, depth)
        if result is not 'cutoff':
            return result

#______________________________________________________________________________
# Informed (Heuristic) Search

def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have depth-first search."""
    return graph_search(problem, PriorityQueue(min, f))

greedy_best_first_graph_search = best_first_graph_search
    # Greedy best-first search is accomplished by specifying f(n) = h(n).

def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search."""
    h = h or problem.h
    def f(n):
        return n.path_cost + h(n)
    return best_first_graph_search(problem, f)

#______________________________________________________________________________
#_____________________________________________________________________________
# The remainder of this file implements examples for the search algorithms.

#______________________________________________________________________________
# Graphs and Graph Problems

class Graph:
    """A graph connects nodes (verticies) by edges (links).  Each edge can also
    have a length associated with it.  The constructor call is something like:
        g = Graph({'A': {'B': 1, 'C': 2})   
    this makes a graph with 3 nodes, A, B, and C, with an edge of length 1 from
    A to B,  and an edge of length 2 from A to C.  You can also do:
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
    This makes an undirected graph, so inverse links are also added. The graph
    stays undirected; if you add more links with g.connect('B', 'C', 3), then
    inverse link is also added.  You can use g.nodes() to get a list of nodes,
    g.get('A') to get a dict of links out of A, and g.get('A', 'B') to get the
    length of the link from A to B.  'Lengths' can actually be any object at 
    all, and nodes can be any hashable object."""

    def __init__(self, dict=None, directed=True):
        self.dict = dict or {}
        self.directed = directed
        if not directed: self.make_undirected()

    def make_undirected(self):
        "Make a digraph into an undirected graph by adding symmetric edges."
        "tempDict used to avoid Python3 error of iterating/changing"
        tempDict = deepcopy(self.dict)
        for a in tempDict.keys():
            for (b, distance) in tempDict[a].items():
                self.connect1(b, a, distance)

    def connect(self, A, B, distance=1):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.connect1(A, B, distance)
        if not self.directed: self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        "Add a link from A to B of given distance, in one direction only."
        self.dict.setdefault(A,{})[B] = distance

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.dict.setdefault(a, {})
        if b is None: return links
        else: return links.get(b)

    def nodes(self):
        "Return a list of nodes in the graph."
        return self.dict.keys()

def UndirectedGraph(dict=None):
    "Build a Graph where every edge (including future ones) goes both ways."
    return Graph(dict=dict, directed=False)


romania = UndirectedGraph(Dict(
    A=Dict(Z=75, S=140, T=118),
    B=Dict(U=85, P=101, G=90, F=211),
    C=Dict(D=120, R=146, P=138),
    D=Dict(M=75),
    E=Dict(H=86),
    F=Dict(S=99),
    H=Dict(U=98),
    I=Dict(V=92, N=87),
    L=Dict(T=111, M=70),
    O=Dict(Z=71, S=151),
    P=Dict(R=97),
    R=Dict(S=80),
    U=Dict(V=142)))
romania.locations = Dict(
    A=( 91, 492),    B=(400, 327),    C=(253, 288),   D=(165, 299), 
    E=(562, 293),    F=(305, 449),    G=(375, 270),   H=(534, 350),
    I=(473, 506),    L=(165, 379),    M=(168, 339),   N=(406, 537), 
    O=(131, 571),    P=(320, 368),    R=(233, 410),   S=(207, 457), 
    T=( 94, 410),    U=(456, 350),    V=(509, 444),   Z=(108, 531))


class GraphProblem(Problem):
    "The problem of searching a graph from one node to another."
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def successor(self, A):
        "Return a list of (action, result) pairs."
        return [(B, B) for B in self.graph.get(A).keys()]

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A,B) or infinity)

    def h(self, node):
        "h function is straight-line distance from a node's state to goal."
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return infinity

#______________________________________________________________________________

def pprint(path):
  path.reverse()
  for e in path:
    print(e.action, e.state)
    
def pprint(path, goal):
  path.reverse()
  print("Path cost: " + str(goal.path_cost))
  for e in path:
    print(e.action, e.state)

