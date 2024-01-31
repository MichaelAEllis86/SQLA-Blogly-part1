from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def connect_db(app):
    db.app=app
    db.init_app(app)

#models go below


class User(db.Model):
    """Users model"""

    __tablename__ = "users"

    def __repr__(self):
        u=self
        return f"<user id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url} "

    id= db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
    first_name=db.Column(db.String(50),
                        nullable=False,
                        unique=False)
    last_name=db.Column(db.String(50),
                        nullable=False,
                        unique=False)
    image_url=db.Column(db.Text, 
                        nullable=True,
                        unique=False,
                        default='https://i.imgur.com/SHxfpjI.jpg'
                        )
#problem exists with image_url model will not accept strings longer than 50, creates a pyscopig error -------->Fixed!
#problem exits with default image, for one it doens't work because of imgur in a img tag, also the default is not filling when the form is left blank ----->Need to fix!

    
    