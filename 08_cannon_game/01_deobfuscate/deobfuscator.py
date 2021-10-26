with open('./gun_obfuscated.py', 'r') as f:
    program = f.read()

program = bytes(program, 'UTF-8')
data = []


def remember(x):
    global data
    data.append(x)


def deobfuscate_once(program):
    if b'exec' in program:
        exec(b'exec = remember\n' + program)
        return True
    return False


data.append(program)
while b'exec' in data[len(data) - 1]:
    deobfuscate_once(data[len(data) - 1])

with open('deobfuscated.py', 'w') as f:
    f.write(data[len(data) - 1].decode('UTF-8'))

print(data[len(data) - 1].decode('UTF-8'))
