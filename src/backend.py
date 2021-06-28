import pandas as pd
import src.autoshaping as autoshaping


# TODO: import other tasks


class Backend:
    """ Class for backend """

    # TODO: add other tasks to self.tasks
    def __init__(self):
        self.tasks = {
            'autoshaping': autoshaping,
        }

    @staticmethod
    def read_params():
        """
        Calls TaskHelper.read_params() function
        :return: TaskHelper.read_params() return value
        """
        return TaskHelper.read_params()

    @staticmethod
    def set_params(params_df):
        """
        Writes new parameters to parameters.csv
        :param params_df: New parameters dataframe
        :return: None
        """
        params_df.to_csv('parameters.csv', index=None)

    @staticmethod
    def read_output(name):
        """
        Reads the output of a specified task
        :param name: name of task
        :return: output in dictionary and dataframe formats
        """
        output_df = pd.read_csv(name + '/output.csv')
        output_dict = output_df.to_dict(orient='list')
        for key in output_dict.keys():
            output_dict[key] = output_dict[key][0]

        return output_dict, output_df

    def start_task(self, name):
        """
        Starts specified task
        :param name: Name of task dir and .py file
        :return: None
        """
        self.tasks[name].main()


# TODO: finish class
class TaskHelper:
    """ Helper functions for tasks"""

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
    def dispense_pellet(num=1):
        """
        Dispenses set number of food pellets
        :param num: number of pellets
        :return: None
        """
        #TODO: ADD hardware support for pellet dispenser
        print('pellet')

    @staticmethod
    def start_light(on=True):
        """
        Turns on/off start_light
        :param on: turns light on if True, off if False
        :return: None
        """
        #TODO: ADD hardware support for start light
        print('start light: ' + on)

    @staticmethod
    def stim_lights(on=(True, True)):
        """
        Turns on/off stim_lights
        :param on: (left light, right light) = (bool, bool)
        :return: None
        """
        #TODO: ADD hardware support for stim lights
        print('stim lights:' + on)

    @staticmethod
    def levers(input_ratio=1):
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


# TODO finish main
if __name__ == '__main__':
    backend = Backend()
    params_dict, params_df = backend.read_params()
    backend.set_params(params_df)
