from flask import Flask,render_template,redirect,request,url_for,flash,session
import wtforms
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

class RegisterForm(wtforms.Form):
    name = wtforms.StringField("Name", validators=[wtforms.validators.DataRequired()])
    username = wtforms.StringField("Username", validators=[wtforms.validators.DataRequired(),
                                                           wtforms.validators.Length(min=8, max=25)])
    email = wtforms.StringField("E-mail", validators=[wtforms.validators.Email(),
                                                      wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Password", validators=[wtforms.validators.DataRequired(),
                                                           wtforms.validators.Length(min=6, max=15)])

class LoginForm(wtforms.Form):
    username = wtforms.StringField("Username", validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField("Password", validators=[wtforms.validators.DataRequired()])

class ContactForm(wtforms.Form):
    email = wtforms.StringField("E-mail", validators=[wtforms.validators.Email(),
                                                      wtforms.validators.DataRequired()])
    content = wtforms.TextAreaField("Content", validators=[wtforms.validators.DataRequired(),
                                                           wtforms.validators.Length(min=10, max=500)])

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = "ironsculpt"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ironsculpt"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


app.static_folder = 'static'

@app.route("/")
def logo():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/trainers")
def trainers():
    return render_template("trainers.html")

@app.route("/about")
def about():
    return render_template("about.html")


    

@app.route("/coaching")
def coaching():
    return render_template("coaching.html")

@app.route("/fitness")
def fitness():
    return render_template("fitness.html")

@app.route("/kickbox")
def kickbox():
    return render_template("kick_box.html")

@app.route("/pilates")
def pilates():
    return render_template("pilates.html")

@app.route("/zumba")
def zumba():
    return render_template("zumba.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm(request.form)

    if request.method == "POST" and form.validate():
        email = form.email.data
        content = form.content.data

        cursor = mysql.connection.cursor()

        query = "INSERT INTO mails(mail_address,content) VALUES(%s,%s)"

        cursor.execute(query,(email,content))
        mysql.connection.commit()

        cursor.close()

        flash("Mail is sent successfully", "success")
        return redirect(url_for("logo"))
    else:
        return render_template("contact.html", form = form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)  #parolayı gizli tutmak için encrypt işlemi yapıldı.

        cursor = mysql.connection.cursor()
        record  = "INSERT INTO users(name,username,email,password) VALUES(%s,%s,%s,%s)"

        cursor.execute(record,(name,username,email,password))
        mysql.connection.commit()

        cursor.close()

        flash("User is recorded successfully", "success")

        return redirect(url_for("logo"))
    else:
        return render_template("register.html", form = form)


@app.route("/logout")
def logout():
    session.clear()
    flash("Successful Logout", "success")
    return redirect(url_for("logo"))



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()

        query = "SELECT * FROM users WHERE username = %s"

        result = cursor.execute(query,(username,))

        if result>0:
            data = cursor.fetchone()
            real_password = data["password"]

            if sha256_crypt.verify(password_entered, real_password):
                session["logged_in"] = True
                session["username"] = username
                flash("Login Process Successful", "success")
                return redirect(url_for("logo"))
            else:
                flash("Wrong Password!", "danger")
                return redirect(url_for("login"))
        else:
            flash("Username is Undefined!", "danger")
            return redirect(url_for("login"))


    else:
        return render_template("login.html", form = form)

if __name__ == "__main__":
    app.run(debug=True)