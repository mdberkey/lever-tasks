from src.task_helper import TaskHelper
import time
import pandas as pd
from random import getrandbits


def main(testing=False):
    output_df = pd.DataFrame.from_dict(
        {
            'response': [],
            'duration': [],
            'IRT': [],
            'cumulative_time': [],
            'TO_interval': [],
            'ITI': [],
            'rewarded(0/1)': [],
            'schedule': []
        }
    )
    # Header Line
    task_helper = TaskHelper()
    task_helper.output_ln('autoshape', output_df.keys())

    params = task_helper.read_params()[0]
    initial_trials = True
    trial_num = 1
    task_helper.start_light(on=True, testing=testing)

    start = time.time()
    length = time.time() + params['session_length']
    while time.time() < length:
        if initial_trials:
            task_helper.stim_lights(left=True, right=True, testing=testing)
            if task_helper.levers_output(left=True, right=True, testing=testing):
                try:
                    duration, lever = task_helper.levers_input(timeout=length - time.time(), testing=testing)
                    task_helper.dispense_pellet(num=params['reward_num'], testing=testing)
                except TimeoutError:
                    duration = None
                    print('Lever Timeout')

                output_row = {
                    'response': trial_num,
                    'duration': duration,
                    'IRT': None,
                    'cumulative_time': time.time() - start,
                    'TO_interval': params['time_out'],
                    'ITI': params['ITI'],
                    'rewarded(0/1)': params['reward_num'],
                    'schedule': 0
                }
                output_df = output_df.append(output_row, ignore_index=True)

                task_helper.output_ln('autoshape', output_df.loc[trial_num - 1])
                if task_helper.levers_output(left=False, right=False, testing=testing):
                    task_helper.stim_lights(left=False, right=False, testing=testing)
                time.sleep(params['ITI'])
                trial_num += 1


if __name__ == '__main__':
    main(testing=True)
