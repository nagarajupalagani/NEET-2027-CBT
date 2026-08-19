
import os, sqlite3, secrets
from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
DB = os.environ.get("DATABASE_PATH", "neet_cbt.db")
TEACHER_PASSWORD_HASH = os.environ.get("TEACHER_PASSWORD_HASH")

QUESTIONS = [
("Units & Measurements","The dimensional formula of impulse is:",["[MLT⁻¹]","[ML²T⁻²]","[MLT⁻²]","[M⁰L⁰T⁰]"],0),
("Units & Measurements","Which pair has the same dimensions?",["Work and torque","Force and pressure","Momentum and energy","Power and impulse"],0),
("Units & Measurements","The SI unit of pressure is:",["N","Pa","J","W"],1),
("Units & Measurements","If x = at², the dimensions of a are:",["[LT⁻¹]","[LT⁻²]","[L²T⁻²]","[T⁻²]"],1),
("Units & Measurements","Which is dimensionless?",["Strain","Surface tension","Young's modulus","Pressure"],0),
("Units & Measurements","1 micrometre equals:",["10⁻³ m","10⁻⁶ m","10⁻⁹ m","10⁶ m"],1),
("Units & Measurements","The number of significant figures in 0.00450 is:",["2","3","4","5"],1),
("Units & Measurements","Percentage error in a quantity x = 20 ± 0.4 is:",["0.5%","2%","4%","20%"],1),
("Units & Measurements","Which equation can be checked using dimensional analysis?",["F = ma","v = u + at","Both A and B","Neither"],2),
("Units & Measurements","Dimensional analysis cannot determine:",["Dimensions of a quantity","Whether an equation is homogeneous","Numerical dimensionless constants","Dimensions of a product"],2),
("Units & Measurements","The dimensional formula of gravitational constant G is:",["[MLT⁻²]","[M⁻¹L³T⁻²]","[ML³T⁻²]","[M⁻¹L²T⁻¹]"],1),
("Units & Measurements","If length is measured with 2% error, the percentage error in area is:",["1%","2%","4%","8%"],2),
("Units & Measurements","A vernier calipers is primarily used to measure:",["Only time","Length/diameter/depth","Mass","Temperature"],1),
("Units & Measurements","Which is an SI base quantity?",["Force","Energy","Electric current","Pressure"],2),
("Units & Measurements","The SI unit of frequency is:",["rad/s","Hz","N","C"],1),
("Motion in a Straight Line","The slope of a position-time graph gives:",["Acceleration","Velocity","Displacement","Force"],1),
("Motion in a Straight Line","The area under a velocity-time graph gives:",["Acceleration","Displacement","Jerk","Speed"],1),
("Motion in a Straight Line","A particle starts from rest with acceleration 2 m/s². Its speed after 5 s is:",["5 m/s","10 m/s","20 m/s","25 m/s"],1),
("Motion in a Straight Line","A body moving with constant velocity has:",["Zero acceleration","Increasing acceleration","Constant non-zero acceleration","Changing speed"],0),
("Motion in a Straight Line","A particle has u = 10 m/s, a = −2 m/s². Time to stop is:",["2 s","5 s","10 s","20 s"],1),
("Motion in a Straight Line","For uniformly accelerated motion, which relation is correct?",["v = u + at","v = u + a/t","s = ut + at","v² = u² + as"],0),
("Motion in a Straight Line","A car travels 20 m in first 2 s and 40 m in next 2 s. Its acceleration is:",["2.5 m/s²","5 m/s²","10 m/s²","15 m/s²"],1),
("Motion in a Straight Line","If x = 3t² + 2t + 1, velocity at t = 2 s is:",["8 m/s","10 m/s","14 m/s","16 m/s"],2),
("Motion in a Straight Line","If x = 4t³, acceleration at t = 1 s is:",["4 m/s²","8 m/s²","24 m/s²","12 m/s²"],2),
("Motion in a Straight Line","A freely falling body starts from rest. Taking g = 10 m/s², displacement in 3 s is:",["15 m","30 m","45 m","90 m"],2),
("Motion in a Straight Line","At the highest point of a vertically thrown ball, its:",["Velocity and acceleration are zero","Velocity is zero, acceleration is g downward","Acceleration is zero, velocity is g","Both are maximum"],1),
("Motion in a Straight Line","Two cars move in the same direction with speeds 20 and 15 m/s. Relative speed is:",["5 m/s","15 m/s","20 m/s","35 m/s"],0),
("Motion in a Straight Line","Two objects move in opposite directions at 10 and 12 m/s. Relative speed is:",["2 m/s","10 m/s","12 m/s","22 m/s"],3),
("Motion in a Straight Line","A velocity-time graph is a horizontal line above the time axis. The body has:",["Constant velocity","Constant acceleration","Increasing velocity","Zero displacement"],0),
("Motion in a Straight Line","A particle covers equal distances in equal time intervals. It has:",["Uniform speed","Zero speed","Variable speed","Infinite acceleration"],0),
("Motion in a Straight Line","Average velocity is zero when:",["Speed is zero throughout","Net displacement is zero","Distance is zero only","Acceleration is zero"],1),
("Motion in a Straight Line","A body moves 10 m east and then 10 m west. Distance and displacement are:",["0, 20 m","20 m, 0","10 m, 10 m","20 m, 20 m"],1),
("Motion in a Straight Line","If acceleration is opposite to velocity, the speed:",["Must increase","Must decrease","Must remain constant","Becomes infinite"],1),
("Motion in a Straight Line","The instantaneous velocity is:",["ds/dt","dt/ds","d²s/dt²","s/t always"],0),
("Motion in a Straight Line","A particle's position is x = 5t − t². It changes direction at:",["t = 2.5 s","t = 5 s","t = 10 s","t = 0"],0),
("Motion in a Plane","A vector has components 3 and 4. Its magnitude is:",["3","4","5","7"],2),
("Motion in a Plane","Two perpendicular vectors of magnitudes 6 and 8 have resultant:",["2","10","14","48"],1),
("Motion in a Plane","If A·B = 0, the vectors are:",["Parallel","Perpendicular","Anti-parallel","Equal"],1),
("Motion in a Plane","The magnitude of A × B is maximum when angle between them is:",["0°","30°","60°","90°"],3),
("Motion in a Plane","For a projectile launched horizontally, horizontal acceleration is:",["g","−g","0","g/2"],2),
("Motion in a Plane","A projectile is launched at 20 m/s at 30°. Taking g = 10 m/s², time of flight is:",["1 s","2 s","3 s","4 s"],1),
("Motion in a Plane","For a projectile on level ground, maximum range occurs at:",["30°","45°","60°","90°"],1),
("Motion in a Plane","For a projectile on level ground, range is:",["u² sinθ/g","u² sin2θ/g","u² cos2θ/g","2u²/g"],1),
("Motion in a Plane","At the highest point of projectile motion, the vertical component of velocity is:",["u","u cosθ","0","g"],2),
("Motion in a Plane","At the highest point of a projectile, acceleration is:",["Zero","g upward","g downward","Horizontal"],2),
("Motion in a Plane","For projectile motion without air resistance, horizontal velocity is:",["Constant","Zero","Increasing","Decreasing"],0),
("Motion in a Plane","A projectile is fired at 30° and another at 60° with same speed. Their ranges are:",["First larger","Second larger","Equal","Cannot compare"],2),
("Motion in a Plane","If a vector A = 3i + 4j, its unit vector is:",["3i+4j","(3/5)i+(4/5)j","(4/5)i+(3/5)j","5i+5j"],1),
("Motion in a Plane","The angle between vectors A and −A is:",["0°","45°","90°","180°"],3),
("Motion in a Plane","If two vectors of magnitudes 5 and 12 are perpendicular, their resultant is:",["7","13","17","60"],1)
]

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
    c=db()
    c.execute("""CREATE TABLE IF NOT EXISTS results(
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, roll TEXT NOT NULL,
      score INTEGER NOT NULL, correct INTEGER NOT NULL, wrong INTEGER NOT NULL,
      unattempted INTEGER NOT NULL, time_taken INTEGER NOT NULL, submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
      answers TEXT NOT NULL)""")
    c.commit(); c.close()

