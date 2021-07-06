import pandas as pd
import autoshape.autoshape
# TODO: import other tasks


class Backend:
    """ backend functions"""

    # TODO: add other tasks to self.tasks
    def __init__(self):
        self.tasks = {
            'autoshape': autoshape,
        }

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
        :return: True if task completed
        """
        self.tasks[name].main()
        return True
