import glob
import pickle
import re
from collections import Counter

from isolation import Isolation

prog = re.compile(".*Win:: (.)\.append\(\{(.*): ..([0-9]*), ([0-9]*)\), (-*[0-9]*).*")

f = []
s = []
first_n = {}
second_n = {}

for myfile in glob.glob("match_*.log"):
    print(myfile)
    with open(myfile) as file:
        for line in file:
            result = prog.match(line)
            if result:
                is_first = True if result.group(1) == "f" else False
                board = int(result.group(2))
                locs = (int(result.group(3)), int(result.group(4)))
                action = result.group(5)

                string = '{} {} {}'.format(board, locs[0], locs[1])
                if is_first:
                    count = first_n.get(string, [])
                    count.append(action)
                    first_n[string] = count
                else:
                    count = second_n.get(string, [])
                    second_n[string] = count
                # print(is_first, board, locs, action)

# key, val
#      locs            , action
#      ( first, second)    int
#          int   int

# Count the number of wins


for key, value in first_n.items():
    if key in second_n:
        print(key, "is in both")
for key, value in second_n.items():
    if key in first_n:
        print(key, "is in both")

start_state = Isolation()
for action in start_state.actions():
    first_state = start_state.result(action)
    first_state_string = '{} {} {}'.format(first_state.board, first_state.locs[0], first_state.locs[1])

    for action_s in first_state.actions():
        # print(action,action_s)
        second_state = first_state.result(action_s)
        second_state_string = '{} {} {}'.format(second_state.board, second_state.locs[0], second_state.locs[1])
        for action_t in second_state.actions():
            # print(action,action_s)
            third_state = second_state.result(action_t)
            third_state_string = '{} {} {}'.format(third_state.board, third_state.locs[0], third_state.locs[1])
            for action_f in third_state.actions():
                # print(action,action_s)
                state = third_state.result(action_f)
                string = '{} {} {}'.format(state.board, state.locs[0], state.locs[1])
                if string in first_n:
                    most_common, num_most_common = Counter(first_n.get(string)).most_common(1)[0]
                    count = first_n.get(third_state_string, [])
                    count.extend([action_f] * num_most_common)
                    first_n[third_state_string] = count
            if third_state_string in first_n:
                most_common, num_most_common = Counter(first_n.get(third_state_string)).most_common(1)[0]
                count = first_n.get(second_state_string, [])
                count.extend([action_s] * num_most_common)
                first_n[second_state_string] = count
        if second_state_string in first_n:
            most_common, num_most_common = Counter(first_n.get(second_state_string)).most_common(1)[0]
            count = first_n.get(first_state_string, [])
            count.extend([action] * num_most_common)
            first_n[first_state_string] = count

new_new_first = {}
for key, value in first_n.items():
    most_common, num_most_common = Counter(value).most_common(1)[0]
    new_new_first[key] = most_common

new_new_second = {}
for key, value in second_n.items():
    if value:
        most_common, num_most_common = Counter(value).most_common(1)[0]
        new_new_first[key] = most_common

# key_value = [int(s) for s in key.split()]


output = open('data.pickle', 'wb')

pickle.dump([new_new_first, new_new_second], output)

output.close()
