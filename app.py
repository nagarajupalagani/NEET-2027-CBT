from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DB_NAME = "results.db"
DURATION = 60


# =========================================================
# QUESTIONS
# =========================================================

QUESTIONS = [

["Work, Energy & Power",
" A force of 10 N acts on a body and displaces it by 5 m in the direction of the force. The work done is:",
["10 J", "25 J", "50 J", "100 J"], 2],

["Work, Energy & Power",
"A body is displaced through 10 m by a force of 20 N acting at 60° to the displacement. Work done is:",
["50 J", "100 J", "150 J", "200 J"], 1],

["Work, Energy & Power",
"The work done by a force is zero when the angle between force and displacement is:",
["0°", "45°", "90°", "180°"], 2],

["Work, Energy & Power",
"A person carries a bag horizontally at constant speed. The work done by the person's upward force on the bag is:",
["Positive", "Negative", "Zero", "Maximum"], 2],

["Work, Energy & Power",
"The SI unit of work is:",
["Newton", "Joule", "Watt", "Pascal"], 1],

["Work, Energy & Power",
"One joule is equal to:",
["1 N/m", "1 N m", "1 kg m", "1 W/s"], 1],

["Work, Energy & Power",
"A force F = 2x acts on a particle along the x-axis. Work done from x = 0 to x = 3 m is:",
["3 J", "6 J", "9 J", "18 J"], 2],

["Work, Energy & Power",
"The work done by a variable force is obtained from the:",
["Slope of F-x graph", "Area under F-x graph", "Area under v-t graph", "Slope of v-t graph"], 1],

["Work, Energy & Power",
"A 2 kg body moving with velocity 5 m/s has kinetic energy:",
["10 J", "20 J", "25 J", "50 J"], 2],

["Work, Energy & Power",
"If the velocity of a body is doubled, its kinetic energy becomes:",
["2 times", "3 times", "4 times", "8 times"], 2],

["Work, Energy & Power",
"The kinetic energy of a body of mass m moving with speed v is:",
["mv", "mv²", "½mv²", "2mv²"], 2],

["Work, Energy & Power",
"A body of mass 4 kg has kinetic energy 200 J. Its speed is:",
["5 m/s", "10 m/s", "20 m/s", "25 m/s"], 1],

["Work, Energy & Power",
"The work-energy theorem states that net work done on a body equals:",
["Change in momentum", "Change in kinetic energy", "Change in potential energy", "Change in power"], 1],

["Work, Energy & Power",
"A body initially at rest is acted upon by a constant force. Its kinetic energy varies with time as:",
["t", "t²", "1/t", "constant"], 1],

["Work, Energy & Power",
"A 5 kg body falls freely through a height of 10 m. Taking g = 10 m/s², its loss of potential energy is:",
["50 J", "100 J", "500 J", "1000 J"], 2],

["Work, Energy & Power",
"Potential energy of a body of mass m at height h above ground is:",
["mg/h", "mgh", "½mgh", "mg²h"], 1],

["Work, Energy & Power",
"A body of mass 2 kg is raised to a height of 5 m. Taking g = 10 m/s², its potential energy is:",
["50 J", "100 J", "150 J", "200 J"], 1],

["Work, Energy & Power",
"Gravitational force is an example of:",
["Non-conservative force", "Conservative force", "Contact force only", "Variable force only"], 1],

["Work, Energy & Power",
"The work done by a conservative force around a closed path is:",
["Positive", "Negative", "Zero", "Infinite"], 2],

["Work, Energy & Power",
"Which of the following is a conservative force?",
["Friction", "Air resistance", "Gravitational force", "Viscous force"], 2],

["Work, Energy & Power",
"Mechanical energy is conserved when:",
["Only conservative forces do work", "Only friction acts", "External force always acts", "Velocity is zero"], 0],

["Work, Energy & Power",
"A spring of force constant k is compressed by x. Its elastic potential energy is:",
["kx", "kx²", "½kx²", "2kx²"], 2],

["Work, Energy & Power",
"A spring is stretched by 2 cm. If its extension is doubled, its stored energy becomes:",
["2 times", "4 times", "8 times", "Half"], 1],

["Work, Energy & Power",
"The force exerted by an ideal spring is:",
["F = kx", "F = -kx", "F = k/x", "F = x/k"], 1],

["Work, Energy & Power",
"A 10 kg body moving at 4 m/s has momentum:",
["20 kg m/s", "40 kg m/s", "80 kg m/s", "160 kg m/s"], 1],

["Work, Energy & Power",
"A body of mass 2 kg moving at 3 m/s is brought to rest. The work done by the retarding force is:",
["+9 J", "-9 J", "+18 J", "-18 J"], 1],

["Work, Energy & Power",
"A force of 100 N moves a body with velocity 2 m/s in the direction of force. Power is:",
["50 W", "100 W", "200 W", "400 W"], 2],

["Work, Energy & Power",
"The SI unit of power is:",
["Joule", "Newton", "Watt", "kWh"], 2],

["Work, Energy & Power",
"One horsepower is approximately:",
["246 W", "546 W", "746 W", "946 W"], 2],

["Work, Energy & Power",
"A machine does 6000 J of work in 30 s. Its power is:",
["100 W", "200 W", "300 W", "600 W"], 1],

["Work, Energy & Power",
"A force of 50 N acts on a body moving with speed 4 m/s at an angle of 60° to the velocity. Power is:",
["50 W", "100 W", "150 W", "200 W"], 1],

["Work, Energy & Power",
"The instantaneous power delivered by a force is:",
["F/v", "Fv", "F + v", "F - v"], 1],

["Work, Energy & Power",
"A 1000 kg car accelerates from 10 m/s to 20 m/s. The change in kinetic energy is:",
["50 kJ", "100 kJ", "150 kJ", "200 kJ"], 2],

["Work, Energy & Power",
"A particle moves in a circle with constant speed. The work done by centripetal force is:",
["Positive", "Negative", "Zero", "Maximum"], 2],

["Work, Energy & Power",
"Friction acting on a sliding body generally does:",
["Positive work", "Negative work", "Zero work always", "Infinite work"], 1],

["Work, Energy & Power",
"A block slides down a rough inclined plane. The work done by friction is:",
["Positive", "Negative", "Zero", "Cannot be defined"], 1],

["Work, Energy & Power",
"A block slides down a smooth inclined plane. The decrease in gravitational potential energy is converted into:",
["Heat only", "Kinetic energy", "Sound only", "Momentum"], 1],

["Work, Energy & Power",
"A ball is thrown vertically upward. At its highest point:",
["KE maximum, PE minimum", "KE zero, PE maximum", "Both KE and PE zero", "KE maximum, PE maximum"], 1],

["Work, Energy & Power",
"During free fall, neglecting air resistance:",
["KE decreases and PE decreases", "KE increases and PE decreases", "KE decreases and PE increases", "Both remain constant"], 1],

["Work, Energy & Power",
"A body is projected vertically upward with speed u. Its maximum height is:",
["u/g", "u²/g", "u²/2g", "2u²/g"], 2],

["Work, Energy & Power",
"A body is dropped from height h. Just before reaching the ground its speed is:",
["√(gh)", "√(2gh)", "2gh", "gh"], 1],

["Work, Energy & Power",
"If the mass of a body is doubled while its velocity remains unchanged, its kinetic energy:",
["Becomes half", "Remains same", "Doubles", "Becomes four times"], 2],

["Work, Energy & Power",
"If both mass and velocity of a body are doubled, its kinetic energy becomes:",
["2 times", "4 times", "6 times", "8 times"], 3],

["Work, Energy & Power",
"A 1 kg body moving at 10 m/s collides with a wall and rebounds at 10 m/s. The change in kinetic energy is:",
["100 J", "50 J", "Zero", "-100 J"], 2],

["Work, Energy & Power",
"A force-displacement graph is a horizontal line at F = 5 N from x = 0 to x = 4 m. Work done is:",
["1.25 J", "9 J", "20 J", "25 J"], 2],

["Work, Energy & Power",
"The area under a power-time graph represents:",
["Force", "Work done", "Momentum", "Acceleration"], 1],

["Work, Energy & Power",
"The area under a force-displacement graph represents:",
["Power", "Energy/work", "Velocity", "Acceleration"], 1],

["Work, Energy & Power",
"A motor lifts a 100 kg load vertically upward at constant speed 2 m/s. Taking g = 10 m/s², power required is:",
["500 W", "1000 W", "2000 W", "4000 W"], 2],

["Work, Energy & Power",
"A 60 W bulb operates for 5 hours. Energy consumed is:",
["0.03 kWh", "0.3 kWh", "3 kWh", "30 kWh"], 1],

["Work, Energy & Power",
"1 kWh is equal to:",
["3.6 × 10³ J", "3.6 × 10⁴ J", "3.6 × 10⁵ J", "3.6 × 10⁶ J"], 3],

["Work, Energy & Power",
"A machine has input power 1000 W and output power 800 W. Its efficiency is:",
["20%", "50%", "80%", "125%"], 2],

["Work, Energy & Power",
"A body moves with constant speed in a straight line under the action of several forces. The net work done over any displacement is:",
["Positive", "Negative", "Zero", "Infinite"], 2],

]


