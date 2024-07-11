import os
import graphviz
from collections import defaultdict

def draw_fsm(states, symbols, transitions, start_state, final_states):
    dot = graphviz.Digraph(format='png')

    # Set graph layout direction
    dot.attr(rankdir='LR')

    # Add states
    for state in states:
        if state in final_states:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    # Combine transitions to the same state with different symbols
    combined_transitions = defaultdict(lambda: defaultdict(list))
    for (from_state, symbol), to_states in transitions.items():
        if isinstance(to_states, tuple):
            for to_state in to_states:
                combined_transitions[from_state][to_state].append(symbol if symbol else 'ε')
        else:
            combined_transitions[from_state][to_states].append(symbol if symbol else 'ε')

    # Add transitions
    for from_state, to_states in combined_transitions.items():
        for to_state, symbols in to_states.items():
            label = '/'.join(symbols)
            dot.edge(from_state, to_state, label=label)

    # Add start state arrow
    dot.node('', shape='none')
    dot.edge('', start_state)

    return dot
