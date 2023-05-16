import ujson
import os

# from bombunia_manager import Bombunia

# Get the list of all files and directories
path = "to_parse"
path_parsed = "grades"
dir_list = os.listdir(path)

data = {}

for i in dir_list:
    with open(f"{path}/{i}",'r') as f:
        data[str(i)] = ujson.load(f)

for i in data:
    with open(f"{path_parsed}/{i}",'w') as f:
        data[str(i)][0]['all_grades'] = data[str(i)][0]['allGrades']
        del data[str(i)][0]['allGrades']

        data[str(i)][0]['sum_of_all_grades'] = data[str(i)][0]['sumOfAllGrades']
        del data[str(i)][0]['sumOfAllGrades'] 

        data[str(i)][0]['count_of_all_grades'] = data[str(i)][0]['muchOfAllGrades']
        del data[str(i)][0]['muchOfAllGrades']

        del data[str(i)][0]['combo']
        del data[str(i)][0]['rekordzik']
        del data[str(i)][0]['dependence']

        ujson.dump(data[str(i)], f)
