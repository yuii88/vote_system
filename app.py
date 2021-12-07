from flask import Flask, render_template, request,redirect
from collections import defaultdict
from uuid import uuid4
from db import VoteDB

app = Flask(__name__)
db = VoteDB()

# topics = dict({
#     'abc1234': { # topic_id, dictionary key
#         'name': 'Hotel for holiday',
#         'data': {
#             'Hotel A': 0,
#             'Hotel B': 1
#         }
#     }
# })

@app.route('/')
def index():
    topics = db.get_topic_names()
    return render_template('index.html',topics=topics)

@app.route('/addTopic', methods=['POST'])
def add_new_topic():
    topic_id = str(uuid4())
    name = request.form.get('name')
    db.add_topic(topic_name=name)
    # topics[topic_id] ={
    #     'name': name,
    #     'data': defaultdict(int)
    # }
    #print(topic_id,name)
    return redirect('/')
    

@app.route('/newTopic')
def new_topic():
    return render_template('newtopic.html')

@app.route('/topic/<topic_id>')
def get_topic_page(topic_id):
    topic_data,topic_name = db.get_topic(topic_id)
    print(topic_data)
    return render_template('topic.html',topic_id=topic_id,topic=topic_data,topic_name=topic_name)

@app.route('/topic/<topic_id>/newChoice', methods=["POST"])
def new_choice(topic_id):
    cname = request.form.get('choice_name')
    db.add_choice(choice_name=cname, topic_id=topic_id)
    #print(cname)
    return redirect(f'/topic/{topic_id}')

# @app.route('/topic/<topic_id>/vote', methods=["POST"])
# def vote_topic(topic_id):
#     choice_name = request.form.get('choice_name')
#     topics[topic_id]['data'][choice_name] += 1
#     return redirect(f'/topic/{topic_id}')


if __name__ == '__main__':
    app.run("0.0.0.0,5000")