import os
from kni import app

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8080)), host=os.environ.get('HOST', '0.0.0.0'))