# =========================================================
# DATABASE
# =========================================================

def db():
    c = sqlite3.connect(DB_NAME)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    c = db()

    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            score INTEGER NOT NULL,
            correct INTEGER NOT NULL,
            wrong INTEGER NOT NULL,
            unattempted INTEGER NOT NULL,
            time_taken INTEGER NOT NULL,
            answers TEXT NOT NULL
        )
    """)

    c.commit()
    c.close()


init_db()


# =========================================================
# STUDENT TEST PAGE
# =========================================================

STUDENT_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NEET 2027 Physics - Work Energy Power</title>

<style>
body{
    margin:0;
    font-family:Arial,sans-serif;
    background:#eef2f7;
    color:#182033;
}

header{
    background:#173f7a;
    color:white;
    padding:18px 25px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:22px;
    font-weight:bold;
}

.timer{
    font-size:28px;
}

.container{
    max-width:1400px;
    margin:25px auto;
    padding:15px;
}

.card{
    background:white;
    border-radius:14px;
    padding:25px;
    box-shadow:0 3px 12px rgba(0,0,0,.08);
}

input[type=text]{
    width:100%;
    box-sizing:border-box;
    padding:14px;
    margin:8px 0 15px;
    border:1px solid #ccc;
    border-radius:8px;
    font-size:17px;
}

button{
    border:0;
    border-radius:8px;
    padding:13px 20px;
    font-size:16px;
    cursor:pointer;
}

.primary{
    background:#173f7a;
    color:white;
}

.warning{
    background:#f5c542;
}

.danger{
    background:#d9534f;
    color:white;
}

.grid{
    display:grid;
    grid-template-columns:1fr 330px;
    gap:20px;
}

.option{
    display:block;
    padding:16px;
    margin:12px 0;
    border:1px solid #ddd;
    border-radius:10px;
    cursor:pointer;
}

.option:hover{
    background:#f4f7fb;
}

.palette{
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:8px;
}

.pal{
    padding:12px 5px;
    background:#eee;
    text-align:center;
    border-radius:7px;
    cursor:pointer;
}

.pal.answered{
    background:#35a66f;
    color:white;
}

.pal.current{
    outline:3px solid #173f7a;
}

.pal.marked{
    background:#f5c542;
}

#exam{
    display:none;
}

.question{
    font-size:21px;
    line-height:1.5;
}

.topic{
    color:#555;
    font-weight:bold;
}

.controls{
    display:flex;
    gap:10px;
    margin-top:20px;
    flex-wrap:wrap;
}

@media(max-width:800px){
    .grid{
        grid-template-columns:1fr;
    }
}
</style>
</head>

<body>

<header>
<div>NEET 2027 PHYSICS • TEST 01</div>
<div class="timer" id="timer">60:00</div>
</header>

<div class="container">

<div id="intro" class="card">

<h1>Work, Energy & Power</h1>

<p><b>50 Questions • 60 Minutes • 200 Marks</b></p>

<p>Correct: +4 &nbsp;&nbsp; Wrong: −1 &nbsp;&nbsp; Unattempted: 0</p>

<label>Student Name</label>
<input id="name" type="text" placeholder="Enter your name">

<label>Roll Number</label>
<input id="roll" type="text" placeholder="Enter roll number">

<button class="primary" onclick="start()">Start Test</button>

</div>


<div id="exam">

<div class="grid">

<div class="card">

<div class="topic" id="topic"></div>

<h2 id="qno"></h2>

<div class="question" id="question"></div>

<div id="options"></div>

<div class="controls">
<button onclick="previous()">Previous</button>
<button class="warning" onclick="mark()">Mark for Review</button>
<button onclick="clearAnswer()">Clear</button>
<button class="primary" onclick="next()">Save & Next</button>
</div>

</div>


<div class="card">

<h2>Question Palette</h2>

<div class="palette" id="palette"></div>

<hr>

<button class="danger" onclick="submitTest()">Submit Test</button>

</div>

</div>

</div>

</div>


<script>

const Q = {{ questions|tojson }};

let i = 0;
let answers = Array(Q.length).fill(null);
let marked = Array(Q.length).fill(false);

let active = false;
let submitted = false;
let startTime = 0;
let remaining = 3600;


function start(){

    const name = document.getElementById("name").value.trim();
    const roll = document.getElementById("roll").value.trim();

    if(!name || !roll){
        alert("Please enter name and roll number.");
        return;
    }

    document.getElementById("intro").style.display="none";
    document.getElementById("exam").style.display="block";

    active = true;
    startTime = Date.now();

    render();
    palette();
    tick();
}


function render(){

    const q = Q[i];

    document.getElementById("topic").textContent = q[0];
    document.getElementById("qno").textContent =
        "Question " + (i+1) + " of " + Q.length;

    document.getElementById("question").textContent = q[1];

    let html="";

    q[2].forEach((x,j)=>{

        html += `
        <label class="option">
            <input
                type="radio"
                name="answer"
                ${answers[i]===j ? "checked" : ""}
                onchange="answers[i]=${j}; palette();"
            >
            ${String.fromCharCode(65+j)}. ${x}
        </label>
        `;

    });

    document.getElementById("options").innerHTML=html;

    palette();
}


function palette(){

    let html="";

    Q.forEach((_,j)=>{

        let cls="pal";

        if(answers[j]!==null) cls+=" answered";
        if(marked[j]) cls+=" marked";
        if(j===i) cls+=" current";

        html += `
        <div class="${cls}" onclick="go(${j})">
            ${j+1}
        </div>
        `;

    });

    document.getElementById("palette").innerHTML=html;
}


function go(n){

    i=n;
    render();

}


function next(){

    if(i < Q.length-1){
        i++;
        render();
    }else{
        alert("You are on the last question. You can submit the test.");
    }

}


function previous(){

    if(i>0){
        i--;
        render();
    }

}


function clearAnswer(){

    answers[i]=null;
    render();

}


function mark(){

    marked[i]=!marked[i];
    palette();

}


async function submitTest(){

    if(!active || submitted) return;

    if(!confirm("Submit test now?")) return;

    submitted=true;
    active=false;

    const elapsed = Math.floor((Date.now()-startTime)/1000);

    const payload={
        name:document.getElementById("name").value.trim(),
        roll:document.getElementById("roll").value.trim(),
        answers:answers,
        elapsed:elapsed
    };

    try{

        const res=await fetch("/submit",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(payload)
        });

        const data=await res.json();

        if(!res.ok){
            throw new Error(data.error || "Submission failed");
        }

        if(data.id){
            window.location.href="/response/"+data.id;
        }else{
            alert("Test submitted, but result could not be opened.");
        }

    }catch(err){

        submitted=false;
        active=true;

        alert("Submission error: " + err.message);

    }

}


function tick(){

    if(!active) return;

    remaining = Math.max(
        0,
        3600-Math.floor((Date.now()-startTime)/1000)
    );

    const min=String(Math.floor(remaining/60)).padStart(2,"0");
    const sec=String(remaining%60).padStart(2,"0");

    document.getElementById("timer").textContent=min+":"+sec;

    if(remaining<=0){
        submitTest();
        return;
    }

    setTimeout(tick,1000);
}

</script>

</body>
</html>
"""


