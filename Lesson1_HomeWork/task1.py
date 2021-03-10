# Посмотреть документацию к API GitHub, разобраться как вывести список
# репозиториев для конкретного пользователя, сохранить JSON-вывод в файле
# *.json.

import requests
import json


def user_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url).json()
    with open(username + '_GITHub.json', 'w') as outfile:
        json.dump(response, outfile)
    return '\n'.join(response[i].get('name') for i in range(len(response)))


#print(user_repos('AlSavva'))

"""
Algorytms_and_data_structure
DataBaseCourse
DataBases_FinalWork
DataScience_PythonLibrary
MashLearn
OpenEduCourses
Pars_Scrap_Crowl_Methods
Python-basics-homework
PythonFitch
"""