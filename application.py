from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, ThoughtPod, PodItem
app = Flask(__name__)


engine = create_engine('sqlite:///thoughtpods.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def HelloWorld():
    return "Hello World"

@app.route('/pods/<int:pod_id>/')
def podList(pod_id):
    thoughtpod = session.query(ThoughtPod).filter_by(id=pod_id).one()
    items = session.query(PodItem).filter_by(thought_pod_id=thoughtpod.id)
    return render_template('podlist.html', thoughtpod=thoughtpod, items=items)


@app.route('/pods/<int:pod_id>/new/', methods=['GET', 'POST'])
def newPodListItem(pod_id):
    if request.method == 'POST':
        newItem = PodItem(
            title=request.form['title'], thought_pod_id=pod_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('podList', pod_id=pod_id))
    else:
        return render_template('newpodlistitem.html', pod_id=pod_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
