import numpy as np
from os import listdir
from os.path import isfile, join


#   TODO: change for local env!
DIR = [
    "D:/Radon/joined_homes",
    "D:/Radon/joined_homes_less",
    "D:/Radon/proc_time_homes",
    "D:/Radon/proc_time_homes_less",
]


def deep_np_as_array(gen):
    if hasattr(gen, '__iter__'):
        return np.asarray([deep_np_as_array(row) for row in gen])
    return gen


if __name__ == '__main__':
    for dir_name in DIR:
        # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        only_files = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]

        total = 0

        for file in only_files:
            num_lines = sum(1 for line in open(dir_name + "/" + file))
            total += num_lines

        print(dir_name, total)

    print(deep_np_as_array([[1, 2, 3], [2, 3, 4]]))
