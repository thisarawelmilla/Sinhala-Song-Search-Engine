import csv
import pandas as pd
import ast

df = pd.read_csv("new_scraped_songs1000_2.csv")
title = df['title']


def edit_distance(word_list, coprus, sim_letter):
    suggestion_terms = []
    for check in word_list:  
        check_len = len(check)
        suggestion = []
        max_score = 3
        for word in coprus:
          if word == check:
             suggestion_terms.append(True)
             break
          else:
             word_len = len(word)
             len_dif = word_len - check_len
             a = max(check_len, word_len)
             n = 0
             if len_dif > 0:
                 check = check + ' '*len_dif
             else:
                 word = word + ' '*(-(len_dif))
             find = True
             stop = False
             consective = False
             penalty = False
             score = 0
             total_score = 0
             missing_letter = 0
             for index in range(a):
                 check[index]
                 sim = ''
                 allow = 2
                 score = 0
                 stop = False
                 if check[index] in sim_letter:
                     sim = sim_letter[check[index]]
                 if consective:
                     penalty = True
                 if not penalty:
                     consective = False

                 while score <1 :
                     for i in range(allow):     
                         if index == 0:
                             if (check[index] !=  word[index+i] and sim != word[index+i]) : 
                                if consective:                            
                                    score += i*5
                                else:
                                    score += i
                             else:
                                stop = True
                                break
                         elif index +1 == a:
                             if (check[index] !=  word[index-i] and sim != word[index-i]) :                             
                                if consective:                            
                                    score += i*5
                                else:
                                    score += i              
                             else:
                                stop = True
                                break
                         else:
                             if (check[index] !=  word[index-i] and sim != word[index-i]) and (check[index] !=  word[index+i] and sim != word[index+i]) :                             
                                if consective:                            
                                    score += i*5
                                else:
                                    score += i              
                             else:
                                stop = True
                                break
                         
                         if i != 0 and stop==True:
                             consective  = True
                         if i+1 == allow and not stop :
                             missing_letter +=1
                  
                     break

                 total_score += score
                 if index+1 == a:
                         if (score <1 or missing_letter<2 ) and total_score < max_score:
                             max_score = total_score
                             suggestion.append([word, total_score])    
                         break
        suggest = False
        added = False
        for i in suggestion :
            if i[1] == max_score:
               if not suggest:
                   suggest_term = i[0]
                   suggest = True
               else:
                   suggestion_terms.append(False)
                   added = True
        if  not added:
            suggestion_terms.append(suggest_term)       
    return suggestion_terms          




