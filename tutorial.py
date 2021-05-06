from app import app, db
from app.models import User, Quiz, Tutorial

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Quiz': Quiz, 'Tutorial': Tutorial}

if __name__=="__main__":
    app.run(host='127.0.0.9', port=5000, debug=True)
