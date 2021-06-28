import PySimpleGUI as sg
import src.backend as be

class Frontend:

    def __init__(self, backend=be.Backend(), size=(500, 300), font='Helvetica',
                 header_font="helvetica 15 underline bold", pad=[5, 5]):
        self.backend = backend
        self.size = size
        self.font = font
        self.header_font = header_font
        self.pad = pad

    def main_menu(self):
        tasks = self.backend.tasks

        task_col = [[sg.Button(task, pad=self.pad)] for task in tasks.keys()]
        task_col.insert(0, [sg.Text("Tasks", font=self.header_font)])
        option_col = [
            [sg.Text("Other", font=self.header_font)],
            [sg.Button("Global Parameters", pad=self.pad)],
            [sg.Button("Export Data", pad=self.pad)],
            #[sg.Button("Quick View Data", pad=self.pad)],
            [sg.Button("Delete Data", pad=self.pad)],
            [sg.Button("QUIT", pad=self.pad)]
        ]

        layout = [
            [sg.Column(task_col), sg.VSeparator(), sg.Column(option_col)],
            [sg.Text("For Info/Help: Please refer to the user manual.")],
            [sg.Text("Source Code: https://github.com/mdberkey/lever-tasks")]
        ]

        main_window = sg.Window("Lever Tasks v0.1", layout, margins=self.size, font=self.font)

        while True:
            event, values = main_window.read()

            if event == "QUIT" or event == sg.WIN_CLOSED:
                break
            elif event == "Global Parameters":
                self.params_menu()
            elif event == "Export Data":
                self.export_data(tasks)
            elif event == "Delete Data":
                self.delete_data(tasks)
            elif event == "Quick View Data":
                self.quick_view_data(tasks)
            else:
                for task in tasks:
                    if event == task.name:
                        self.params_menu(task)
        main_window.close()

    def params_menu(self):
        pass

if __name__ == '__main__':
    frontend = Frontend()
    frontend.main_menu()
