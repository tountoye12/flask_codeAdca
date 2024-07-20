from flask import Flask


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/')
@app.route('/home')
def home():
    return 'Hello, World!'


@app.route('/reporter/<int:reporter_id>')
def reporter(reporter_id):
    return f'''
    <h2>Reporter {reporter_id} Bio</h2>
    <a href="/">Return to home page</a>
    '''


# declaring the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary key column
    title = db.Column(db.String(80), index=True, unique=True)  # book title
    author_name = db.Column(db.String(50), index=True, unique=False)  # author name
    author_surname = db.Column(db.String(80), index=True, unique=False)  # author surname
    month = db.Column(db.String(20), index=True, unique=False)  # the month of the book suggestion
    year = db.Column(db.Integer, index=True, unique=False)  # tthe year of the book suggestion

    # Get a nice printout for Book objects
    def __repr__(self):
        return "{} in: {},{}".format(self.title, self.month, self.year)


# Add your columns for the Reader model here below.
class Reader(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), index = True, unique = False)
    surname = db.Column(db.String(80), unique = False, index = True)
    email = db.Column(db.String(120), unique = True, index = True)
    #add your relationship column here
    reviews = db.relationship("Review", backref="reviewer",
    lazy="dynamic")
    # get a nice printout for Reader objects
    def __repr__(self):
        return "Reader: {}".format(self.email)


#declaring the Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
    stars = db.Column(db.Integer, unique = False) #a review's rating
    text = db.Column(db.String(200), unique = False) #a review's text
    #here below is the foreign key column linking to the primary key (id) of the Book model (book).
    #Note the lower case here: 'book.id' instead of 'Book.id'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id')) #foreign key column
    #Checkpoint 1: your code here below (be careful about the indentation)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('reader.id'))

    #get a nice printout for Review objects
    def __repr__(self):
        return "Review: {} stars: {}".format(self.text, self.stars)

if __name__ == '__main__':
    app.run()
