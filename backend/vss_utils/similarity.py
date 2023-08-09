from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pandas as pd
import time

def get_link(top_two):
    links = []
    for i in top_two:
        if i[-1].isnumeric(): temp = i[:-6]
        else: temp = i[:-4]
        links.append(f'https://docs.appian.com/suite/help/23.2/{temp}.html')
    if links[0] == links[1]: return links[0]
    return links[0] + '; ' + links[1]

def create_dataframe(matrix, tokens):
    df = pd.DataFrame(data=matrix, index=tokens, columns=tokens)
    return(df)

def vss(question, dir_path):
    filenames = {}
    #Parse the dir_path directory to grab all of the documentation and store it in the filenames dictionary
    for file_path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, file_path)):
            file_contents = ""
            with open(os.path.join(dir_path, file_path), "r") as f:
                for line in f:
                    stripped_line = line.strip()
                    file_contents += stripped_line
            filenames[file_path] = file_contents
    #Add question to file bank for comparison
    filenames['question'] = question

    #Create the vectorizer
    count_vectorizer = CountVectorizer()
    vector_matrix = count_vectorizer.fit_transform(list(filenames.values()))
    vector_matrix
    #Create the similarity matrix
    start_time = time.time()
    cosine_similarity_matrix = cosine_similarity(vector_matrix)
    df = create_dataframe(cosine_similarity_matrix,list(filenames.keys()))
    end_time = time.time()
    #print("Asked question: ", question)
    #print("Total time (in sec):", end_time-start_time)
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
        #print(df.loc[:, ['question']].sort_values(by=['question']))

    #Pull the most related files and break them into smaller sections 
    temp = df.loc[:, ['question']].sort_values(by=['question'])
    top_five = temp.index[-6:-1]

    segmented = {}
    size = 1000
    for i in top_five:
        text = filenames[i]
        words = text.split(' ')
        j = 0
        k = 1
        if(len(words) <= size):
            segmented[i] = text
            continue
        while j+size < len(words):
            segmented[i + ' ' + str(k)] = ' '.join(words[j:j+size])
            j += size
            k += 1
        segmented[i + ' ' + str(k)] = ' '.join(words[-size:])
    segmented['question'] = question

    #Run the Count vectorizor and similarity matrix for the smaller segments of the docs
    count_vectorizer2 = CountVectorizer()
    vector_matrix2 = count_vectorizer2.fit_transform(list(segmented.values()))
    vector_matrix2
    start_time = time.time()
    cosine_similarity_matrix2 = cosine_similarity(vector_matrix2)
    df2 = create_dataframe(cosine_similarity_matrix2, list(segmented.keys()))
    end_time = time.time()
    #print("Asked question: ", question)
    #print("Total time (in sec):", end_time-start_time)
    #with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        #display(df2.loc[:, ['question']].sort_values(by=['question']))

    #Return the text of the two highest ranking questions
    temp2 = df2.loc[:, ['question']].sort_values(by=['question'])
    top_two = temp2.index[-3:-1]
    final_context = segmented[top_two[0]] + '\n' + segmented[top_two[1]]
    return (get_link(top_two), final_context)    


vss('How can I change my default search selection in Designer', 'backend/output_full')