# =========================================================
# RESPONSE SHEET
# =========================================================

RESPONSE_HTML = """
<!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Response Sheet</title>

<style>

body{
    margin:0;
    font-family:Arial;
    background:#eef2f7;
    color:#182033;
}

.container{
    max-width:1000px;
    margin:30px auto;
    padding:15px;
}

.card{
    background:white;
    padding:25px;
    margin-bottom:18px;
    border-radius:14px;
    box-shadow:0 3px 12px rgba(0,0,0,.08);
}

.correct{
    border-left:6px solid #35a66f;
}

.wrong{
    border-left:6px solid #d9534f;
}

.unattempted{
    border-left:6px solid #999;
}

button{
    padding:13px 20px;
    border:0;
    border-radius:8px;
    background:#173f7a;
    color:white;
    font-size:16px;
}

@media print{
    .no-print{
        display:none;
    }
}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>Test Submitted Successfully</h1>

<h2>NEET 2027 PHYSICS • TEST 01</h2>

<p><b>Student:</b> {{ row["name"] }}</p>

<p><b>Roll Number:</b> {{ row["roll"] }}</p>

<h2>Score: {{ row["score"] }}/200</h2>

<p>
Correct: {{ row["correct"] }}
|
Wrong: {{ row["wrong"] }}
|
Unattempted: {{ row["unattempted"] }}
</p>

</div>


{% for n,q in enumerate(questions) %}

{% set student = answers[n] %}
{% set correct = q[3] %}

<div class="card
{% if student is none %}
unattempted
{% elif student == correct %}
correct
{% else %}
wrong
{% endif %}
">

<h3>Question {{ n+1 }}</h3>

<p><b>{{ q[1] }}</b></p>

{% if student is none %}

<p>Your Answer: <b>Not Attempted</b></p>

{% elif student == correct %}

<p>Your Answer:
<b>{{ "ABCD"[student] }}. {{ q[2][student] }}</b>
✓ Correct
</p>

{% else %}

<p>Your Answer:
<b>{{ "ABCD"[student] }}. {{ q[2][student] }}</b>
✗ Wrong
</p>

<p>
Correct Answer:
<b>{{ "ABCD"[correct] }}. {{ q[2][correct] }}</b>
</p>

{% endif %}

</div>

{% endfor %}


<div class="card no-print">

<button onclick="window.print()">Download / Save as PDF</button>

</div>

</div>

</body>
</html>
"""


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template_string(
        STUDENT_HTML,
        questions=QUESTIONS
    )


