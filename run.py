
from flask import Flask
from billing_system import app

if __name__ == '__main__':
    Flask.run(app, debug=True)
