from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# Place import statement at the bottom to avoid circular referencing
from app import views # noqa
