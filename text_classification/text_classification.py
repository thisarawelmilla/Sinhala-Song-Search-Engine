import pandas as pd
import ast
import codecs

def get_class(term_list):
    with codecs.open('/home/thisara/Documents/sem 7/Data Mining/ir_project_160684E/field_keys.txt', 'r', encoding='utf-8') as json_file:
         cop = json_file.read()
    cop = ast.literal_eval(cop)

    weights = {'singer': [['1',1.0],['2',1.0]], 'composer': [['3',1.0],['4',1.0],['5',1.0]], 'music': [['3',0.5],['6',1.0]], 'genre': [['7',1.0]], 'ratings': [['9',1.0],['10',1.0],['11',1.0]], 'beat': [['6',0.5]]}

    weight_list=[]
    for field in weights:
         weight = 0
         for term in term_list:
              for words in weights[field]:   
                   all_word = cop[words[0]]
                   if term in all_word:
                       weight += words[1]
         weight_list.append(weight)

    return weight_list

