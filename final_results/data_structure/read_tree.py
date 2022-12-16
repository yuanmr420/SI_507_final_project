import json
CACHE_FILENAME = 'tree_cache.json'

def open_cache():
    '''Open the tree cache file in json format

    Parameters
    ----------
    None

    Returns
    -------
    A tree dictionary

    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_content = cache_file.read()
        cache_dict = json.loads(cache_content)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def q1(tree):
    '''The first node of my tree: Are you hungry?

    Parameters
    ----------
    tree: dic
        a tree dictionary

    Returns
    -------
    True: Boolean
        it means that the user choose yes
    False: Boolean
        it means that the user choose no. And there would be no more questions for uses to answer.

    '''
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
    '''The second node of my tree: Which state do you live in?

    Parameters
    ----------
    tree: dic
        a tree dictionary

    Returns
    -------
    promt: str
        the state users choose

    '''
    print('02 Which state do you live in?')
    for state in tree['Are you hungry?']['Yes'].keys():
        print(state)
    print("Please type the state's name you live in:")
    prompt = input()
    print('Your choice is: ' + prompt)
    return prompt

def q3(tree, state):
    '''The third node of my tree: Which city do you live in?

    Parameters
    ----------
    tree: dic
        a tree dictionary
    state: str
        the state users choose in second node

    Returns
    -------
    None

    '''
    print('03 Which city do you live in?')
    for num,city in tree['Are you hungry?']['Yes'][state].items():
        print(num+": "+city)
    print("Please type the city's name you live in:")
    prompt = input()
    print('Your choice is: ' + prompt)
    print('Thanks! See you next time!')

def main():
    '''The mian part to run all the function in this file. It helps show how the tree works.

    Parameters
    ----------
    None

    Returns
    -------
    None

    '''
    tree = open_cache()
    if q1(tree):
        state = q2(tree)
        q3(tree,state)

if __name__ == '__main__':
    main()
