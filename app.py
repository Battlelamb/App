from flask import Flask, render_template, request, redirect, url_for, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_mongoengine import MongoEngine
# from pymongo import MongoClient

# connection = MongoClient('localhost',27017)

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)


class User(db.Document):
    firstname = db.StringField()
    lastname = db.StringField()

    def to_json(self):
        return {"firstname": self.firstname,
                "lastname": self.lastname}


class RegisterForm(Form):
    firstname = StringField(u'First Name', validators=[
                            validators.input_required()])
    lastname = StringField(u'Last Name', validators=[validators.optional()])


@app.route("/")
def index():
    numbers = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
    ]
    sayi = 10
    return render_template("index.html", number=sayi, numbers=numbers)


@app.route("/hakkimizda")
def about():
    return render_template("about.html")


@app.route("/article/<string:id>")
def artickle(id):
    return "Article Id" + id


@app.route("/register", methods=['GET', "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST":
        firstname = form.firstname.data
        lastname = form.lastname.data

        user = User(firstname=firstname, lastname=lastname)
        user.save()

        return redirect(url_for("register"))
    else:
        users = list(User.objects)
        print(users)
        return render_template("register.html", form=form, users=users)

    # return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
