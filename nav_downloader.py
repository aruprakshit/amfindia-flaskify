import yaml
from pathlib import Path
import requests
import json
from bs4 import BeautifulSoup
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/amfiindia_com_db_dev"
mongo = PyMongo(app)

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open("{}/data/ppfas.yml".format(Path.cwd())) as file:
    metadata = yaml.load(file, Loader=Loader)
    r = requests.post(
        metadata["url"],
        data=metadata["payload"],
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "My User Agent 1.0",
        },
    )
    soup = BeautifulSoup(r.text)
    for tr in soup.select("tbody tr")[5:]:
        tds = [td for td in tr.children if td != '\n']
        print("NAV: {0} on {1}".format(tds[0].get_text(strip=True), tds[-1].get_text(strip=True)))
        mongo.db.ppfas.insert_one(dict(nav=tds[0].get_text(strip=True), ))

