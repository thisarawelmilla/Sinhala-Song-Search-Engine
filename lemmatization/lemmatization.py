affix_list = ['ගේ']

def lemmatize(world_list):
    lemmatized_word_list = world_list
    word_index = 0
    for word in world_list:
        for affix in affix_list:
            if word[-2:] == affix:
                lemmatized_word = word[:-2]
                lemmatized_word_list[word_index] = lemmatized_word
                break
        word_index += 1 
    
    return lemmatized_word_list


		 
