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

["Newton's Laws of Motion",
"A body continues to remain in its state of rest or uniform motion in a straight line unless acted upon by an external force. This statement represents:",
["Newton's first law", "Newton's second law", "Newton's third law", "Law of gravitation"], 0],

["Newton's Laws of Motion",
"The inertia of a body depends on its:",
["Velocity", "Acceleration", "Mass", "Force"], 2],

["Newton's Laws of Motion",
"A passenger in a moving bus falls forward when the bus suddenly stops due to:",
["Inertia of rest", "Inertia of motion", "Inertia of direction", "Gravitational force"], 1],

["Newton's Laws of Motion",
"When a bus suddenly starts moving, a passenger tends to fall backward because of:",
["Inertia of rest", "Inertia of motion", "Inertia of direction", "Friction"], 0],

["Newton's Laws of Motion",
"Newton's second law of motion gives the relation between:",
["Mass and velocity", "Force and acceleration", "Work and energy", "Momentum and displacement"], 1],

["Newton's Laws of Motion",
"The SI unit of force is:",
["Joule", "Watt", "Newton", "Pascal"], 2],

["Newton's Laws of Motion",
"A force of 20 N acts on a body of mass 5 kg. Its acceleration is:",
["2 m/s²", "4 m/s²", "5 m/s²", "100 m/s²"], 1],

["Newton's Laws of Motion",
"If the net force acting on a body is zero, its acceleration is:",
["Zero", "Maximum", "Constant non-zero", "Infinite"], 0],

["Newton's Laws of Motion",
"A body of mass 10 kg is acted upon by a force of 50 N. Its acceleration is:",
["2 m/s²", "5 m/s²", "10 m/s²", "500 m/s²"], 1],

["Newton's Laws of Motion",
"The momentum of a body is defined as:",
["mv", "ma", "m/v", "v/m"], 0],

["Newton's Laws of Motion",
"The rate of change of momentum of a body is equal to:",
["Energy", "Power", "Force", "Work"], 2],

["Newton's Laws of Motion",
"If the momentum of a body is doubled while its mass remains constant, its velocity:",
["Becomes half", "Remains same", "Doubles", "Becomes four times"], 2],

["Newton's Laws of Motion",
"A force of 10 N acts on a body for 2 s. The impulse delivered is:",
["5 Ns", "10 Ns", "20 Ns", "40 Ns"], 2],

["Newton's Laws of Motion",
"Impulse is equal to:",
["Change in kinetic energy", "Change in momentum", "Change in velocity", "Rate of change of momentum"], 1],

["Newton's Laws of Motion",
"Newton's third law states that action and reaction:",
["Act on the same body", "Are equal and opposite and act on different bodies", "Are unequal", "Always cancel each other"], 1],

["Newton's Laws of Motion",
"A gun recoils when a bullet is fired because of:",
["Newton's first law", "Newton's second law", "Newton's third law", "Conservation of energy only"], 2],

["Newton's Laws of Motion",
"When a person walks on the ground, the force that actually propels the person forward is:",
["Weight", "Normal reaction", "Static friction", "Air resistance"], 2],

["Newton's Laws of Motion",
"A book is placed on a horizontal table. The normal reaction of the table acts:",
["Horizontally", "Vertically upward", "Vertically downward", "Along the surface"], 1],

["Newton's Laws of Motion",
"A block of mass m rests on a horizontal surface. Its normal reaction is:",
["mg", "m/g", "Zero", "mg/2"], 0],

["Newton's Laws of Motion",
"A body is pulled horizontally by a force F on a frictionless surface. Its acceleration is:",
["F/m", "mF", "F+m", "m/F"], 0],

["Newton's Laws of Motion",
"A 5 kg block is pulled by a horizontal force of 20 N on a smooth surface. Its acceleration is:",
["2 m/s²", "4 m/s²", "5 m/s²", "100 m/s²"], 1],

["Newton's Laws of Motion",
"Two forces of 10 N and 6 N act in the same direction on a body. The resultant force is:",
["4 N", "6 N", "16 N", "60 N"], 2],

["Newton's Laws of Motion",
"Two forces of 10 N and 6 N act in opposite directions on a body. The resultant force is:",
["4 N", "16 N", "60 N", "1.67 N"], 0],

["Newton's Laws of Motion",
"Two equal and opposite forces acting on the same body produce:",
["Maximum acceleration", "Zero net force", "Double acceleration", "Infinite acceleration"], 1],

["Newton's Laws of Motion",
"A block is moving with constant velocity on a horizontal surface. The net force on it is:",
["Zero", "Equal to its weight", "Equal to friction", "Maximum"], 0],

["Newton's Laws of Motion",
"The coefficient of friction is defined as the ratio of:",
["Friction to normal reaction", "Normal reaction to friction", "Mass to force", "Force to acceleration"], 0],

["Newton's Laws of Motion",
"The maximum value of static friction is called:",
["Kinetic friction", "Limiting friction", "Rolling friction", "Viscous force"], 1],