# =========================================================
# SUBMIT
# =========================================================

@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json(force=True)

    name = str(data.get("name","")).strip()[:100]
    roll = str(data.get("roll","")).strip()[:50]
    answers = data.get("answers",[])
    elapsed = int(data.get("elapsed",0))

    if not name or not roll or not isinstance(answers,list):
        return jsonify({
            "error":"Name, roll number and answers are required."
        }),400

    answers = (answers + [None]*len(QUESTIONS))[:len(QUESTIONS)]

    correct = sum(
        1
        for a,q in zip(answers,QUESTIONS)
        if isinstance(a,int) and a == q[3]
    )

    wrong = sum(
        1
        for a,q in zip(answers,QUESTIONS)
        if a is not None and a != q[3]
    )

    unattempted = len(QUESTIONS) - correct - wrong

    score = correct*4 - wrong

    c = db()

    cur = c.execute("""
        INSERT INTO results
        (name,roll,score,correct,wrong,unattempted,time_taken,answers)
        VALUES (?,?,?,?,?,?,?,?)
    """,(
        name,
        roll,
        score,
        correct,
        wrong,
        unattempted,
        elapsed,
        json.dumps(answers)
    ))

    c.commit()

    # IMPORTANT:
    # lastrowid belongs to the CURSOR, not the CONNECTION.
    result_id = cur.lastrowid

    c.close()

    return jsonify({
        "id":result_id,
        "score":score,
        "correct":correct,
        "wrong":wrong,
        "unattempted":unattempted
    })


