import time
import pandas as pd
import multiprocessing
from task_queue import TaskQueue
import autoshape.autoshape as autoshape
import fixed_ratio.fixed_ratio as fixed_ratio
import fixed_interval.fixed_interval as fixed_interval


# TODO: import other tasks


class Backend:
    """ backend functions"""

    # TODO: add other tasks to self.tasks
    def __init__(self):
        self.tasks = {
            'autoshape': autoshape,
            'fixed_ratio': fixed_ratio,
            'fixed_interval': fixed_interval,

        }
        self.task_queue = TaskQueue(50)

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
    def set_params(params_df: pd.DataFrame):
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

    def start_task(self, params=None):
        """
        Starts task specified by parameters
        """
        if not params:
            params = self.read_params()[0]
        name = params['schedule']
        length = params['session_length']

        proc = multiprocessing.Process(target=self.task_process, name='task_process', args=(name, params,))
        proc.start()
        print(f'Task timer started: {length} seconds remaining.')
        time.sleep(length)

        if proc.is_alive():
            print(f'Terminating task. {length} seconds elapsed.')
            proc.terminate()
            proc.join()

        print('Task completed.')
        return True

    def task_process(self, name: str, params: pd.DataFrame):
        """
        Helper method for start_task
        """
        self.tasks[name].main(params)

    def enqueue_task(self):
        """
        enqueues task specified by parameters
        """
        params = self.read_params()[0]
        if self.task_queue.enqueue(params):
            return True
        else:
            return False

    def start_queue(self):
        """
        Starts task Queue
        """
        for i in range(self.task_queue.size):
            self.start_task(params=self.task_queue.dequeue())
        return True

    def get_queue_size(self):
        """
        return: current size of task queue
        """
        return self.task_queue.size

    @staticmethod
    def calc_func(func: str, x: int):
        return int(eval(func))
