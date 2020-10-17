from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from league import getLeagueData
app = Flask(__name__, instance_relative_config=True)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reminders.html', methods = ["GET","POST"])
def reminders():
    if request.method  == "POST":
        req = request.form
        league_ID = req.get("league_ID")
        espn_s2 = req.get("espn_s2")
        swid = req.get("swid")
        teamName = req.get("teamName")
        data = getLeagueData(league_ID,espn_s2,swid,teamName)
        parts = data.split("|") #best players of each position -> free agency replacements
        topPlayers = parts[0].split("/") #QB, RB, WR, TE, FLEX, DST, K in that order
        
        return redirect(url_for('advice', topQBs = topPlayers[0][0:len(topPlayers[0])-1], topRBs = topPlayers[1][0:len(topPlayers[1])-1], topWRs = topPlayers[2][0:len(topPlayers[2])-1],topTEs = topPlayers[3][0:len(topPlayers[3])-1],  topFLEXs = topPlayers[4][0:len(topPlayers[4])-1], topDSTs = topPlayers[5][0:len(topPlayers[5])-1], topKs = topPlayers[7][0:len(topPlayers[7])-1], freeAgencyData = parts[1]))
    return render_template('reminders.html')    
  

@app.route('/advice.html')
def advice():
    return render_template('advice.html',freeAgencyData = request.args.get('freeAgencyData'), topQBs = request.args.get('topQBs'), topRBs = request.args.get('topRBs'),topWRs = request.args.get('topWRs'),topTEs = request.args.get('topTEs'), topFLEXs = request.args.get('topFLEXs'), topDSTs = request.args.get('topDSTs'), topKs = request.args.get('topKs'))