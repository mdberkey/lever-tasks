import pandas as pd


# TODO: finish class
class Task:
    """ Task class for backend """
    def __init__(self, name, params, output, script):
        self.name = name

    def read_params(self):
        pass

    def set_params(self):
        pass

    def start_task(self):
        pass

    def get_results(self):
        pass


# TODO: finish class
class TaskHelper:
    """ Helper functions for tasks"""
    @staticmethod
    def read_params():
        params = {
            'subject': 'bob',
            'date': 'mm/dd/yy',
            'code': 'rm2054',
            'initials': 'mdb',
            'schedule': 'autoshape',
            'schedule_num': 0,
            'session_length': 120,
            'time_out': 5,
            'ITI': 10,
            'reward_num': 2,
            'reward_delay': 30
        }
        return params

    @staticmethod
    def dispense_pellet(self, num=1):
        print('pellet')
        pass

    @staticmethod
    def start_light(self, on=True):
        pass

    @staticmethod
    def stim_lights(self, on=(True, True)):
        pass

    @staticmethod
    def levers(self, input_ratio=1):
        # TODO levers come out
        for i in range(input_ratio):
            # TODO await lever press
            print('lever pressed')
        return True


# TODO finish main
if __name__ == '__main__':
    print('eee')