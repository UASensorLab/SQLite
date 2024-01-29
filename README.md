# SQLite
## First
pip install Flask SQLAlchemy
## Second 
templates file have three html File, index login, register. (This is APP file)
## third 
In terminal run python + APP.py file , path
if the port not work
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5002)
In here change port number to 5001,5003 so on.
