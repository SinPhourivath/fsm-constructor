from itertools import combinations
from collections import deque
import diagram

class FSM:
    # Constructor
    def __init__(self, states, symbols, transitions, start_state, final_states):
        self.states = states
        self.symbols = symbols
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states
        self.dfa = self.is_dfa()


    # Method for checking input parameters
    def __str__(self):
        return f"States: {self.states}\n" \
               f"Start State: {self.start_state}\n" \
               f"End States: {self.final_states}\n" \
               f"Symbols: {self.symbols}\n" \
               f"Transitions: {self.transitions}"


    # Method for checking type of fsm
    def is_dfa(self):
        for (state, symbol), destinations in self.transitions.items():
            # If epsilon transition
            if symbol == '':
                return False
            # If multiple transisitons for one symbol
            if isinstance(destinations, set) and len(destinations) > 1:
                return False

        # Check if every state has a transition for every symbol
        for state in self.states:
            for symbol in self.symbols:
                if (state, symbol) not in self.transitions:
                    return False
        return True
    

    # Method for finding the next state from current state and symbol
    def transition(self, state, symbol):
        return self.transitions.get((state, symbol))
    

    # Method for finding set of all states that can be reached from current state via one or more epsilon transitions

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            if (state, '') in self.transitions:
                next_states = self.transition(state, '')
                if isinstance(next_states, str):
                    next_states = {next_states}
                for next_state in next_states:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure


    # Method for finding set of all states that can be reached from current state via a symbol
    # Method for finding set of all states that can be reached from current state via a symbol
    def move(self, states, symbol):
        next_states = set()
        for state in states:
            if (state, symbol) in self.transitions:
                next_states.add(self.transition(state, symbol))
        return next_states


    # Method for string testing
    def accept(self, string):
        # If it's a DFA then do the DFA way
        if self.dfa:
            current_state = self.start_state
            for char in string:
                if (current_state, char) in self.transitions:
                    current_state = self.transition(current_state, char)
            return current_state in self.final_states
        # IF it's a NFA then do the NFA way
        else:
            current_states = self.epsilon_closure({self.start_state})
            for char in string:
                # move() find set of all states that can be reached from current state via a symbol
                # epsilon_closure() checking more state that can be reeached from this set of state via epsilon
                current_states = self.epsilon_closure(self.move(current_states, char))
            return any(state in self.final_states for state in current_states)


    # Method for eliminating unreachable state
    def removeUnreachable(self):
        # Using Breadth First Search algorithm to find all reachable state
        reachable = [self.start_state]
        track = [self.start_state]
        while len(track) != 0:
            state = track.pop()
            for symbol in self.symbols:
                tmp = self.transition(state, symbol)
                if tmp not in reachable:
                    track.append(tmp)
                    reachable.append(tmp)

        # Delete unreachable states from the main state
        new_states = []
        for state in self.states:
            if state in reachable:
                new_states.append(state)
        self.states = new_states

        # Delete transitions from unreachable states
        new_transitions = {}
        for key in self.transitions:
            state, symbol = key
            next_state = self.transitions[key]
            if state in reachable:
                new_transitions[key] = next_state
        self.transitions = new_transitions


    # Method for finding equivalent state
    def findEquivalent(self):
        # Setup all possible combination of state
        # Note: This is not transistion table. Key are made from two states and value is boolean
        distinguishable = {}
        pairs = list(combinations(self.states, 2))
        for pair in pairs:
            distinguishable[pair] = False

        # Mark distinguishable if one is normal and one is final state
        for key in distinguishable.keys():
            p, q = key
            if (p in self.final_states) ^ (q in self.final_states):
                distinguishable[(p, q)] = True

        # Continue marking 
        iterate = True
        while iterate:
            iterate = False
            for p, q in pairs:
                if not distinguishable[(p, q)]:
                    for symbol in self.symbols:
                        p_next = self.transition(p, symbol)
                        q_next = self.transition(q, symbol)
                        if (p_next, q_next) in distinguishable and distinguishable[(p_next, q_next)]:
                            distinguishable[(p, q)] = True
                            iterate = True
                            break
        
        # Form new state
        equivalent_classes = []
        used_state = set()
        # Iterate over each state to form new state
        for p in self.states:
            if p not in used_state:
                equivalent_class = [p]
                used_state.add(p)
                for q in self.states:
                    if q not in used_state and not distinguishable[(p, q)]:
                        equivalent_class.append(q)
                        used_state.add(q)
                equivalent_classes.append(equivalent_class)
        
        return equivalent_classes
    
    
    def reconstruct(self, eq_classes):
        new_states = ['q' + str(count) for count in range(len(eq_classes))]
        new_start_state = None
        new_final_states = set()
        new_transitions = {}

        state_mapping = {}
        for i, eq_class in enumerate(eq_classes):
            for state in eq_class:
                state_mapping[state] = new_states[i]  # Map old state to new state
                if state in self.final_states:
                    new_final_states.add(new_states[i])  # If any state in the class is final, mark new state as final
                if new_start_state is None and state in self.start_state:
                    new_start_state = new_states[i]

        # Create new transition function
        for i, eq_class in enumerate(eq_classes):
            for state in eq_class:
                for symbol in self.symbols:
                    next_state = self.transition(state, symbol)  # Get the transition of the old state
                    if next_state is not None:
                        new_transitions[(new_states[i], symbol)] = state_mapping[next_state]  # Map to the new transition
               
        return FSM(new_states, self.symbols, new_transitions, new_start_state, new_final_states)

    # Method for minimizing DFA
    def minimize(self):
        if self.dfa == False:
            return

        self.removeUnreachable()

        equivalent_states = self.findEquivalent()

        minimized_fsm = self.reconstruct(equivalent_states)

        return minimized_fsm
    

    # Method for converting NFA to DFA
    def convert_to_dfa(self):

        start_state = frozenset(self.epsilon_closure({self.start_state}))
        queue = deque([start_state])
        dfa_states = set()
        dfa_transitions = {}
        dfa_final_states = set()

        while queue:
            current = queue.popleft()
            if current not in dfa_states:
                dfa_states.add(current)
                if any(state in self.final_states for state in current):
                    dfa_final_states.add(current)
                for symbol in self.symbols:
                    next_state = frozenset(self.epsilon_closure(self.move(current, symbol)))
                    dfa_transitions[(current, symbol)] = next_state
                    if next_state not in dfa_states:
                        queue.append(next_state)

        # Creating the state mapping
        state_mapping = {}
        for i, state in enumerate(dfa_states):
            state_mapping[tuple(state)] = f'q{i}'

        # Updating dfa_states
        updated_dfa_states = []
        for state in dfa_states:
            updated_dfa_states.append(state_mapping[tuple(state)])
        dfa_states = updated_dfa_states

        # Updating dfa_final_states
        updated_dfa_final_states = []
        for state in dfa_final_states:
            updated_dfa_final_states.append(state_mapping[tuple(state)])
        dfa_final_states = updated_dfa_final_states

        # Updating dfa_transitions
        updated_dfa_transitions = {}
        for (from_state, symbol), to_state in dfa_transitions.items():
            new_from_state = state_mapping[tuple(from_state)]
            new_to_state = state_mapping[tuple(to_state)]
            updated_dfa_transitions[(new_from_state, symbol)] = new_to_state
        dfa_transitions = updated_dfa_transitions

        # Updating the start state
        start_state = state_mapping[tuple(start_state)]
        
        return FSM(dfa_states, self.symbols, dfa_transitions, start_state, dfa_final_states)
    

    def draw(self):
        dfa = diagram.draw_fsm(self.states, self.symbols, self.transitions, self.start_state, self.final_states)
        dfa.render(cleanup=True)


# fsm_states = ['q0', 'q1', 'q2', 'q3', 'q4']
# fsm_start_state = 'q0'
# fsm_final_states = ['q1', 'q3']
# fsm_symbols = ['a', 'b']
# fsm_transitions = {
#     ('q0', 'a'): 'q1',
#     ('q0', 'b'): 'q1',
#     ('q1', 'a'): 'q2',
#     ('q1', 'b'): 'q2',
#     ('q2', 'a'): 'q3',
#     ('q2', 'b'): 'q3',
#     ('q3', 'a'): 'q2',
#     ('q3', 'b'): 'q2',
#     ('q4', 'a'): 'q3',
#     ('q4', 'b'): 'q2',
# }

# Why tuple? In Python, dictionary key must be immutable after creation. Also order must be preserve (current_state, symbol)
# Why set for multiple transisiton? Order doesn't matter and set is much more efficient
# Why list for other variable? List are not complicated, easy to append and pop as I will do operation on the original data