from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/handle_form', methods=['POST'])
def handle_form():
    data = request.json
    action = data.get('action')
    states = list(data.get('states'))
    symbols = list(data.get('symbols'))
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
        # If there are multiple target state, make it a set instead
        if len(target_states) == 0:
            target_states = ''
        elif isinstance(target_states, list) and len(target_states) == 1:
            target_states = target_states[0]
        elif isinstance(target_states, list) and len(target_states) > 1:
            target_states = set(target_states)
            
        transitions[(state, symbol)] = target_states

    # Just p 
    print("Action:", action)
    print("States:", states)
    print("Symbols:", symbols)
    print("Start State:", start_state)
    print("Final States:", final_states)
    print("Test String:", test_string)
    print(transitions)
    
    # Example: Return a JSON response
    return jsonify({"message": "Form data received", "data": data})

if __name__ == '__main__':
    app.run(debug=True)
