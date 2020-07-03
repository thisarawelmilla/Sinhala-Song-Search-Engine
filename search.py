from elasticsearch import Elasticsearch
import re
import string
import tokenization.tokenization
import remove_stop_words.remove_stop_words
import lemmatization.lemmatization
import text_classification.text_classification
import spell_correction.spell_correction



def search_query(es, keyword, field_list,spell_check, other_list):
    print(keyword[0])
    if len(keyword)>1:
        all_queries =[{"multi_match" : {"query": keyword[0] ,"fields": field_list}}]
    elif len(keyword)>2:
        all_queries =[{"multi_match" : {"query": keyword[0] ,"fields": field_list}},{"multi_match" : {"query": keyword[-1] ,"fields": field_list}}]
    else:
        all_queries =[]       
    for i in range(len(keyword)-1):
        k = {}
        g = {}
        k["query"] = keyword[i] + ' '+keyword[i+1]
        k["fields"] = field_list
        g["multi_match"]=k
        all_queries.append(g)
    z= {}
    z['should'] = all_queries
    x = {}
    x['bool']= z
    body = {}
    body["query" ]= x
    body["from"]  = 0
    body["size"] = 50
    res = es.search(index="songs", body= body)
    return res


   
def results(lyrics_res, other_res, filters):

    lyrics_results = lyrics_res['hits']['hits']
    other_results = other_res['hits']['hits']
    all_results =[]
    word = {}
    for i in filters:
       all_filts = []
       filt = filters[i]
       print(i)
       if len(filt) >0 and i != 'ratings':
            for j in filt:

                all_filts += tokenization(j)
            word[i] = all_filts 

    add = False
    for i in other_results:
        if add or (len(word) ==0 and filters =={ 'genre': [], 'ratings': []}):             
            all_results.append([i['_score'], i['_source']])
    for i in lyrics_results:
        print(add,word,type(add),type(word))
        if add or (len(word) ==0 and filters =={}):             
            all_results.append([i['_score'], i['_source']])
    return all_results



def search(es, search_term, filters, coprus): 
    special_stopwords = ['ගයු', 'ගැයූ', 'ගයන', 'ගායනා', 'ගයනා', 'ගැයුවේ', 'ගැයුව','ගැයූවේ', 'ගායක', 'ගායකයා', 'ගයන්නේ','කියු', 'කියන', 'කියනා', 'කියුවේ', 'කියූවේ','කිව්ව', 'කියන්නේ','ලියු', 'ලියූ', 'ලියන', 'ලියනා', 'ලියුවේ', 'ලියූවේ', 'ලියන්නේ','රචනා', 'රැචූයේ','පද','වචන', 'පේලි', 'පේළි','ජාතිය', 'ජාතියේ', 'වර්ග', 'වර්ගයේ', 'කාණ්ඬය','කාන්ඬයේ', 'වගේ', 'ඒවගේ','නම','ගීතයේ', 'සිංදුවේ', 'ගීයේ','ජනප්‍රිය', 'ප්‍රකට', 'ප්‍රසිද්ධ', 'කැමති', 'දන්න', 'දන්නා', 'හොද', 'හොඳ', 'සාර්ථක','අප්‍රිය', 'අප්‍රකට', 'අප්‍රසිද්ධ', 'අකැමති', 'නොදන්න', 'නොදන්නා', 'හොද', 'හොඳ', 'අසාර්ථක','සාමාන්‍ය','නොවන', 'නැති','නොමැති', 'නොවු', 'නොවූ', 'නොවුන','නොවුනු', 'නොවී', 'නොවි', 'වර්තමාන','ගීත','ගීතයේ','ගී', 'ගීතය','ගීතයට','සිංදු','සිංදුවේ','සිංදුව','සිංදුවට','කවුද','කාගේද','කීයද','මොනවාද']  
    tokens = tokenization(search_term)
    spell_check = spell_correction.edit_distance(tokens, coprus[0], coprus[1])
    stopword_removed = remove_stopword(spell_check, coprus[2])

    field_scores = text_classification.get_class(stopword_removed)
    stopword_removed = remove_stopword(stopword_removed, special_stopwords)

    body = {"query" : { "match_phrase" : {"lyrics":search_term } } }
    lyrics_res = es.search(index="songs_try_13", body= body)

    field_list = ['singer','composer', 'music', 'genre', 'ratings', 'key']
    other_list = ['title','lyrics']
    term = spell_check [0]
    for i in spell_check [1:]:
        term += ' ' + i
    for i in range(len(field_list)):
        field_list[i] = field_list[i] +'^'+str(int(field_scores[i]*2))

    other_res =search_query(es,stopword_removed, field_list, term, other_list)
    output = results(lyrics_res, other_res, filters)
    changed = False

    for i in range(len(tokens)):
        if tokens[i] != spell_check[i]:
             changed =  True
    if changed:
        replace = 'ඔබ අදහස් කළේ:'+''
        for i in spell_check:
            replace += ' ' + i
    else:
        replace = ''

    return {'spell_correction':replace, 'hits_number': str(len(output)), 'results':output}


