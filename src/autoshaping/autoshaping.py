from src.task_helper import TaskHelper
import time
import pandas as pd
from random import getrandbits


def main():
    output_df = pd.DataFrame.from_dict(
        {
            'response': [1],
            'duration': [0.00],
            'IRT': [0.00],
            'cumulative_time': [00.00],
            'TO_interval': [0],
            'ITI': [0.00],
            'rewarded(0/1)': [0],
            'schedule': [0]
        }
    )
    # Header Line
    TaskHelper.output_ln('autoshaping', output_df.keys())

    params = TaskHelper.read_params()[0]
    TaskHelper.start_light(True)

    length = time.time() + params['session_length']
    while time.time() < length:
        right_side = bool(getrandbits(1))
        TaskHelper.stim_lights(not right_side, right_side)
        TaskHelper.levers_out(not right_side, right_side)

        time_out = time.time() + params['time_out']
        # task loop
        while time.time() < time_out:
            if TaskHelper.await_levers():
                time.sleep(params['reward_delay'])
                TaskHelper.dispense_pellet(params['reward_num'])
                break

        time.sleep(params['ITI'])
    TaskHelper.start_light(False)


if __name__ == '__main__':
    main()
