# <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
#    <link rel="preconnect" href="https://fonts.gstatic.com">


from flask import Flask , render_template ,url_for , redirect ,request , flash 
#       THIS BELONGES TO LOGIN / REGISTER
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField , SubmitField , PasswordField , BooleanField
from wtforms.validators import InputRequired  , Length , Email
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_user , login_required , logout_user , current_user


app = Flask(__name__)

@app.route("/")
def home():
  return render_template('home.html' , nadpis = "Home")

@app.route("/sorry")
def sorry():
  return render_template('sorry.html' , nadpis = "Sorry")

@app.route("/description")
def description():
  return render_template('description.html' , nadpis = "Description")

#-----------------------------------------------#
#------THIS IS LOGIN AND REGISTER TO COPY-------#
#------THIS IS LOGIN AND REGISTER TO COPY-------#
#-----------------------------------------------#
app.config['SECRET_KEY'] = 'totomabyttajnykluc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'users' : 'sqlite:///users.db' ,
    'users_text' : 'sqlite:///text.db', #this is for text editor
}


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class users(UserMixin , db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(15) , unique = True)
    password = db.Column(db.String(80) , unique = True)
    email = db.Column(db.String(80))


class LoginForm(FlaskForm):
    username = StringField('username' , validators=[InputRequired() , Length(min = 5 , max= 20)])
    password = PasswordField('password' , validators=[InputRequired() , Length(min = 8 , max= 30)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email' , validators=[InputRequired() , Email(message = 'Invalid Email') , Length( max= 50)])
    username = StringField('username' , validators=[InputRequired() , Length(min = 5 , max= 20)])
    password = PasswordField('password' , validators=[InputRequired() , Length(min = 8 , max= 30)])

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route("/login" , methods=['GET' , 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.query.filter_by(username = form.username.data).first()
        if user:
            if check_password_hash(user.password , form.password.data):
                login_user(user , remember=form.remember.data)
                return redirect(url_for('admin'))
        return '<h1> Invalid username or password </h1>'
    return render_template('login.html' , nadpis = "Login" , form = form)

@app.route("/signup" , methods=['GET' , 'POST'])
def signup():
    form = RegisterForm()   
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data , method='sha256')
        new_user = users(username = form.username.data , email = form.email.data , password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('signup.html' , nadpis = "Register" , form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# DONT FORGOT TO WRITE IN COMMAND PROMPT  "python" than "from app import db" than "db.create_all()" and "exit()" 



#-----------------------------------------------#
#------END OF LOGIN AND REGISTER FORM-----------#
#------END OF LOGIN AND REGISTER FORM-----------#
#-----------------------------------------------#





#-----------------------------------------------#
#------START OF TEXT EDITOR AND ADMIN PAGE------#
#------START OF TEXT EDITOR AND ADMIN PAGE------#
#-----------------------------------------------#
class EditorData(db.Model):
    __bind_key__ = 'users_text'
    id = db.Column(db.Integer , primary_key = True)
    title = db.Column(db.String)
    text = db.Column(db.String(80))
    users_id = db.Column(db.Integer)
    image = db.Column(db.String)
    html = db.Column(db.Text)

@app.route("/admin")
@login_required
def admin():
    page = request.args.get('page', 1, type=int)
    admin_article = EditorData.query.paginate(page = page , per_page = 6)
    return render_template('admin.html' , nadpis = "Admin" , admin_article = admin_article)

@app.route("/addtext" , methods=['GET' , 'POST'])
@login_required
def addtext(): 
    user = current_user.id
    name = ""
    if request.method == "POST":
        if request.method == 'POST' and 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            name = filename
        new_data = EditorData(html = request.form.get('editordata') , users_id = user , title = request.form.get('title') , text = request.form.get('text') , image = name )
        db.session.add(new_data)
        db.session.commit()
    return render_template('addtext.html' , nadpis = "Add Text" )

@app.route("/text_example/<int:id>")
def text_example(id):
    data = EditorData.query.get(id)
    return render_template('text_example.html' , nadpis = "Text" , data = data.html , art_title = data.title)

@app.route('/article')
def article(): 
    page = request.args.get('page', 1, type=int)
    articles = EditorData.query.paginate(page = page , per_page = 6)
    return render_template("article.html" , articles = articles )

@app.route('/deleteArticle/<int:id>' , methods=['POST'])
def deleteArticle(id):
    uploads = EditorData.query.get(id)
    db.session.delete(uploads)
    db.session.commit()
    return render_template("home.html" , nadpis = "Home")


#-----------------------------------------------#
#------END OF TEXT EDITOR AND ADMIN PAGE--------#
#------END OF TEXT EDITOR AND ADMIN PAGE--------#
#-----------------------------------------------#

#
#           THIS IS FOR UPLOADING FOLDER
#
from flask_uploads import configure_uploads, IMAGES, UploadSet
from werkzeug.utils import secure_filename

photos = UploadSet('photos', IMAGES)
 
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
 
configure_uploads(app, photos)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)



