from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import search
import ast

with open('/home/thisara/Documents/sem 7/Data Mining/ir_project_160684E/src_copus/stopwords.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    stopwords = text.split('\n')[1:-2]

with open('/home/thisara/Documents/sem 7/Data Mining/ir_project_160684E/copus_words.txt', 'r', encoding='utf-8') as f:
    text = f.read()
coprus = ast.literal_eval(text)

with open('/home/thisara/Documents/sem 7/Data Mining/ir_project_160684E/similarity.txt', 'r', encoding='utf-8') as f:
    sim = f.read()
sim_letter = ast.literal_eval(sim)
coprus = [coprus, sim_letter, stopwords]


app = Flask(__name__)
es = Elasticsearch(localhost = 'localhost', port=9200)


@app.route('/')
def home():
    return render_template('search.html')


@app.route('/search/results', methods=['GET', 'POST'])
def search_request():  
    # read data and the query
    search_term = request.form["input"]
    applied_filter = {}

    applied_filter['genre'] = request.form.getlist('genre')
    applied_filter['ratings'] = request.form.getlist('popularity')
 
    # retrieve data
    results = search.search(es, search_term, applied_filter,  coprus)

    # results prepare for representation
    res_represent = []
    for i in results['results']:
        i = i[1]
        res_represent.append([i['title'],i['singer'],i['composer'],i['music'],i['lyrics'],i['beat'],i['genre'],i['ratings']])
    represent = [results['spell_correction'], results['hits_number'], res_represent]

    return render_template('results.html', res=represent  )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
