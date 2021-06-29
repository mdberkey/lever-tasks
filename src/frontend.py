import PySimpleGUI as sg
import src.backend as be
import pandas as pd
import os
from shutil import copy


class Frontend:
    """ frontend GUI """

    def __init__(self, backend=be.Backend(), size=(200, 100), font='Helvetica',
                 header_font='helvetica 15 underline bold', pad=[10, 10]):
        self.backend = backend
        self.size = size
        self.font = font
        self.header_font = header_font
        self.pad = pad

    def main_menu(self):
        """
        Main menu of frontend
        :return: None
        """
        tasks = self.backend.tasks

        button_col = [
            [sg.Text('Options', font=self.header_font)],
            [sg.Button('Lever Tasks', pad=self.pad)],
            [sg.Button('Export Data', pad=self.pad)],
            [sg.Button('Delete Data', pad=self.pad)],
            [sg.Button('QUIT', pad=self.pad)]
        ]

        layout = [
            [sg.Column(button_col, justification='center')],
            [sg.Text('For Info/Help: Please refer to the user manual.')],
            [sg.Text('Source Code: https://github.com/mdberkey/lever-tasks')]
        ]

        main_window = sg.Window('Lever Tasks v0.1', layout, margins=self.size, font=self.font)

        while True:
            event, values = main_window.read()
            if event == 'QUIT' or event == sg.WIN_CLOSED:
                break
            elif event == 'Export Data':
                self.export_data(tasks.keys())
            elif event == 'Delete Data':
                self.delete_data(tasks.keys())
            elif event == 'Lever Tasks':
                self.params_menu()
        main_window.close()

    def params_menu(self):
        """
        Menu for chaning parameters
        :return: None
        """
        params = self.backend.read_params()[0]
        params_col = []
        for key, value in params.items():
            if key == 'schedule':
                params_col.append([sg.Text(key, size=(25, 1)),
                                   sg.InputCombo(['Autoshape', 'FR', 'FI', 'VR', 'VI', 'DRL', 'PR'], key=key,
                                                 default_value=value)])
            else:
                params_col.append([sg.Text(key, size=(25, 1)), sg.InputText(value, key=key)])

        layout = [[sg.Column(params_col)], [sg.Button('Back to Main Menu'), sg.Button('Confirm Parameters')],
                  [sg.Text('Note: You must \'Confirm Parameters\' before starting task.')]]

        start_button = sg.Button('Start Task', disabled=True, key='ST')
        layout[1].append(start_button)

        params_window = sg.Window('Parameters', layout, margins=self.size, font=self.font)
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
                            sg.Popup('Parameter Error: Please enter date format as: \'mm/dd/yy\'', font=self.font)
                    elif key == 'schedule':
                        if not value:
                            sg.Popup('Parameter Error: Please enter a schedule.', font=self.font)
                    values[key] = [value]

                self.backend.set_params(pd.DataFrame.from_dict(values, orient='columns'))
                try:
                    start_button.update(disabled=False)
                except UnboundLocalError:
                    pass
            elif event == 'ST':
                task = self.backend.read_params()[0]['schedule']
                if self.backend.start_task(name=task):
                    sg.Popup('Task Completed.', font=self.font)
        params_window.close()

    def export_data(self, tasks):
        """
        Exports output.csv files to expored_data folder.
        :param tasks: list of tasks names
        :return:
        """
        export_tasks = []
        for dir in tasks:
            if os.path.getsize(dir + '/output.csv') == 0:
                continue
            else:
                export_tasks.append(dir)

        layout = [
            [sg.Text('Task data to be exported:', font=self.header_font, pad=self.pad)]
        ]
        if not export_tasks:
            layout.append([sg.Text('None', pad=self.pad)])
        else:
            for dir in export_tasks:
                layout.append([sg.Text(dir, pad=self.pad)])
        layout.append([sg.Button('Cancel', pad=self.pad), sg.Button('Continue', pad=self.pad)])

        window = sg.Window('Export Data', layout, font=self.font)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            elif event == 'Continue':
                os.chdir('..')
                for dir in export_tasks:
                    src = os.path.join('src', dir, 'output.csv')
                    dest = os.path.join('exported_data', dir + '_output.csv')
                    copy(src, dest)
                os.chdir('src')
                sg.Popup('Data Exported to \'exported_data\' folder.', font=self.font)
                break
        window.close()

    def delete_data(self, tasks):
        """
        Clears output.csv files from every task's folder
        :param tasks: list of task names
        :return: None
        """
        layout = [
            [sg.Text('WARNING', font=self.header_font, pad=self.pad, background_color='red')],
            [sg.Text('This will delete the following non-exported data:', font=self.header_font, pad=self.pad)]
        ]

        for dir in tasks:
            if os.path.getsize(dir + '/output.csv') == 0:
                continue
            else:
                layout.append([sg.Text(dir)])

        if len(layout) == 2:
            layout.append([sg.Text('None')])
        layout.append([sg.Button('Cancel', pad=self.pad), sg.Button('Continue', pad=self.pad)])

        window = sg.Window('Delete Data', layout, font=self.font)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            elif event == 'Continue':
                for dir in tasks:
                    data = open(dir + '/output.csv', 'w+')
                    data.close()
                sg.Popup('Data Deleted', font=self.font)
                break
        window.close()


if __name__ == '__main__':
    frontend = Frontend()
    frontend.main_menu()
