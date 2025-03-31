from app import app
from flask_restful import Api
from app.api import initialize_api

api = Api(app) 
print("Initializing API routes...")
initialize_api(api)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)