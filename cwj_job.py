from Web_Scrapper import *
from flask import Flask, render_template, request, redirect, send_file

app = Flask("SuperScrapper")

db = {}

@app.route("/")
def home():
    return render_template("potato.html")

@app.route("/report")
def report():
    word = request.args.get("word") ## Query argument
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            job1 = indeed_get_jobs(word)
            job2 = SO_get_jobs(word)
            jobs = job1 + job2
            db[word] = jobs
    else:
        return redirect("/")
    return render_template('report.html',
                           SearchingBy=word,
                           resultNumber=len(jobs),
                           jobs = jobs) ## Query argument to render_template

@app.route("/export")
def export():
    try:
        word = request.args.get("word") ## Query argument
        if word:
            word = word.lower()
        else:
            raise Exception()
        jobs = db.get(word)
        if jobs:
            save_to_file(word,jobs)
        else:
            raise Exception()
        return send_file(filename_or_fp=f"{word}_jobs.csv")
    except:
#         import pdb;pdb.set_trace()
        return redirect("/")

app.run(host="0.0.0.0")