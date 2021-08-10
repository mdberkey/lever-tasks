import sched

import PySimpleGUI as sg
import backend as be
import pandas as pd
import os
from shutil import copy


class Frontend:
    """ frontend GUI """

    def __init__(self, backend=be.Backend(), size=(200, 100), font='Helvetica',
                 header_font='helvetica 15 underline bold', pad=(10, 10)):
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
            [sg.Button('Task Queue', pad=self.pad)],
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
            elif event == 'Task Queue':
                self.queue_menu()
        main_window.close()

    # TODO: Get names/info for DRL and PR (line 69)
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
                                   sg.InputCombo(['autoshape', 'fixed_ratio', 'fixed_interval', 'variable_ratio',
                                                  'variable_interval', 'DRL', 'PR'], key=key,
                                                 default_value=value)])
            else:
                params_col.append([sg.Text(key, size=(25, 1)), sg.InputText(value, key=key)])
        start_button = sg.Button('Start Task', disabled=True, key='ST')
        queue_button = sg.Button('Enqueue Task', disabled=True, key='QT')
        layout = [[sg.Column(params_col)], [
            sg.Button('Back to Main Menu'),
            sg.Button('Confirm Parameters'),
            start_button,
            queue_button,
        ], [sg.Text('Note: You must \'Confirm Parameters\' before starting or enqueuing a task.')]]

        params_window = sg.Window('Parameters', layout, margins=self.size, font=self.font)
        while True:
            event, values = params_window.read()

            if event == 'Back to Main Menu' or event == sg.WIN_CLOSED:
                break
            elif event == 'Confirm Parameters':
                valid = True
                for key, value in values.items():
                    if key == 'date':
                        # checks if date is proper format
                        try:
                            assert (list(map(int, value.split('/'))))
                        except ValueError:
                            sg.Popup('Parameter Error: Please enter date format as: \'mm/dd/yy\'', font=self.font)
                            valid = False
                    elif key == 'schedule':
                        if not value:
                            sg.Popup('Parameter Error: Please enter a schedule.', font=self.font)
                            valid = False
                    elif key == 'ratio_function' or key == 'interval_function':
                        # checks if functions are valid
                        try:
                            assert self.backend.calc_func(value, 1)
                        except SyntaxError:
                            sg.Popup('Parameter Error: Please enter a valid math function (with x as the variable) for ' + key)
                            valid = False

                        # checks if functions match with schedule
                        schedule = values['schedule'][0]
                        if key == 'ratio_function':
                            if 'x' in value and not schedule == 'variable_ratio':
                                sg.Popup('Parameter Error: ratio_function param: ' + value + ' is incompatible with schedule param: ' + schedule)
                                valid = False
                        elif key == 'interval_function':
                            if 'x' in value and not schedule == 'variable_interval':
                                sg.Popup('Parameter Error: interval_function param: ' + value + ' is incompatible with schedule param: ' + schedule)
                                valid = False

                    values[key] = [value]

                if valid:
                    self.backend.set_params(pd.DataFrame.from_dict(values, orient='columns'))
                    try:
                        start_button.update(disabled=False)
                    except UnboundLocalError:
                        pass
                    try:
                        queue_button.update(disabled=False)
                    except UnboundLocalError:
                        pass
            elif event == 'ST':
                if self.backend.start_task():
                    sg.Popup('Task Completed.', font=self.font)
            elif event == 'QT':
                if self.backend.enqueue_task():
                    sg.Popup('Task Enqueued.', font=self.font)
                else:
                    sg.Popup(f'Queue is full at: {self.backend.get_queue_size()}')

        params_window.close()

    def export_data(self, tasks: list):
        """
        Exports output.csv files to expored_data folder.
        :param tasks: list of tasks names
        :return: None
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

    def delete_data(self, tasks: list):
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

    def queue_menu(self):
        queue = self.backend.task_queue

        if queue.is_empty():
            queue_col = [[sg.Text('Queue is empty.')]]
        else:
            queue_col = [
                [sg.Text('Queue Size: ' + str(queue.size), font=self.font)],
                [sg.Text('Front of Queue: ' + queue.que_front()['schedule'], font=self.font)],
                [sg.Text('Back of Queue: ' + queue.que_rear()['schedule'], font=self.font)]
            ]

        layout = [[sg.Column(queue_col)], [
            sg.Button('Back to Main Menu'),
            sg.Button('Start Queue', key='SQ'),
        ], [sg.Text('Note: New tasks begin immediately after one another.')]]

        params_window = sg.Window('Task Queue', layout, margins=self.size, font=self.font)
        while True:
            event, values = params_window.read()

            if event == 'Back to Main Menu' or event == sg.WIN_CLOSED:
                break
            elif event == 'SQ':
                if queue.is_empty():
                    pass
                elif self.backend.start_queue():
                    sg.Popup('Queue Completed.', font=self.font)

        params_window.close()


if __name__ == '__main__':
    frontend = Frontend()
    frontend.main_menu()
