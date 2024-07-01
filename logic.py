from itertools import combinations

class FSM:
    def __init__(self, states, start_state, final_states, symbols, transitions):
        self.states = states
        self.start_state = start_state
        self.final_states = final_states
        self.symbols = symbols
        self.transitions = transitions


    # Method for checking fsm's input argument
    def __str__(self):
        return f"States: {self.states}\n" \
               f"Start State: {self.start_state}\n" \
               f"End States: {self.final_states}\n" \
               f"Symbols: {self.symbols}\n" \
               f"Transitions: {self.transitions}"
    

    # Method for finding the next state
    def transition(self, state, symbol):
        return self.transitions.get((state, symbol))


    # Method for string testing
    def isAccept(self, test_string):
        current_state = self.start_state
        for char in test_string:
            current_state = self.transition(current_state, char)

        if current_state in self.final_states:
            print("String accepted")
        else:
            print("String rejected")


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

        # Delete unreachable states from the main sate
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

        # Continue marking untill no state 
        iterate = True
        while iterate:
            iterate = False
            for p, q in pairs:
                if not distinguishable[(p, q)]:
                    for symbol in self.symbols:
                        p_next = self.transition(p, symbol)
                        q_next = self.transition(q, symbol)
                        if p_next != q_next and distinguishable[(p_next, q_next)]:
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
                available_state = list(set(self.states) - used_state)
                for q in available_state:
                    # Check if state q is equivalent to state p
                    if distinguishable[(p, q)] == True:
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
                    next_state = self.transitions[(state, symbol)]  # Get the transition of the old state
                    new_transitions[(new_states[i], symbol)] = state_mapping[next_state]  # Map to the new transition
               
        # Return the new FSM
        return FSM(new_states, new_start_state, new_final_states, self.symbols, new_transitions)

    # Method for minimizing if DFA
    def minimize(self):
        
        # Reserved for checking FSM type

        self.removeUnreachable()

        equivalent_states = self.findEquivalent()

        minimized_fsm = self.reconstruct(equivalent_states)

        return minimized_fsm


fsm_states = ['q0', 'q1', 'q2', 'q3', 'q4']
fsm_start_state = 'q0'
fsm_final_states = ['q1', 'q3']
fsm_symbols = ['a', 'b']
fsm_transitions = {
    ('q0', 'a'): 'q1',
    ('q0', 'b'): 'q1',
    ('q1', 'a'): 'q2',
    ('q1', 'b'): 'q2',
    ('q2', 'a'): 'q3',
    ('q2', 'b'): 'q3',
    ('q3', 'a'): 'q2',
    ('q3', 'b'): 'q2',
    ('q4', 'a'): 'q3',
    ('q4', 'b'): 'q2'
}

fsm = FSM(fsm_states, fsm_start_state, fsm_final_states, fsm_symbols, fsm_transitions)

print(fsm)
print()

new_fsm = fsm.minimize()

print(new_fsm)