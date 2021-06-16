from src.backend import TaskHelper
import time


def main():
    params = TaskHelper.read_params()
    ITI = params['ITI']
    reward_num = params['reward_num']
    reward_delay = params['reward_delay']

    TaskHelper.start_light()

    length = time.time() + params['session_length']
    while time.time() < length:

        time_out = time.time() + params['time_out']
        # task loop
        while time.time() < time_out:
            TaskHelper.stim_lights()
            if TaskHelper.levers():
                time.sleep(reward_delay)
                TaskHelper.dispense_pellet(reward_num)
            TaskHelper.stim_lights(on=False)
            time.sleep(ITI)


if __name__ == '__main__':
    main()