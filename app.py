from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class BlogPosts(db.Model):
    id= db.Column(db.Integer , primary_key= True )
    title = db.Column(db.String(30) , nullable = False)
    content = db.Column(db.Text , nullable = False)
    author = db.Column(db.String(20) , nullable = False , default = 'N/A')
    date_created = db.Column(db.DateTime , default = datetime.utcnow)

    def __repr__(self) -> str:
        return 'blogpost' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts' , methods = ['GET', 'POST'])
def posts():
    if request.method=='POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        

        new_post = BlogPosts(title = post_title , content = post_content , author = post_author)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts')

    else:
        all_posts   = BlogPosts.query.order_by(BlogPosts.date_created).all()
    return render_template('posts.html' , posts = all_posts)

@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post = BlogPosts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/posts')


@app.route('/posts/update/<int:id>' , methods=['GET', 'POST'])
def update_post(id):
    post = BlogPosts.query.get_or_404(id)
    if request.method=='POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    
    else:
        return render_template('update.html' , post=post)

@app.route('/posts/new' , methods=['GET', 'POST'])
def new_post():
    if request.method=='POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']

        if post_title and post_content and post_author =='':

            return render_template('new_post.html')
        else:

            new_post = BlogPosts(title = post_title , content = post_content , author = post_author)

            db.session.add(new_post)
            db.session.commit()

            return redirect('/posts')
        
    else:
        return render_template('new_post.html')



if __name__=="__main__":
    app.run(debug=True)
