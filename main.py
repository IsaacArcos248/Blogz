from flask import Flask, request, redirect, render_template,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key="Pullth3l3v3rKronk"
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


# @app.before_request
# def require_login():
#     allowed_routes = ['login','blog','index','signup']
#     if request.endpoint not in allowed_routes and 'username' not in session:
#         return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method == ['POST']:
        username=request.form['username']
        password=request.form['password']
        verification=request.form['passver']

        username_error = ''
        password_error = ''
        verification_error = ''

        if not username:
            username_error = 'Username field must have a valid data type'
        else:
            if len(username) < 3 or len(username)> 20:
                username_error = "The Username must be 3-20 characters in lenght!"

        if not password:
            password_error = 'Password must not be empty'
        else:
            if password != verification:
                password_error = 'Your Password Must Match the Password in the Verification Field!'
                password = ''

        if not verification:
            verification_error = "Please enter the password again to verify"
        else:
            if verification != password:
                verification_error = 'Your Password Must Match the Password Field !'
                verification = ''

        if username_error or password_error or verification_error:
            return render_template('signup.html', username = username, password = password, verification = verification, 
            username_error = username_error, password_error = password_error, verification_error = verification_error)
        else:
            new_user=User(username,password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/blog')

    return render_template('signup.html', username = '', password = '', verificaton = '', username_error = '', password_error = '', verification_error = '')

@app.route('/login', methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        user_error = ''
        password_error = ''

        if not username:
            user_error = "The username does not exist!"
        else:
            user_error = ''
        
        if not password:
            password_error = "The password is incorrect"
        else:
            password_error = ''

        if username and user.password == password:
            session["username"]= username
            return redirect ("/newpost")
        else:
            return redirect("/login",user_error = user_error, password_error = password_error) 

    return render_template('login.html', username = '', password = '', username_error = '', password_error = '')

@app.route('/newpost')
def post():
    return render_template('newpost.html', title = "New Entry")


@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()

        title_error = ''
        body_error=''

        if not title:
            title_error = "Please review your blog title to ensure it is filled out correctly!"
        else:
            title_error = '' 


        if not body:
            body_error = "Please review your blog body to ensure it is filled out correctly!"
        else:
            body_error = ''

    
        if title_error or body_error:
            return render_template('newpost.html', title = title, body = body, title_error = title_error, body_error=body_error)
        else:
            new_entry = Blog(title,body,owner)
            db.session.add(new_entry)
            db.session.commit()
            return redirect("/blog?id={}".format(new_entry.id))

@app.route('/blog', methods = ['POST','GET'])
def index_2():
    blog_id = request.args.get('id')

    if not blog_id:
        entries = Blog.query.all()
        return render_template('blog.html' ,title='Blog Entries!',entries=entries) 
    else:
        entry = Blog.query.get(blog_id)
        return render_template('record.html', entry = entry, title = 'Blog Post')

@app.route('/blog', methods=['GET',"POST"])
def display_blog():
    if request.method == "GET":
        blog_id = request.args.get('id')
        return(render_template('record.html', title = title ,blog_id = blog_id ))

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()