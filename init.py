from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///content.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    place = db.Column(db.String(300), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Card %r' % self.id


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/content')
def all_cards():
    py_cards = Card.query.order_by(Card.date.desc()).all()
    return render_template("publications.html", cards=py_cards)


@app.route('/create-card', methods=['POST', 'GET'])
def create_travel():
    if request.method == "POST":
        new_file = request.form['input_file']
        new_desc = request.form['input_desc']
        new_place = request.form['input_place']

        new_card = Card(file=new_file, description=new_desc, place=new_place)

        try:
            db.session.add(new_card)
            db.session.commit()
            return redirect('/content')
        except:
            return "Ошибка при создании публикации"
    else:
        return render_template("new-publication.html")


@app.route('/content/<int:id>')
def detail(id):
    this_card = Card.query.get(id)
    return render_template("detail.html", card=this_card)


@app.route('/content/<int:id>/delete')
def delete_travel(id):
    this_card = Card.query.get_or_404(id)

    try:
        db.session.delete(this_card)
        db.session.commit()
        return redirect('/content')
    except:
        "Ошибка при удалении путешествия"


# @app.route('/travels/<int:id>/update', methods=['POST', 'GET'])
# def update_travel(id):
#     travel = Travel.query.get(id)
#     if request.method == "POST":
#         travel.title = request.form['title']
#         travel.author = request.form['author']
#         travel.route = request.form['route']
#         travel.description = request.form['description']
#         travel.status = request.form['status']
#
#         try:
#             db.session.commit()
#             return redirect('/travels')
#         except:
#             return "Ошибка при редактировании путешествия"
#     else:
#         return render_template("update-travel.html", travel=travel)


if __name__ == "__main__":
    app.run(debug=False)
