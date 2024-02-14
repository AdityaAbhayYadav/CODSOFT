import PySimpleGUI as sg

# Function to check if a string can be converted to a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Create layout for the calculator
layout = [
    [sg.Text('Enter the First Number:'), sg.InputText(key='-NUM1-')],
    [sg.Text('Enter the Second Number:'), sg.InputText(key='-NUM2-')],
    [sg.Text('Choose the Operation:'), sg.InputCombo(('+', '-', '*', '/', '//', '**', '%'), key='-OPERATION-')],
    [sg.Button('Calculate'), sg.Button('Exit')],
    [sg.Text(size=(40, 1), key='-OUTPUT-')]
]

# Create the window
window = sg.Window('Calculator', layout)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    if event == 'Calculate':
        # Get input values
        num1 = values['-NUM1-']
        num2 = values['-NUM2-']
        operation = values['-OPERATION-']

        # Check if input values are valid floats
        if is_float(num1) and is_float(num2):
            num1 = float(num1)
            num2 = float(num2)
            
            # Perform calculation based on selected operation
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 != 0:  # Check for division by zero
                    result = num1 / num2
                else:
                    result = 'Cannot divide by zero'
            elif operation == '//':
                result = num1 // num2
            elif operation == '**':
                result = num1 ** num2
            elif operation == '%':
                result = num1 % num2
            else:
                result = 'Invalid Operation Selected!'
            
            window['-OUTPUT-'].update(f'Result: {result}')
        else:
            window['-OUTPUT-'].update('Invalid Input! Please enter valid numbers.')

# Close the window
window.close()