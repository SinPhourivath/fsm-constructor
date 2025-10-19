$(document).ready(function () {
    // Event listeners for states and symbols input
    $('#states, #symbols').on('input', function () {
        updateTransitionTable();
    });

    // Function to update transition table based on states and symbols input
    function updateTransitionTable() {
        const states = $('#states').val().split(',').map(s => s.trim()).filter(s => s);
        const symbols = $('#symbols').val().split(',').map(s => s.trim()).filter(s => s);

        // Clear the transition table
        $('#transition-table thead tr').empty();
        $('#transition-table tbody').empty();

        // Add headers to the transition table
        $('#transition-table thead tr').append('<th>State</th>');
        symbols.forEach(symbol => {
            $('#transition-table thead tr').append(`<th>${symbol}</th>`);
        });

        // Add rows to the transition table
        states.forEach(state => {
            const row = $('<tr></tr>');
            row.append(`<td>${state}</td>`);
            symbols.forEach(symbol => {
                row.append(`<td><select multiple class="form-control transition-select" data-state="${state}" data-symbol="${symbol}">
                    ${states.map(s => `<option value="${s}">${s}</option>`).join('')}
                </select></td>`);
            });
            $('#transition-table tbody').append(row);
        });

        $('.transition-select').select2();

        // Log the states and symbols for debugging
        console.log("States: ", states);
        console.log("Symbols: ", symbols);

        // Update start state and final states options
        updateStateOptions(states);
    }

    // Function to update start state and final states options
    function updateStateOptions(states) {
        $('#start-state, #final-states').empty();
        $('#start-state').append('<option value="">Select start state</option>');
        $('#final-states').append('<option value="">Select final states</option>');

        states.forEach(state => {
            $('#start-state').append(`<option value="${state}">${state}</option>`);
            $('#final-states').append(`<option value="${state}">${state}</option>`);
        });
    }

    // Initial call to populate the transition table and state options
    updateTransitionTable();

    $('#final-states').on('change', function () {
        const selectedState = $(this).val();
        if (selectedState) {
            addOrRemoveSelectedState(selectedState);
        }
        // Reset select value to default after adding
        $(this).val('');
    });

    // Function to add or remove selected state from container
    function addOrRemoveSelectedState(state) {
        const selectedStatesContainer = $('#selected-state');
        const existingStates = selectedStatesContainer.find('.state').map(function() {
            return $(this).text().replace(' x', '');
        }).get();

        if (existingStates.includes(state)) {
            // Remove the state if it already exists
            selectedStatesContainer.find('.state').filter(function() {
                return $(this).text().replace(' x', '') === state;
            }).remove();
            logSelectedStates();
        } else {
            // Add the state if it does not exist
            selectedStatesContainer.append(`<div class="state">${state} <span class="remove-btn">x</span></div>`);
            // Add remove functionality
            selectedStatesContainer.find('.remove-btn').off('click').on('click', function () {
                $(this).parent().remove();
                logSelectedStates();
            });
            logSelectedStates();
        }
    }

    function logSelectedStates() {
        const selectedStates = $('#selected-state').find('.state').map(function() {
            return $(this).text().replace(' x', '');
        }).get();
        console.log("Selected states: ", selectedStates);
        return selectedStates;
    }

    function collectFormData(action) {
        const states = $('#states').val().split(',').map(s => s.trim()).filter(s => s);
        const symbols = $('#symbols').val().split(',').map(s => s.trim()).filter(s => s);
        const testString = $('#testString').val();
        const startState = $('#start-state').val();
        const finalStates = logSelectedStates();
        const transitions = [];

        // Collect data from the transition table
        $('#transition-table tbody tr').each(function() {
            const state = $(this).find('td:first').text().trim();
            $(this).find('select').each(function() {
                const symbol = $(this).data('symbol');
                const targetStates = $(this).val();
                transitions.push({ state, symbol, targetStates });
            });
        });

        const formData = {
            states,
            symbols,
            startState,
            finalStates,
            transitions,
            testString,
            action  // Add action to formData
        };

        console.log("Form Data: ", JSON.stringify(formData, null, 2));
        return formData;
    }

    function sendTransitionDataToServer(data) {
        $.ajax({
            url: `http://localhost:5000/handle_form`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function (response) {
                console.log('Server response:', response);
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    }

    let action_button = null;

    $('#automata-form').submit(function (e) {
        e.preventDefault(); // Prevent the form from submitting normally

        const formData = collectFormData(action_button); // Pass the action as 'submit'

        // Send formData to Flask server via AJAX
        $.ajax({
            url: '/handle_form',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData), // Convert formData to JSON string
            success: function (response) {
                console.log('Server response:', response);
                // Handle success response if needed
            },
            error: function (error) {
                console.error('Error:', error);
                // Handle error if needed
            }
        });
    });

    // Add event listeners to each button to handle form submission
    $('#test-dfa-nfa, #convert-nfa-dfa, #test-string, #minimize-dfa').on('click', function () {
        action_button = $(this).data('action');  // Get the action from the button's data-action attribute
        const formData = collectFormData(action_button); // Pass the action to collectFormData
        sendTransitionDataToServer(formData);
    });
});
