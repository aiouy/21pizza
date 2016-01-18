import sys

task = input("Tasks (enter 1 or 2):\n1. Validate inputs and get price (this should always be done first)\n2. Order\n")
print(task)
if int(task) == 1:
    print('awesome: 1')
elif int(task) == 2:
    print('awesome: 2')
else:
    print('Please enter either 1 or 2')
    sys.exit()
