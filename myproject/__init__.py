from flask import Flask,render_template
from .models import db
from .views import main_bp


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.sqlite'
    db.init_app(app)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
 

    return app
