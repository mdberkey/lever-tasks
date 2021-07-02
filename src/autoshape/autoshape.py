from src.task_helper import TaskHelper
import time
import pandas as pd
from random import getrandbits


def main():
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
    task_helper.start_light(on=True)

    start = time.time()
    length = time.time() + params['session_length']
    while time.time() < length:
        if initial_trials:
            task_helper.stim_lights(left=True, right=True)
            if task_helper.levers_output(left=True, right=True):
                try:
                    duration = task_helper.levers_input(timeout=length)
                    task_helper.dispense_pellet()
                except TimeoutError:
                    duration = None

                output_df['response'].append(trial_num)
                output_df['duration'].append(duration)
                output_df['IRT'].append(None)
                output_df['cumulative_time'].append(time.time() - start)
                output_df['TO_interval'].append(params['time_out'])
                output_df['ITI'].append(params['ITI'])
                output_df['rewarded(0/1)'].append(1)
                output_df['schedule'].append(0)

                task_helper.output_ln('autoshape', output_df[trial_num - 1])
                if task_helper.levers_output(left=False, right=False):
                    task_helper.stim_lights(left=False, right=False)
                time.sleep(params['ITI'])
                trial_num += 1


if __name__ == '__main__':
    main()
