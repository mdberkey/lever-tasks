import PySimpleGUI as sg
import src.backend as be
import pandas as pd


class Frontend:
    """ frontend GUI """

    def __init__(self, backend=be.Backend(), size=(500, 300), font='Helvetica',
                 header_font='helvetica 15 underline bold', pad=[5, 5]):
        self.backend = backend
        self.size = size
        self.font = font
        self.header_font = header_font
        self.pad = pad

    def main_menu(self):
        tasks = self.backend.tasks
        task_col = [[sg.Button(task, pad=self.pad)] for task in tasks.keys()]
        task_col.insert(0, [sg.Text('Tasks', font=self.header_font)])
        option_col = [
            [sg.Text('Other', font=self.header_font)],
            [sg.Button('Export Data', pad=self.pad)],
            [sg.Button('Delete Data', pad=self.pad)],
            [sg.Button('QUIT', pad=self.pad)]
        ]

        layout = [
            [sg.Column(task_col), sg.VSeparator(), sg.Column(option_col)],
            [sg.Text('For Info/Help: Please refer to the user manual.')],
            [sg.Text('Source Code: https://github.com/mdberkey/lever-tasks')]
        ]

        main_window = sg.Window('Lever Tasks v0.1', layout, margins=self.size, font=self.font)

        while True:
            event, values = main_window.read()
            if event == 'QUIT' or event == sg.WIN_CLOSED:
                break
            elif event == 'Export Data':
                self.export_data(tasks)
            elif event == 'Delete Data':
                self.delete_data(tasks)
            else:
                self.params_menu(event)
        main_window.close()

    def params_menu(self, task, is_task=True):
        params = self.backend.read_params()[0]
        params_col = []
        for key, value in params.items():
            params_col.append([sg.Text(key, size=(25, 1)), sg.InputText(value, key=key)])

        layout = [
            [sg.Column(params_col)],
            [sg.Button('Back to Main Menu'), sg.Button('Confirm Parameters')],
        ]

        layout.append([sg.Text('Note: You must \'Confirm Parameters\' before starting task.')])
        start_button = sg.Button('Start Task', disabled=True, key='ST')
        layout[1].append(start_button)

        params_window = sg.Window(task + ' Parameters', layout, margins=self.size, font=self.font)
        while True:
            event, values = params_window.read()

            if event == 'Back to Main Menu' or event == sg.WIN_CLOSED:
                break
            elif event == 'Confirm Parameters':
                for key, value in values.items():
                    if key == 'date':
                        try:
                            assert (list(map(int, value.split('/'))))
                        except ValueError:
                            sg.Popup('Parameter Error: Please put date format as: \'mm/dd/yy\'', font=self.font)
                    values[key] = [value]

                self.backend.set_params(pd.DataFrame.from_dict(values, orient='columns'))
                try:
                    start_button.update(disabled=False)
                except UnboundLocalError:
                    pass
            elif event == 'ST':
                if self.backend.start_task(name=task):
                    sg.Popup('Task Completed.', font=self.font)
        params_window.close()

    def export_data(self):
        pass

    def delete_data(self):
        pass


if __name__ == '__main__':
    frontend = Frontend()
    frontend.main_menu()
