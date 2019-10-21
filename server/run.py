from dotenv import load_dotenv

from main.db import db
from main.app import create_app

load_dotenv()

app = create_app('default')

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()  # create the data.db unless it's already existed


if __name__ == '__main__':
    app.run(port=5000, debug=False)
