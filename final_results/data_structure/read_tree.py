import json
CACHE_FILENAME = 'tree_cache.json'

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_content = cache_file.read()
        cache_dict = json.loads(cache_content)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def q1(tree):
    print("01 " + str(list(tree.keys())[0]))
    key = list(tree.keys())[0]
    choice = tree[key].keys()
    for item in choice:
        print(item)
    print("Please type Yes or No:")
    promt = input()
    if promt == 'No':
        print(tree[key][promt])
        return False
    if promt == 'Yes':
        print('Your choice is: Yes')
        return True

def q2(tree):
    print('02 Which state do you live in?')
    for state in tree['Are you hungry?']['Yes'].keys():
        print(state)
    print("Please type the state's name you live in:")
    prompt = input()
    print('Your choice is: ' + prompt)
    return prompt

def q3(tree, state):
    print('03 Which city do you live in?')
    for num,city in tree['Are you hungry?']['Yes'][state].items():
        print(num+": "+city)
    print("Please type the city's name you live in:")
    prompt = input()
    print('Your choice is: ' + prompt)
    print('Thanks! See you next time!')

def main():
    tree = open_cache()
    if q1(tree):
        state = q2(tree)
        q3(tree,state)

if __name__ == '__main__':
    main()
