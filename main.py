from flask import Flask, render_template,request,redirect,send_file
from scrapper import get_jobs
app = Flask("SuperScrapper")
from exporter import save_to_file


db = {}

@app.route("/")
def home():
  return render_template("index.html")


@app.route("/report")
def report():
  word = request.args.get('word')
  location = request.args.get('loc')
  if word:
    word=word.lower()
    fromDb = db.get(word)   
    if fromDb:
      jobs = fromDb
    else:
      jobs = get_jobs(word,location)
      db[word] = jobs
  else:
    return redirect("/")
  return render_template(
    "report.html",
    searchingBy=word,
    resultNumber = len(jobs),
    jobs = jobs
  )


@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word:
      raise Exception()
    word = word.lower()
    jobs = db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")



app.run(host="0.0.0.0")