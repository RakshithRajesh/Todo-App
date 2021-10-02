from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class ContactForm(FlaskForm):
    name = StringField(100, validators=[DataRequired()])
    submit = SubmitField("Submit")

class DataBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f"User: {self.id}"

@app.route('/', methods=['GET','POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        new_user = DataBase(name=name)
        home = url_for("home")
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            return f"Name You have Choosen is Already!!! <a href='{home}'>Return to Homepage</a>"

        return redirect(url_for("home"))
    else:
        user_list = DataBase.query.order_by(DataBase.date_created)
        return render_template("index.html",form=form, user_list=user_list)

@app.route("/delete/<int:id>")
def delete(id):
    user_to_delete = DataBase.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for("home"))
    except:
        return "There was a error"

@app.route('/updatename/<int:id>', methods=["GET", "POST"])
def update_name(id):
    username_to_update = DataBase.query.get_or_404(id)
    if request.method == "POST":
        username_to_update.name = request.form.get("name")
        home = url_for("home")
        try: 
            db.session.commit()
            return redirect("/")
        except:
            return f"There was a Error Updating the User's Details... <a href='{home}'>Return to Homepage</a>"

    else:
        return render_template("update_name.html", username_to_update=username_to_update)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

if __name__ == '__main__': 
    app.run(debug=True)