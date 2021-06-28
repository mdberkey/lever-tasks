import pandas as pd
import src.autoshaping.autoshaping as autoshaping


# TODO: import other tasks


class Backend:
    """ backend functions"""

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
        :return: True if task completed
        """
        self.tasks[name].main()
        return True


# TODO finish main
if __name__ == '__main__':
    backend = Backend()
    params_dict, params_df = backend.read_params()
    backend.set_params(params_df)
