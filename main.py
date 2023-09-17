from collections import OrderedDict
import argparse

dictionary = OrderedDict()
stats = OrderedDict()

parser = argparse.ArgumentParser()
parser.add_argument('--import_from')
parser.add_argument('--export_to')
args = parser.parse_args()
export_to = args.export_to
import_from = args.import_from

c = 0
if import_from is not None:

    with open(import_from, 'r') as file:
        g = file.readlines()
        a = []
        for element in g:
            a.append(element.strip())
        a, stat = (eval(a[0]), eval(a[1]))
    for key, value in a.items():
        dictionary[key] = value
    print(f'{len(a)} cards have been loaded.')
    stats.update(stat)


while True:
    if c == 1:
        b = 'add'
    else:
        b = input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
    if b == 'log':
        file = input('File name:')
        with open(file, 'w') as f:
            f.write(str(stats))
            f.close()
        print('The log has been saved.')
    if b == 'reset stats':
        stats = {}
        print('Card statistics has been reset.')
    if b == 'hardest card':
        gz = sorted(stats.items(), key=lambda hello: hello[1], reverse=True)
        if len(gz) == 0:
            print('There are no cards with errors')
            continue
        if gz[0][1] == 0:
            print('There are no cards with errors')
            continue
        x = gz[0][1]
        second = []
        for error in gz:
            if error[1] == x:
                second += [(error[0].center(len(error[0]) + 2, '"'), error[1])]
        s = [[i for i, j in second],
             [j for i, j in second]]
        if len(s[0]) == 1:
            print(f'The hardest card is {", ".join(s[0])}. You have {s[1][0]} errors answering it.')
        print(f'The hardest cards are {", ".join(s[0])}. You have {s[1][0]} errors answering them.')
    if b == 'exit':
        print('Bye Bye!')
        if export_to is not None:
            with open(export_to, 'w') as file:
                file.writelines(str(dictionary) + '\n' + str(stats))
                print(f'{len(dictionary)} cards have been saved.')
                file.close()
        break
    if b == 'remove':
        x = input('Which card?\n')
        try:
            del dictionary[x]
            print('The card has been removed.')
        except KeyError:
            print(f'Can\'t remove "{x}": there is no such card.')
        finally:
            continue

    elif b == 'add':
        x = input('The card:\n')
        if x in dictionary.keys():
            print(f'The term "{x}" already exists.\n')
            c = 1
            continue
        y = input('The definition of the card:\n')
        if y in dictionary.values():
            y = input(f'The definition "{y}" already exists.\n')
            while True:
                if y in dictionary.values():
                    y = input(f'The definition "{y}" already exists.\n')
                    continue
                break
        dictionary[x] = y
        stats[x] = 0
        print(f'The pair ("{x}":"{y}") has been added.')
        c = 0

    if b == 'ask':
        x = int(input('How many times to ask?'))
        while x > 0:
            for key, value in dictionary.items():
                if x == 0:
                    break
                definition = input(f'Print the definition of "{key}"\n')
                wrong = f'Wrong. The right answer is "{value}"'
                for k, v in dictionary.items():
                    if v == definition and v != value:
                        wrong += f', but your definition is correct for "{k}".'
                if definition == value:
                    print('Correct!')
                else:
                    print(wrong)
                    stats[key] += 1

                x -= 1
    if b == 'export':
        x = input('File name:\n')
        with open(x, 'w') as file:
            file.writelines(str(dictionary) + '\n' + str(stats))
            print(f'{len(dictionary)} cards have been saved.')
            file.close()
    if b == 'import':
        x = input('File name:\n')
        try:
            with open(x, 'r') as file:
                g = file.readlines()
                a = []
                for element in g:
                    a.append(element.strip())
                a, stat = (eval(a[0]), eval(a[1]))
            for key, value in a.items():
                dictionary[key] = value
            print(f'{len(a)} cards have been loaded.')
            stats.update(stat)
        except FileNotFoundError:
            print('File not found.')