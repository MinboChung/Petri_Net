#########################################################################
#                                                                       #
#       Title: petri_net.py                                             #
#       Written by: Minbo Chung                                         #
#       Written in: 2023-09-21                                          #
#       Updated by: ---                                                 #
#       Updated in: ---                                                 #
#                                                                       #
#########################################################################

# TODO: Maybe add classes for places, transitions, and arcs
# Maybe also implement this class as an abstracted class so I can give examples of nets.
# Try run CPN to understand Petri nets

# from abc import ABC, abstractmethod

# class Node(ABC):
#     def __init__(self, name, type):
#         ...

# class Place(Node):
#     ...

# class Transition(Node):
#     ...
import pprint

pp = pprint.PrettyPrinter(indent=6)


class PetriNet:
    """
        Definition 1 (Petri Net): A Petri net is a triple (P, T, F):
            - P is a finite set of places
            - T is a finite set of transitions (P intersection T = An empty set)
            - F is subset of (P X T) Union (T X P) nad it is a set of arcs
    """
    def __init__(self):
        self.P = {}
        self.T = {}
        self.F = []
        # For Boundedness
        self.k = 0

    def append_p(self, p_name, token=0):
        if p_name not in self.P:
            self.P[p_name] = token
        else:
            print(f"append_place: {p_name} already exists in P. Try another name.")
    
    def append_t(self, t_name):
        if t_name not in self.T:
            # Not enabled
            self.T[t_name] = False
        else:
            # Technically you can add a duplicated name but for good practice purpose.
            print(f"append_transitions: {t_name} already exists in T. Try another name.")
    
    def append_arc(self, n_a, n_b, weight=1):
        # arc node = (node_A -> node_B)
        # weight meaning how many arcs within nodes
        arc = (n_a, n_b, weight)
        self.F.append(arc)
    
    def relations_exist(self, t_name):
        """
            We assume that we can only fire a token if the transition has its input place.

            Return: Concluding whether it is possible to fire, and the relations that are able to fire
        """
        relations_exist = False
        if t_name in self.T:
            result = [arc for arc in self.F if arc[0] == t_name or arc[1] == t_name]
            if result:
                print(f"can_fire: {t_name} exist in {result} and thus for F.")
                relations_exist = True
            else:
                print(f"can_fire: {t_name} does not exist in F.")

        else:
            print(f"can_fire: {t_name} doesn't exist in T.")

        return relations_exist, result

    def fire_transition(self, t_name):
        if t_name in self.T:
            relations_exist, F = self.relations_exist(t_name)
            if relations_exist:
                cons_relation = [p for (p, t, w) in F if t == t_name]
                prod_relation = [p for (t, p, w) in F if t == t_name]
                p_cons = cons_relation[0]
                p_prod = prod_relation[0]

                num_token_in_cons_p = self.P[p_cons]

                if num_token_in_cons_p > 0:
                    self.P[p_cons] -= 1
                    self.P[p_prod] += 1
                    self.T[t_name] = True
                else:
                    print(f"fire_transition: {p_cons} has no token.")
                
            else:
                print(f"fire_transition: Unable to fire token via {t_name}")            
        else:
            print(f"fire_transition: {t_name} does not exist in T.")

    def add_token(self, p_name, num_token_to_add=1):
        if p_name in self.P:
            self.P[p_name] += num_token_to_add
        else:
            print(f"add_token: {p_name} does not exist in P.")
    
    def display_net(self):
        print("Current state M:\n")
        pp.pprint(f"Set of places       = {self.P}")
        pp.pprint(f"Set of transitions  = {self.T}")
        pp.pprint(f"Set of arcs         = {self.F}")