@app.route("/")
def home():
    return render_template("student.html", count=len(QUESTIONS), duration=60)

@app.route("/submit", methods=["POST"])
def submit():
    data=request.get_json(force=True)
    name=str(data.get("name","")).strip()[:100]
    roll=str(data.get("roll","")).strip()[:50]
    answers=data.get("answers",[])
    elapsed=int(data.get("elapsed",0))
    if not name or not roll or not isinstance(answers,list): return jsonify({"error":"Name, roll number and answers are required"}),400
    answers=(answers+[None]*len(QUESTIONS))[:len(QUESTIONS)]
    correct=sum(a==q[3] for a,q in zip(answers,QUESTIONS) if isinstance(a,int))
    wrong=sum(a is not None and a!=q[3] for a,q in zip(answers,QUESTIONS))
    un=len(QUESTIONS)-correct-wrong
    score=correct*4-wrong
    c=db()
    c.execute("INSERT INTO results(name,roll,score,correct,wrong,unattempted,time_taken,answers) VALUES(?,?,?,?,?,?,?,?)",
              (name,roll,score,correct,wrong,un,elapsed,json.dumps(answers)))
    c.commit(); c.close()
    return jsonify({"score":score,"correct":correct,"wrong":wrong,"unattempted":un})

@app.route("/teacher/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        pw=request.form.get("password","")
        if TEACHER_PASSWORD_HASH and check_password_hash(TEACHER_PASSWORD_HASH,pw):
            session["teacher"]=True; return redirect(url_for("dashboard"))
        return render_template("login.html", error="Incorrect password.")
    return render_template("login.html", error=None)

@app.route("/teacher")
def dashboard():
    if not session.get("teacher"): return redirect(url_for("login"))
    c=db(); rows=c.execute("SELECT * FROM results ORDER BY score DESC, time_taken ASC").fetchall(); c.close()
    return render_template("dashboard.html", rows=rows)

@app.route("/teacher/logout")
def logout():
    session.clear(); return redirect(url_for("login"))

@app.route("/teacher/export")
def export():
    if not session.get("teacher"): abort(403)
    import csv, io
    c=db(); rows=c.execute("SELECT name,roll,score,correct,wrong,unattempted,time_taken,submitted_at FROM results ORDER BY score DESC").fetchall(); c.close()
    out=io.StringIO(); w=csv.writer(out); w.writerow(rows[0].keys() if rows else ["name","roll","score","correct","wrong","unattempted","time_taken","submitted_at"])
    for r in rows: w.writerow(list(r))
    from flask import Response
    return Response(out.getvalue(),mimetype="text/csv",headers={"Content-Disposition":"attachment; filename=neet_results.csv"})

@app.route("/teacher/clear", methods=["POST"])
def clear():
    if not session.get("teacher"): abort(403)
    c=db(); c.execute("DELETE FROM results"); c.commit(); c.close()
    return redirect(url_for("dashboard"))

init()
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
