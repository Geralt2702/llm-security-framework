import PySimpleGUI as sg
from main import LLMSecurityTester
from config import OLLAMA_MODELS, OUTPUT_CONFIG

sg.theme('DarkBlue3')

layout = [
    [sg.Text('LLM Security Test Framework', font=('Arial', 20, 'bold'))],
    [sg.Text('Model:'), sg.Combo(OLLAMA_MODELS, default_value='gemma3', key='-MODEL-')],
    [sg.Checkbox('Jailbreak', default=True, key='-TEST-JAILBREAK-')],
    [sg.Checkbox('Prompt Injection', default=True, key='-TEST-INJECTION-')],
    [sg.Checkbox('Red Teaming', default=True, key='-TEST-REDTEAM-')],
    [sg.Button('Run Tests'), sg.Button('Exit')],
    [sg.Output(size=(100, 20), key='-OUTPUT-')]
]

window = sg.Window('LLM Security Framework', layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    elif event == 'Run Tests':
        try:
            model = values['-MODEL-']
            categories = []
            if values['-TEST-JAILBREAK-']: categories.append('jailbreak')
            if values['-TEST-INJECTION-']: categories.append('prompt_injection')
            if values['-TEST-REDTEAM-']: categories.append('red_teaming')
            
            print(f'Starting tests with model: {model}')
            tester = LLMSecurityTester(model=model)
            tester.run_tests(categories=categories if categories else None)
            tester.generate_html_report()
            print(f'Tests complete! Results: {len(tester.results)} tests, {len(tester.alerts)} alerts')
        except Exception as e:
            print(f'Error: {e}')

window.close()
