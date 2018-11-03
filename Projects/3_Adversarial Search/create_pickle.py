import pickle
import os

first = []
second = []
os.system('cat *.log | grep Win | sed -e "s/.*:: //" > m.py')
exec(open("./m.py").read())

print("Total: {}, first wins {} times and second wins {} times".format(len(first)+ len(second),len(first), len(second)))

n = {}

for j in [first, second]:
    for i in j:
       for key, val in i.items():
          string = '{} {}'.format(key, val)
          value = n.get(string,0 )+1
          n[string] = value

new_first = {}
for key, val in n.items():
    key_value = [int(s) for s in key.split()]
    value = new_first.get(key_value[0], ( None, 0) )
    # action, value
    if key_value[1] <= val:
       value = ( key_value[1], val )
       new_first[key_value[0]] = value

new_new_first = {}
for key, (action, count) in new_first.items():
    new_new_first[key] = action 

#for key, val in new_first.items():
#    print(val[1], key, val[0])

output = open('data.pickle', 'wb')

pickle.dump(new_new_first, output)

output.close()

