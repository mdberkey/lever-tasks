import pandas as pd
import time


class TaskHelper:
    """ helper functions for tasks"""

    @staticmethod
    def read_params():
        """
        Reads parameters from parameters.csv
        :return: parameters in dictionary and dataframe format
        """
        params_df = pd.read_csv('parameters.csv')
        params_dict = params_df.to_dict(orient='list')
        for key in params_dict.keys():
            params_dict[key] = params_dict[key][0]

        return params_dict, params_df

    @staticmethod
    def output_ln(task_dir, data_ln=''):
        """
        Writes a line of data to a task's output.csv
        :param task: task's data being recorded
        :param data_ln: new line of data being appended
        :return: None
        """
        with open(task_dir + '/output.csv', 'a+') as output_file:
            output_file.write(','.join(map(str, data_ln)) + '\n')

    @staticmethod
    def dispense_pellet(num=1):
        """
        Dispenses set number of food pellets
        :param num: number of pellets
        :return: None
        """
        #TODO: ADD hardware support for pellet dispenser
        print('pellet')

    @staticmethod
    def start_light(on):
        """
        Turns on/off start_light
        :param on: turns light on if True, off if False
        :return: None
        """
        #TODO: ADD hardware support for start light
        print('start light: ' + on)

    @staticmethod
    def stim_lights(left, right):
        """
        Turns on/off stim_lights
        :param on: (left light, right light) = (bool, bool)
        :return: None
        """
        #TODO: ADD hardware support for stim lights
        print('stim lights: ' + left + right)

    @staticmethod
    def levers_out(left, right):
        #TODO: ADD hardware support for levers out
        return True

    @staticmethod
    def await_levers(input_ratio=1):
        """
        Deploys and gets input from levers
        :param input_ratio: Input ratio for levers
        :return: lever results
        """
        #TODO: ADD hardware support for levers
        # TODO levers come out
        for i in range(input_ratio):
            # TODO await lever press
            print('lever pressed')
        return True

    @staticmethod
    def await_retrieval():
        #TODO: Await signal for pellet retreival
        return time.time()
