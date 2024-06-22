class FSM:
    def __init__(self, states, start_state, end_states, symbols, transitions):
        self.states = states
        self.start_state = start_state
        self.end_states = end_states
        self.symbols = symbols
        self.transitions = transitions

    # Method for checking fsm's input argument
    def __str__(self):
        return f"States: {self.states}\n" \
               f"Start State: {self.start_state}\n" \
               f"End States: {self.end_states}\n" \
               f"Symbols: {self.symbols}\n" \
               f"Transitions: {self.transitions}"

fsm_states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
fsm_start_state = 'q0'
fsm_end_states = ['q1', 'q2']
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

fsm = FSM(fsm_states, fsm_start_state, fsm_end_states, fsm_symbols, fsm_transitions)

print(fsm)