# =========================================================
# RESPONSE SHEET
# =========================================================

@app.route("/response/<int:result_id>")
def response_sheet(result_id):

    c = db()

    row = c.execute(
        "SELECT * FROM results WHERE id=?",
        (result_id,)
    ).fetchone()

    c.close()

    if not row:
        return "Response sheet not found",404

    answers = json.loads(row["answers"])

    return render_template_string(
        RESPONSE_HTML,
        row=row,
        answers=answers,
        questions=QUESTIONS,
        enumerate=enumerate
    )


# =========================================================
# TEACHER LOGIN
# =========================================================

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Teacher Login</title>
<style>
body{
    font-family:Arial;
    background:#eef2f7;
}
.card{
    max-width:400px;
    margin:80px auto;
    background:white;
    padding:30px;
    border-radius:14px;
}
input{
    width:100%;
    box-sizing:border-box;
    padding:14px;
    margin:10px 0;
}
button{
    padding:13px 20px;
    background:#173f7a;
    color:white;
    border:0;
    border-radius:8px;
}
</style>
</head>
<body>

<div class="card">

<h1>Teacher Login</h1>

<form method="POST">

<input
type="password"
name="password"
placeholder="Teacher password"
required
>

<button type="submit">Login</button>

</form>

{% if error %}
<p style="color:red">{{error}}</p>
{% endif %}

