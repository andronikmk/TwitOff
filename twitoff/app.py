"""Main application and routing logic for TwitOff"""
# test commit after pull request.
from flask import Flask, render_template, request
from .models import DB, User
#from .predict import predict_user
from .twitter import add_or_update_user
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def create_app():
    """Create and configure an instance of the Flask applications."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['ENV'] = getenv('ENV')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)
    
    @app.route("/user", methods=['POST'])
    @app.route("/user/<name>", methods=['GET'])
    def user(name=None):
        message = ''
        import pdb; pdb.set_trace()
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfullt added!'.format(name)
            tweets = User.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                                             message=message)

    @app.route("/reset")
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])
   
    return app