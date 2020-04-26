import os
from flask import Flask


app = Flask(__name__)


from Question_Mark import routes
