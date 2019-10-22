from flask import Flask
import os


app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/packages')
def packages():
    return 'Hello World!'

@app.route('/packages/<name>')
def packages_name():
    return 'package_name'

if __name__ == '__main__':
    print(app.config)
    app.run()

