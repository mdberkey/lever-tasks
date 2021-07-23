import pandas as pd
import time
from gpiozero import LED, Motor, Button, GPIOPinMissing
from random import randint


class TaskHelper:
    """ helper functions for tasks"""

    def __init__(self, testing=True):
        if testing:
            self.io_dict = {}
        else:
            self.io_dict = {
                'feeder': Motor(forward=4),
                'start_led': LED(27),
                'left_led': LED(21),
                'right_led': LED(13),
                'left_lev_output': Motor(forward=23, backward=22),
                'right_lev_output': Motor(forward=24, backward=25),
                'left_lev_input': Button(12),
                'right_lev_input': Button(5)
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
    def output_ln(task_dir, data_ln=''):
        """
        Writes a line of data to a task's output.csv
        :param task: task's data being recorded
        :param data_ln: new line of data being appended
        :return: None
        """
        with open(task_dir + '/output.csv', 'a+') as output_file:
            output_file.write(','.join(map(str, data_ln)) + '\n')

    def dispense_pellet(self, num=1, testing=False):
        """
        Dispenses set number of food pellets
        :param num: number of pellets
        :param testing: allows testing of tasks with assumption that hardware works
        :return: None
        """
        if testing:
            for i in range(num):
                print('pellet')
        else:
            # TODO: test hardware support for pellet dispenser
            for i in range(num):
                self.io_dict['feeder'].forward()
                print('pellet')

    def start_light(self, on, testing=False):
        """
        Turns on/off start_light
        :param on: turns light on if True, off if False
        :param testing: allows testing of tasks with assumption that hardware works
        :return: None
        """
        if testing:
            if on:
                print('start light: on')
            else:
                print('start light: off')
        else:
            # TODO: test hardware support for start light
            light = self.io_dict['start_led']
            if on:
                light.on()
                print('start light: on')
            else:
                light.off()
                print('start light: off')

    def stim_lights(self, left, right, testing=False):
        """
        Turns on/off stim_lights
        :param left: left light on if true
        :param right: right light on if true
        :param testing: allows testing of tasks with assumption that hardware works
        :return: None
        """
        if testing:
            if left:
                print('left light: on')
            else:
                print('left light: off')

            if right:
                print('right light: on')
            else:
                print('right light: off')
        else:
            # TODO: test hardware support for stim lights
            left_light = self.io_dict['left_led']
            right_light = self.io_dict['right_led']
            if left:
                left_light.on()
                print('left light: on')
            else:
                left_light.off()
                print('left light: off')

            if right:
                right_light.on()
                print('right light: on')
            else:
                right_light.off()
                print('right light: off')

    def levers_output(self, left, right, testing=False):
        """
        Deploys/retracts levers
        :param left: left lever out if true
        :param right: right lever out if true
        :param testing: allows testing of tasks with assumption that hardware works
        :return: True if successful, false otherwise
        """
        if testing:
            if left:
                print('left lever: out')
            else:
                print('left lever: in')

            if right:
                print('right lever: out')
            else:
                print('right lever: in')
        else:
            # TODO: test hardware support for levers out
            left_lever = self.io_dict['left_lev_output']
            right_lever = self.io_dict['right_lev_output']
            if left:
                left_lever.foward()
                print('left lever: out')
            else:
                left_lever.backward()
                print('left lever: in')

            if right:
                right_lever.forward()
                print('right lever: out')
            else:
                right_lever.backward()
                print('right lever: in')

        return True

    def levers_input(self, timeout=900, ratio=1, testing=False):
        """
        Deploys and gets input from levers
        :param timeout: time until lever is retracted and counted as not pressed
        :param ratio: Input ratio for levers
        :param testing: allows testing of tasks with assumption that hardware works
        :return: lever results
        """
        if testing:
            counter = 0
            timeout = time.time() + timeout
            while time.time() < timeout:
                time.sleep(randint(0, 4))
                key = 'h'
                # key = input('Awaiting lever press: ')
                if key == 'h':
                    counter += 1
                    if counter >= ratio:
                        return randint(0, 5), 0
                elif key == 'l':
                    counter += 1
                    if counter >= ratio:
                        return randint(0, 5), 1
            raise TimeoutError
        else:
            left_lever = self.io_dict['left_lev_output']
            right_lever = self.io_dict['right_lev_output']
            counter = 0
            timeout = time.time() + timeout
            while time.time() < timeout:
                if left_lever.is_pressed:
                    counter += 1
                    if counter >= ratio:
                        return left_lever.held_time, 0
                elif right_lever.is_pressed:
                    counter += 1
                    if counter >= ratio:
                        return right_lever.held_time, 1
            raise TimeoutError


if __name__ == '__main__':
    try:
        helper = TaskHelper()
    except GPIOPinMissing:
        print('ERROR: GPIO pins are missing. Please set up GPIO terminal.')
