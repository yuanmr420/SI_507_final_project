import pandas as pd
import json

state = pd.read_csv("d:\\2022fall 课程资料\\SI 507\\hw\\final project\\cities\\usa_states_latitude_and_longitude_values.csv")
state_name_num = list(enumerate(list(state['state_name'])))

city = pd.read_csv("d:\\2022fall 课程资料\\SI 507\\hw\\final project\\cities\\cities.csv")
city_list = []
for row in city.itertuples():
    city_list.append((getattr(row,'State'),getattr(row,'City')))
city_list.sort()

#create a tree to ask whether hungry
def hung_tree(city_dic):
    tree = {"Are you hungry?":
                {'No':'Thanks! See you next time',
                'Yes':
                city_dic}}
    return tree

#create a tree to show the relationships between states and cities
def create_city_tree(city_list):
    city_dic = {}
    i = 0
    for city in city_list:
        if city[0] not in city_dic.keys():
            i =0
            city_dic.setdefault(city[0],{})
            city_dic[city[0]][i]=city[1]
        else:
            city_dic[city[0]][i]=city[1]
            i += 1
    return city_dic

def main():
    city_dict = create_city_tree(city_list)
    tree = hung_tree(city_dict)
    dump_json_cache = json.dumps(tree)
    fw = open('tree_cache.json', 'w')
    fw.write(dump_json_cache)
    fw.close()

if __name__ == '__main__':
    main()

