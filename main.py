from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from wtforms.validators import DataRequired, Email
from wtforms import StringField, SubmitField, EmailField, PasswordField, URLField
import smtplib
import csv
from csv import writer

class Form(FlaskForm):
    name = StringField(label="Freind Name", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class Login(FlaskForm):
    your_name = StringField(label="Your name", validators=[DataRequired()])
    your_email = EmailField(label="Email", validators=[DataRequired()])
    your_password = PasswordField(label="Password", validators=[DataRequired()])
    date = StringField(label="Date")
    time = StringField(label="Time")
    location = URLField(label="URL")
    submit = SubmitField(label="Log in ")



app = Flask(__name__)
app.config["SECRET_KEY"] = "fgsdmgqjsgmdjlgqdmsglù"

Bootstrap5(app)


#creat extension
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///freinds.db"
db.init_app(app)


PASSWORD = "seqppjzzgkneqbhe"

#creat table
class Freind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)


with app.app_context():
    db.create_all()



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=['POST', "GET"])
def add():
    form = Form()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data

        new_freind = Freind(name=name, email=email)
        db.session.add(new_freind)
        db.session.commit()

        # with open("freind-data.csv", mode="a", encoding="utf-8") as data:
        #     data.write(f"\n{name},"
        #                f"{email}")

        return redirect(url_for("freinds_list"))

    return render_template("add.html", form=form)

@app.route("/freinds")
def freinds_list():
    all_freind = db.session.execute(db.select(Freind)).scalars().all()
    return render_template("freinds.html", all_freind=all_freind)


@app.route("/delete")
def delete():
    id = request.args.get("id")
    freind_want_delete = db.get_or_404(Freind, id)
    db.session.delete(freind_want_delete)
    db.session.commit()
    return redirect(url_for('freinds_list'))


@app.route("/login", methods=["POST", "GET"])
def login():
    form = Login()
    if form.validate_on_submit():
        email = form.your_email.data
        password = form.your_password.data
        name = form.your_name.data
        date = form.date.data
        time = form.time.data
        location = form.location.data
        data_list = db.session.execute(db.select(Freind)).scalars()
        for item in data_list:
            server = ""
            if "gmail" in email:
                server = "smtp.gmail.com"
            elif "outlook" in email:
                server = "outlook.office365.com"
            elif "yahoo" in email:
                server = "smtp.mail.yahoo.com"
            else:
                server = "smtp.live.com"

            message = f"You are cordially invited to celebrate {name}'s birthday! Join us for a fun-filled evening of laughter," \
                      f" music, and good company as we mark this special occasion. Your presence would make the celebration" \
                      f" complete. Date: {date} Time: {time} Venue: {location} RSVP: [Contact Information] We look forward" \
                      f" to celebrating with you!"
            giphy_url = "https://media4.giphy.com/media/3oEjHEPaDX25ZMiH16/giphy.gif?cid=ecf05e47vcgtpfnzvdida0n0fvwlhg1qlgk46u6x5hxinuz6&ep=v1_gifs_search&rid=giphy.gif&ct=g"
            with smtplib.SMTP(server, port=587) as coneection:
                coneection.starttls()
                coneection.login(user=email, password=password)
                coneection.sendmail(from_addr=email,
                                    to_addrs=item.email,
                                    msg=f"subject:Dear {item.name}\n\n{giphy_url}\n{message}"
                                    )

            return redirect(url_for("has_sent"))




    return render_template("login.html", form=form)


@app.route("/hassent")
def has_sent():
    return render_template("message_sent.html")



if __name__ == "__main__":
    app.run(debug=True)






# your_email = input("Write your email please: ")
# your_password = input("Write you password please: ")
#
# names = input("write name of your freinds ex: ahmed, abdou: ").split()
#
# print(names)
#
#
# placeholder = "[name]"
#
# with open(r"Input\Names\invited_names.txt") as file_names:
#     list_of_names = file_names.readlines()
#
#
#
#
# with open(r"Input\Letters\starting_letter.txt") as letter_txt:
#     letter_contents = letter_txt.read()
#     for name in list_of_names:
#         script_name = name
#         new_letter = letter_contents.replace(placeholder, script_name)
#         with open(r"Output\ReadyToSend\freind_letter", mode="w") as mini_letter:
#            mini_letter.write(new_letter)




