from flask import Flask

def create_app():
    app = Flask(__name__)

    # 블루 프린트
    from .views import main_views, itooza_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(itooza_views.bp)

    return app
