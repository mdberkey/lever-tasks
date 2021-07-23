from task_helper import TaskHelper
import pandas as pd
import time


def main(params, testing=True):
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
    task_helper = TaskHelper(testing=testing)
    task_helper.output_ln('autoshape', output_df.keys())

    initial_trials = True
    trial_num = 1
    task_helper.start_light(on=True, testing=testing)

    start = time.time()
    while True:
        if initial_trials:
            task_helper.stim_lights(left=True, right=True, testing=testing)
            if task_helper.levers_output(left=True, right=True, testing=testing):
                try:
                    duration, lever = task_helper.levers_input(testing=testing)
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
    main(params=TaskHelper.read_params()[0])
