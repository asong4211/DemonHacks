from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import *
from wtforms.widgets import TextArea

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Flying_Squirrel/Documents/DemonHacks/Demo/database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.before_request
def before_request():
    initialize_db() #initialize database if needed

@app.teardown_request
def teardown_request(exception):
    db1.close()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class PostForm(FlaskForm):
    title = StringField('Title',validators=[InputRequired()])
    post = StringField('Post',validators=[InputRequired()], widget = TextArea())
    categories = SelectField('Categories', choices = [
    ('general','General'),
    ('prejudice','Prejudice and Discrimination'),
    ('stress','School Stress'),
    ('death','Grief and Death'),
    ('addiction','Addiction and Substance Abuse'),
    ('romantic','Romantic Relationship'),
    ('sexualOrient','Sexual Orientation'),
    ('body','Body Image & Eating Disorder')])



@app.route('/create/', methods=['POST','GET'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'GET':
        return render_template('newPost.html',form = form)
    else:
        if form.validate_on_submit():
            Post.create(date = datetime.datetime.now(),
                        title = form.title.data,
                        text = form.post.data,
                        category = form.categories.data)
            categories = form.categories.data;
            print(categories)
            if categories == "general":
                return redirect(url_for('general'))
            if categories == "prejudice":
                return redirect(url_for('prejudice'))
            if categories == "stress":
                return redirect (url_for('stress'))
            if categories == "death":
                return redirect(url_for('grief'))
            if categories == "body":
                return redirect(url_for('body'))
            if categories == "addiction":
                return redirect(url_for('addiction'))
            if categories == "romantic":
                return redirect(url_for('romantic'))
            if categories == "sexualOrient":
                return redirect(url_for('sexualOrient'))
            else:
                return redirect(url_for('general'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user) #second param:
                return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',posts= Post.select().where(Post.category == "general").order_by(Post.date.desc()))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/retrieve', methods = ["POST","GET"])
@login_required
def retrieve():
    name = request.args.get('myPost')
    print(name)
    post = Post.select().where(Post.title == name)
    return render_template('userPost.html', post = post)


#This is to route to different category.

@app.route('/general/',methods=['POST', 'GET'])
@login_required
def general():
    posts = Post.select().where(Post.category == "general").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)

@app.route('/prejudice/', methods = ['POST','GET'])
@login_required
def prejudice():
    posts = Post.select().where(Post.category == "prejudice").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)

@app.route('/stress/', methods = ['POST','GET'])
@login_required
def stress():
    posts = Post.select().where(Post.category == "stress").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)

@app.route('/grief/', methods = ['POST', 'GET'])
@login_required
def grief():
    posts = Post.select().where(Post.category == "death").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)

@app.route('/body/', methods = ['POST', 'GET'])
@login_required
def body():
    posts = Post.select().where(Post.category == "body").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)

@app.route('/addiction/', methods = ['POST', 'GET'])
@login_required
def addiction():
    posts = Post.select().where(Post.category == "addiction").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)

@app.route('/romantic/', methods = ['POST','GET'])
@login_required
def romantic():
    posts = Post.select().where(Post.category == "romantic").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)

@app.route('/sexualOrient/', methods = ['POST','GET'])
@login_required
def sexualOrient():
    posts = Post.select().where(Post.category == "sexualOrient").order_by(Post.date.desc())
    return render_template('dashboard.html', posts = posts)


if __name__ == '__main__':
    app.run(debug=True)
