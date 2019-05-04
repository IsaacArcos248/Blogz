from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['POST','GET'])
def new_post():

    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']

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
            new_entry = Blog(title,body)
            db.session.add(new_entry)
            db.session.commit()
            return redirect("/blog?id={}".format(new_entry.id))

    return render_template('newpost.html', title = "Add A Blog Entry")


@app.route('/blog', methods = ['POST','GET'])
def index_2():
    blog_id = request.args.get('id')

    if not blog_id:
        entries = Blog.query.all()
        return render_template('blog.html' ,title='Blog Entries!',entries=entries) 
    else:
        entry = Blog.query.get(blog_id)
        return render_template('record.html', entry = entry, title = 'Blog Post')


@app.route('/blog', methods=['GET'])
def display():
    if request.method == "GET":
        blog_id = request.args.get('id')
        return(render_template('record.html', title = title ,blog_id = blog_id ))



if __name__ == '__main__':
    app.run()