["Newton's Laws of Motion",
"Frictional force is generally:",
["Always independent of normal reaction", "Proportional to normal reaction", "Proportional to velocity always", "Independent of surfaces"], 1],

["Newton's Laws of Motion",
"A block of mass 10 kg is on a horizontal surface with coefficient of friction 0.2. Taking g = 10 m/s², limiting friction is:",
["2 N", "10 N", "20 N", "50 N"], 2],

["Newton's Laws of Motion",
"A block is moving on a rough horizontal surface. Kinetic friction acts:",
["In the direction of motion", "Opposite to relative motion", "Vertically upward", "Vertically downward"], 1],

["Newton's Laws of Motion",
"A block is placed on an inclined plane of angle θ. The component of its weight parallel to the plane is:",
["mg cosθ", "mg sinθ", "mg tanθ", "mg"], 1],

["Newton's Laws of Motion",
"For a block on a smooth inclined plane of angle θ, its acceleration down the plane is:",
["g", "g cosθ", "g sinθ", "g tanθ"], 2],

["Newton's Laws of Motion",
"For a block resting on a smooth inclined plane, the normal reaction is:",
["mg", "mg sinθ", "mg cosθ", "Zero"], 2],

["Newton's Laws of Motion",
"A block slides down a rough inclined plane. Friction acts:",
["Down the plane", "Up the plane", "Vertically downward", "Horizontally"], 1],

["Newton's Laws of Motion",
"A person standing in a lift experiences a normal reaction greater than their weight when the lift:",
["Moves upward with constant velocity", "Moves downward with constant velocity", "Accelerates upward", "Is at rest"], 2],

["Newton's Laws of Motion",
"A person of mass m stands in a lift accelerating upward with acceleration a. The apparent weight is:",
["mg", "m(g-a)", "m(g+a)", "ma"], 2],

["Newton's Laws of Motion",
"A person in a lift accelerating downward with acceleration a experiences apparent weight:",
["m(g+a)", "m(g-a)", "mg", "ma"], 1],

["Newton's Laws of Motion",
"When a lift is freely falling, the apparent weight of a person inside is:",
["mg", "2mg", "Zero", "mg/2"], 2],

["Newton's Laws of Motion",
"Two blocks of masses 2 kg and 3 kg are connected by a light string on a smooth horizontal surface and pulled by a 10 N force. Their common acceleration is:",
["1 m/s²", "2 m/s²", "5 m/s²", "10 m/s²"], 1],

["Newton's Laws of Motion",
"In an ideal Atwood machine, masses m and 2m are connected by a light inextensible string. The acceleration of the system is:",
["g/3", "g/2", "2g/3", "g"], 0],

["Newton's Laws of Motion",
"In an ideal Atwood machine, the tension in the string is:",
["Always zero", "Same throughout the string", "Different at every point", "Equal to the heavier weight"], 1],

["Newton's Laws of Motion",
"A body moving in a circle with constant speed has:",
["Zero acceleration", "Constant velocity", "Centripetal acceleration", "No force"], 2],

["Newton's Laws of Motion",
"The centripetal acceleration of a particle moving with speed v in a circle of radius r is:",
["vr", "v/r", "v²/r", "r/v²"], 2],

["Newton's Laws of Motion",
"The centripetal force required for circular motion is:",
["mv/r", "mv²/r", "mr/v²", "mv²r"], 1],

["Newton's Laws of Motion",
"A car moves on a level circular road. The centripetal force is provided by:",
["Weight", "Normal reaction", "Friction", "Engine power only"], 2],

["Newton's Laws of Motion",
"On a banked road, the horizontal component of normal reaction can provide:",
["Weight", "Centripetal force", "Friction only", "Gravitational potential energy"], 1],

["Newton's Laws of Motion",
"A force of 100 N acts on a body of mass 20 kg. If friction opposing motion is 20 N, acceleration is:",
["2 m/s²", "4 m/s²", "5 m/s²", "6 m/s²"], 0],

["Newton's Laws of Motion",
"A 2 kg block is acted upon by a net force of 6 N. Starting from rest, its velocity after 3 s is:",
["3 m/s", "6 m/s", "9 m/s", "12 m/s"], 2],

["Newton's Laws of Motion",
"A 4 kg body changes its velocity from 5 m/s to 10 m/s in 2 s. The net force acting on it is:",
["5 N", "10 N", "15 N", "20 N"], 1],

["Newton's Laws of Motion",
"A force acts on a body for a very short time and produces a large change in momentum. This is an example of:",
["Impulse", "Power", "Work", "Potential energy"], 0],

["Newton's Laws of Motion",
"Seat belts in cars are used mainly because of:",
["Newton's law of gravitation", "Inertia of motion", "Conservation of energy", "Buoyancy"], 1],

["Newton's Laws of Motion",
"While jumping from a boat to the shore, the boat moves backward due to:",
["Newton's first law", "Newton's second law", "Newton's third law", "Conservation of energy"], 2],

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
<title>NEET 2027 Physics - Newton's Laws of Motion</title>

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
<div>NEET 2027 PHYSICS • TEST 03</div>
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
