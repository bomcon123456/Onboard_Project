from dotenv import load_dotenv

from main.app import create_app
from main.db import db

load_dotenv()

app = create_app('development')

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()  # create the data.db unless it's already existed


if __name__ == '__main__':
    app.run(port=5000, debug=False)
