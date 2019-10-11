from db import db
from ma import ma
from app import app

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()  # create the data.db unless it's already existed


if __name__ == '__main__':
    app.run(port=5000)