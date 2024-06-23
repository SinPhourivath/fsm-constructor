class FSM:
    def __init__(self, states, start_state, end_states, symbols, transitions):
        self.states = states
        self.start_state = start_state
        self.final_states = end_states
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

        # Delete transitions to unreachable states
        new_transitions = {}
        for key in self.transitions:
            state, symbol = key
            next_state = self.transitions[key]
            if state in reachable:
                new_transitions[key] = next_state
        self.transitions = new_transitions


    # Method for finding equivalent state
    def mergeEquivalent(self):
        # Setup all possible combination of state
        distinguishable = {}
        for p in self.states:
            for q in self.states:
                if p < q:
                    distinguishable[(p, q)] = False

        # Mark distinguishable if one is normal and one is final state
        for p, q in distinguishable:
            if (p in self.final_states) ^ (q in self.final_states):
                distinguishable[(p, q)] = True

        # Continue marking
        

    # Method for minimizing if DFA
    def minimize(self):
        
        # Reserved for checking FSM type

        self.removeUnreachable()

        self.mergeEquivalent()



fsm_states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
fsm_start_state = 'q0'
fsm_final_states = ['q1', 'q2']
fsm_symbols = ['a', 'b']
fsm_transitions = {
    ('q0', 'a'): 'q1',
    ('q0', 'b'): 'q4',
    ('q1', 'a'): 'q4',
    ('q1', 'b'): 'q2',
    ('q2', 'a'): 'q2',
    ('q2', 'b'): 'q2',
    ('q3', 'a'): 'q0',
    ('q3', 'b'): 'q4',
    ('q4', 'a'): 'q2',
    ('q4', 'b'): 'q1',
    ('q5', 'a'): 'q1',
    ('q5', 'b'): 'q2'
}

fsm = FSM(fsm_states, fsm_start_state, fsm_final_states, fsm_symbols, fsm_transitions)

print(fsm)

fsm.isAccept("bba")

fsm.minimize()

print(fsm)