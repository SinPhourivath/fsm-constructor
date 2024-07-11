from flask import Flask, render_template, request, jsonify
import logic

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/handle_form', methods=['POST'])
def handle_form():
    data = request.json
    action = data.get('action')
    states = list(data.get('states'))

    # Don't need epsilon
    symbols = list(data.get('symbols'))
    symbols = [s for s in symbols if 'epsilon' not in s]

    start_state = data.get('startState')
    final_states = list(data.get('finalStates'))
    test_string = data.get('testString')
    transitions_data = data.get('transitions', [])

    # Process transitions data from JSON index into a dictionary
    transitions = {}
    for transition in transitions_data:
        state = str(transition['state'])
        symbol = str(transition['symbol'])
        target_states = transition['targetStates']

        # Convert target states into a normal string because it will be a list by default from JSON
        # If there are multiple target state, make it a tuple instead
        if len(target_states) == 0:
            continue
        elif isinstance(target_states, list) and len(target_states) == 1:
            target_states = target_states[0]
        elif isinstance(target_states, list) and len(target_states) > 1:
            target_states = tuple(target_states)
        
        if symbol == 'epsilon':
            transitions[(state, '')] = target_states
        else:
            transitions[(state, symbol)] = target_states

    
    fsm = logic.FSM(states, symbols, transitions, start_state, final_states)

    
    match action:
        case 'test-dfa-nfa':
            result = fsm.is_dfa()
            if result:
                print("This is DFA")
            else:
                print("This is NFA")
        case 'test-string':
            result = fsm.accept(test_string)
            print(result)
        case 'convert-nfa-dfa':
            dfa = fsm.convert_to_dfa()
            dfa.draw()
        case 'minimize-dfa':
            mini = fsm.convert_to_dfa()
            mini = mini.minimize()
            mini.draw()

    graph_url = '/Diagraph.gv.png'  # Generate your graph image and save it
    message = f'Action {action} performed successfully.'

    # # Print for debugging purpose
    # print("Action:", action)
    # print("States:", states)
    # print("Symbols:", symbols)
    # print("Start State:", start_state)
    # print("Final States:", final_states)
    # print("Test String:", test_string)
    # print(transitions)
    
    # Return a JSON response
    return jsonify({
        'graphUrl': graph_url,
        'message': message
    })

if __name__ == '__main__':
    app.run(debug=True)
