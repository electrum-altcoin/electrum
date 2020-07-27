import sys
from pathlib import Path

replacement_args = {
    "{{buildmatrix_coin_name_normal}}": sys.argv[1],
}

def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = f.read()
        if old_string not in s:
            return

    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)

for path in Path('./').rglob('**/*.py'):
    for key, value in replacement_args.items():
        inplace_change(path.absolute(), key, value)

