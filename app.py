from flask import Flask, render_template, request,redirect
from collections import defaultdict
from uuid import uuid4
from db import VoteDB
from model import db, Votes, Topics

app = Flask(__name__)

@app.route('/')
def index():
    topics = list(Topics.select()) # SELECT *
    return render_template('index.html',topics=topics)

@app.route('/addTopic', methods=['POST'])
def add_new_topic():
    topic_id = str(uuid4())
    name = request.form.get('name')
    Topics.create(id=topic_id, name=name)
    return redirect('/')
    

@app.route('/newTopic')
def new_topic():
    return render_template('newtopic.html')

@app.route('/topic/<topic_id>')
def get_topic_page(topic_id):
    topic = list(Topics.select().where(Topics.id == topic_id)) 
    print(topic)
    votes = list(Votes.select().where(Votes.topic == topic[0])) 
    return render_template('topic.html',topic_id=topic_id,topic=topic[0],votes=votes)

# @app.route('/topic/<topic_id>/newChoice', methods=["POST"])
# def new_choice(topic_id):
#     cname = request.form.get('choice_name')
#     db.add_choice(choice_name=cname, topic_id=topic_id)
#     #print(cname)
#     return redirect(f'/topic/{topic_id}')

# @app.route('/topic/<topic_id>/vote', methods=["POST"])
# def vote_topic(topic_id):
#     choice_id = request.form.get('choice')
#     db.vote(choice_id=choice_id, topic_id=topic_id)
#     return redirect(f'/topic/{topic_id}')


if __name__ == '__main__':
    db.connect()
    db.create_tables([Topics, Votes])
    app.run("0.0.0.0,5000")