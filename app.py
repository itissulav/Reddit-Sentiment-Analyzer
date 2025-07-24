from flask import Flask
from controllers.IndexController import index_blueprint
from controllers.ResultsController import results_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(index_blueprint)
app.register_blueprint(results_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
