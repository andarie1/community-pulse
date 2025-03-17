from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .question import *
from .response import *
from .statistic import *