</div>

</body>
</html>
"""


@app.route("/teacher/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        password=request.form.get("password","")

        stored=os.environ.get("TEACHER_PASSWORD","teacher123")

        if password == stored:

            session["teacher"]=True

            return redirect(url_for("dashboard"))

        return render_template_string(
            LOGIN_HTML,
            error="Incorrect password."
        )

    return render_template_string(
        LOGIN_HTML,
        error=None
    )


# =========================================================
# TEACHER DASHBOARD
# =========================================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">

<title>Teacher Dashboard</title>

<style>

body{
    font-family:Arial;
    background:#eef2f7;
}

.container{
    max-width:1100px;
    margin:30px auto;
    padding:15px;
}

.card{
    background:white;
    padding:20px;
    margin-bottom:15px;
    border-radius:12px;
}

table{
    width:100%;
    border-collapse:collapse;
}

th,td{
    padding:12px;
    border-bottom:1px solid #ddd;
    text-align:left;
}

a{
    color:#173f7a;
}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>Teacher Dashboard</h1>

<h2>NEET 2027 PHYSICS • TEST 01</h2>

</div>

<div class="card">

<table>

<tr>
<th>Name</th>
<th>Roll</th>
<th>Score</th>
<th>Correct</th>
<th>Wrong</th>
<th>Unattempted</th>
<th>Response</th>
</tr>

{% for r in results %}

<tr>

<td>{{r["name"]}}</td>

<td>{{r["roll"]}}</td>

<td>{{r["score"]}}/200</td>

<td>{{r["correct"]}}</td>

<td>{{r["wrong"]}}</td>

<td>{{r["unattempted"]}}</td>

<td>
<a href="/response/{{r['id']}}" target="_blank">
View
</a>
</td>

</tr>

{% endfor %}

</table>

</div>

</div>

</body>
</html>
"""


@app.route("/teacher/dashboard")
def dashboard():

    if not session.get("teacher"):
        return redirect(url_for("login"))

    c=db()

    results=c.execute("""
        SELECT *
        FROM results
        ORDER BY id DESC
    """).fetchall()

    c.close()

    return render_template_string(
        DASHBOARD_HTML,
        results=results
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/teacher/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# RUN
# =========================================================

if __name__=="__main__":

    port=int(os.environ.get("PORT",5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
