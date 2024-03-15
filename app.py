from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms.fields.simple import TextAreaField
# from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from mygenerator import generate_barcode

app = Flask(__name__)
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSOR CLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)

# Articles = Articles()


@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    if result > 0:
        articles = cur.fetchall()
        # print(articles)
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found !'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()


# Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    return render_template('article.html', article=article)


# Register Form Class
class RegisterForm(Form):
    fullname = StringField('Full Name', [validators.length(min=2, max=100)])
    username = StringField('Username', [validators.length(min=2, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        fullname = form.fullname.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(fullname, email, username, password) VALUES(%s, %s, %s, %s)",
                    (fullname, email, username, password))
        # Commit to DB
        mysql.connection.commit()
        # Close cursor
        cur.close()
        flash('You are now registered and can log in !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data[4]
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # app.logger.info('PASSWORD MATCHED')
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'User not found'
            return render_template('login.html', error=error)
    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login !', 'danger')
            return redirect(url_for('login'))

    return wrap


# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out !', 'success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    result = cur.execute("SELECT * FROM articles")
    if result > 0:
        articles = cur.fetchall()
        # print(articles)
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found !'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

# Article Form Class
class ArticleForm(Form):
    code = StringField('Code')
    title = StringField('Title', [validators.length(min=2, max=100)])
    body = TextAreaField('Body', [validators.length(min=15)])


# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    form.code.data = generate_barcode()

    if request.method == 'POST' and form.validate():
        code = form.code.data
        title = form.title.data
        body = form.body.data

        # Create a cursor
        cur = mysql.connection.cursor()
        # Execute the insertion query
        cur.execute("INSERT INTO articles(code, title, body, author) VALUES (%s, %s, %s, %s)",
                    (code, title, body, session['username']))
        # Commit the transaction
        mysql.connection.commit()
        # Close the cursor
        cur.close()
        flash('Article Created !', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)

# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create a cursor
    cur = mysql.connection.cursor()
    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()

    # Get Form
    form = ArticleForm(request.form)
    # Populate article form fields
    form.code.data = article[1]
    form.title.data = article[2]
    form.body.data = article[3]

    if request.method == 'POST' and form.validate():
        # Get updated data from the form
        title = request.form['title']
        body = request.form['body']

        # Create a cursor
        cur = mysql.connection.cursor()
        # Execute the update query
        cur.execute("UPDATE articles SET title = %s, body = %s WHERE id = %s", (title, body, id))
        # Commit the transaction
        mysql.connection.commit()
        # Close the cursor
        cur.close()
        flash('Article Updated!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # Execute the delete query
    cur.execute("DELETE FROM articles WHERE id = %s", [id])
    # Commit the transaction
    mysql.connection.commit()
    # Close the cursor
    cur.close()
    flash('Article Deleted!', 'success')
    return redirect(url_for('dashboard'))
# main function
if __name__ == '__main__':
    app.secret_key = 'mine21'
    app.run(debug=True)