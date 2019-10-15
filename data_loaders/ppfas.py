import csv
from pathlib import Path
from flask import Flask
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/amfiindia_com_db_dev"
mongo = PyMongo(app)

file_names = ['jan-mar.csv', 'apr-jun.csv', 'july-sep.csv']

for filename in file_names:
    with open("{0}/data/ppfas/{1}".format(Path.cwd(), filename)) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            if 'INF879O01027' in row:
                mongo.db.ppfas.insert_one(dict(
                    scheme_code=row[0],
                    scheme_name=row[1],
                    isin=row[2],
                    nav=float(row[4]),
                    captured_on=datetime.datetime.strptime(row[-1], "%d-%b-%Y")
                ))

