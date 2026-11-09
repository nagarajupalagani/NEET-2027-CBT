from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
import sqlite3
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DB_NAME = "results.db"
DURATION = 70


# =========================================================
# QUESTIONS
# =========================================================
QUESTIONS = [
    ["Gravitation", "What is the value of acceleration due to gravity at a height equal to half the radius of the Earth from its surface?",
     ["4.4 m/s^2", "6.5 m/s^2", "Zero", "9.8 m/s^2"], 0],

    ["Gravitation", "When a planet revolves around the Sun, in general, for the planet:",
     ["Linear momentum and linear velocity are constant.", "Linear momentum and areal velocity are constant.", "Kinetic and potential energy are constant.", "Angular momentum about the Sun and areal velocity are constant."], 3],

    ["Gravitation", "Electrical as well as gravitational effects can be thought to be caused by fields. Which statement is true for an electrical or gravitational field?",
     ["A gravitational or electric field does not exist in the space around an object.", "Fields are useful for understanding forces acting through a distance.", "There is no way to verify the existence of a force field since it is just a concept.", "The field concept is often used to describe contact forces."], 1],

    ["Gravitation", "Two bodies of mass 8 kg are placed at vertices A and B of an equilateral triangle ABC. A third body of mass 2 kg is placed at centroid G. If AG = BG = CG = 1 m, where should a fourth body of mass 4 kg be placed so that the resultant force on the 2 kg body is zero?",
     ["At C", "At a point P on line CG such that PG = 1/sqrt(2) m", "At a point P on line CG such that PG = 0.5 m", "At a point P on line CG such that PG = 2 m"], 1],

    ["Gravitation", "The value of acceleration due to gravity at a height of 10 km above Earth's surface is x. At what depth inside Earth will g have the same value x?",
     ["5 km", "20 km", "10 km", "15 km"], 1],

    ["Gravitation", "A satellite orbiting close to Earth has kinetic energy K. The minimum extra kinetic energy required for it to just overcome Earth's gravitational pull is:",
     ["K", "2K", "sqrt(3)K", "2sqrt(2)K"], 0],

    ["Gravitation", "A space station is at a height equal to Earth's radius. If v_E is the escape velocity at Earth's surface, the escape velocity at the space station is:",
     ["1/2 v_E", "1/4 v_E", "1/sqrt(2) v_E", "1/sqrt(3) v_E"], 2],

    ["Gravitation", "The value of acceleration due to gravity at a depth of 1600 km is:",
     ["4.9 m/s^2", "9.8 m/s^2", "7.35 m/s^2", "19.6 m/s^2"], 2],

    ["Gravitation", "A mass m on Earth's surface is shifted to a height equal to Earth's radius. If R is Earth's radius and M its mass, the work done is:",
     ["mgR/2", "mgR", "2mgR", "mgR/4"], 0],

    ["Gravitation", "An astronaut of mass m is on a satellite orbiting Earth at a height h above the surface. Earth's radius is R and mass is M. The gravitational pull F_G on the astronaut is:",
     ["Zero since the astronaut feels weightless", "0 < F_G < GMm/R^2", "GMm/(R+h)^2 < F_G < GMm/R^2", "F_G = GMm/(R+h)^2"], 3],

    ["Gravitation", "A body of mass m is taken from Earth's surface to a height equal to twice Earth's radius R_e. The increase in potential energy is (g is surface gravity):",
     ["(1/2)mgR_e", "(3/4)mgR_e", "(1/4)mgR_e", "(2/3)mgR_e"], 3],

    ["Gravitation", "Moving from a point 16 km below Earth's surface to a point 16 km above it, the approximate percentage change in g is (R_E = 6400 km):",
     ["0.12%", "0.25%", "0.50%", "0.75%"], 1],

    ["Gravitation", "At what height h, in terms of Earth's radius R, does acceleration due to gravity become g/9?",
     ["sqrt(3)R", "2sqrt(2)R", "2R", "4R"], 2],

    ["Gravitation", "A 1 kg body falls to Earth from infinity. Its speed and kinetic energy on reaching Earth's surface are (R = 6400 km, g = 9.8 m/s^2):",
     ["11.2 km/s; 6.27 x 10^7 J", "11.2 km/s; 12.54 x 10^7 J", "8.8 km/s; 6.27 x 10^7 J", "8.8 km/s; 12.54 x 10^7 J"], 0],

    ["Gravitation", "The escape velocity from spherical planet A is 10 km/s. Planet B has 10% of A's density and 10% of A's radius. The escape velocity from B is:",
     ["1000 m/s", "200sqrt(5) m/s", "1000sqrt(2) m/s", "100sqrt(10) m/s"], 3],

    ["Gravitation", "Earth has 8 times the mass and 2 times the radius of a planet. If Earth's escape velocity is 11.2 km/s, the planet's escape velocity is:",
     ["8.4 km/s", "11.2 km/s", "5.6 km/s", "2.8 km/s"], 2],

    ["Gravitation", "A satellite orbits Earth at a distance 9 times closer to Earth than the Moon. If the Moon's period is 27 days, the satellite's period is:",
     ["3 days", "27 days", "81 days", "1 day"], 3],

    ["Gravitation", "An astronaut takes a ball of mass m from Earth's surface and places it in a circular orbit at altitude 318.5 km. The change in total mechanical energy is x times (GMm/2R_E). Find x. (R_E = 6370 km.)",
     ["12", "11", "9", "10"], 1],

    ["Gravitation", "Two satellites A and B orbit a planet in circular orbits of radii 4R and R. If the speed of A is v, the speed of B is:",
     ["6v", "(3/4)v", "3v", "12v"], 0],

    ["Gravitation", "Assuming Earth has uniform density, a body weighs 300 N on its surface. Its weight at a depth R/4 is:",
     ["75 N", "375 N", "300 N", "225 N"], 3],

    ["Gravitation", "The kinetic energy required to project a body of mass m from Earth's surface to infinity is:",
     ["(1/2)mgR_E", "4mgR_E", "mgR_E", "2mgR_E"], 2],

    ["Gravitation", "A satellite revolving in a stationary orbit around a planet has period 6 hours. The planet's mass is one-fourth Earth's mass. If Earth's geostationary orbital radius is 4.2 x 10^4 km, the satellite's orbital radius is:",
     ["1.68 x 10^5 km", "1.4 x 10^4 km", "8.4 x 10^4 km", "1.05 x 10^4 km"], 3],

    ["Gravitation", "A 90 kg body placed at a distance 2R above Earth's surface experiences a gravitational pull (R is Earth's radius, g = 10 m/s^2):",
     ["300 N", "225 N", "100 N", "120 N"], 2],

    ["Gravitation", "A light planet revolves around a massive star in a circular orbit of radius R and period T. If the attractive force is proportional to R^(-3/2), then:",
     ["T^2 is proportional to R^(7/2)", "T^2 is proportional to R^3", "T^2 is proportional to R^(5/2)", "T^2 is proportional to R^(3/2)"], 2],

    ["Gravitation", "The mass of the Moon is 1/144 times the mass of a planet and its diameter is 1/16 times the planet's diameter. If the planet's escape velocity is v, the Moon's escape velocity is:",
     ["v/4", "v/6", "v/12", "v/3"], 3],

    ["Gravitation", "Earth's escape velocity is 11.2 km/s. A planet has one-third Earth's radius and one-sixth Earth's mass. Its escape velocity is:",
     ["7.9 km/s", "8.4 km/s", "4.2 km/s", "11.2 km/s"], 0],

    ["Gravitation", "At a point above Earth's surface, gravitational potential is -5.12 x 10^7 J/kg and g is 6.4 m/s^2. If Earth's mean radius is 6400 km, the height of the point is:",
     ["1600 km", "1200 km", "540 km", "1000 km"], 0],

    ["Gravitation", "A planet takes 200 days to complete one revolution around the Sun. If its orbital distance is reduced to one-fourth, its new period is:",
     ["20 days", "50 days", "100 days", "25 days"], 3],

    ["Gravitation", "If Earth's diameter is reduced to half its original value while its mass remains constant, the surface acceleration due to gravity becomes:",
     ["g/4", "2g", "g/2", "4g"], 3],

    ["Gravitation", "Two identical particles, each of mass m, move in a circle of radius a under their mutual gravitational attraction. The angular speed of each particle is:",
     ["sqrt(Gm/(2a^3))", "sqrt(Gm/a^3)", "sqrt(Gm/(8a^3))", "sqrt(Gm/(4a^3))"], 3],

    ["Gravitation", "A body is released from rest at a height equal to Earth's radius R above the surface. Its speed when it strikes Earth is:",
     ["sqrt(gR/2)", "sqrt(4gR)", "sqrt(2gR)", "sqrt(gR)"], 3],

    ["Gravitation", "Two planets A and B have radii R and 1.5R and densities rho and rho/2, respectively. The ratio of surface gravity g_B : g_A is:",
     ["2:1", "2:3", "4:3", "3:4"], 3],

    ["Gravitation", "A planet has mass 9M_E and radius 4R_E. If Earth's escape velocity is 11.2 km/s, the planet's escape velocity is:",
     ["33.6 km/s", "11.2 km/s", "16.8 km/s", "67.2 km/s"], 2],

    ["Gravitation", "A planet has 16 times Earth's mass and 4 times Earth's radius. The ratio of its escape velocity to Earth's escape velocity is:",
     ["1:4", "1:sqrt(2)", "4:1", "2:1"], 3],

    ["Gravitation", "Two satellites A and B move around Earth in the same orbit. The mass of A is twice the mass of B. Which quantity is the same for both?",
     ["Potential energy", "Kinetic energy", "Total energy", "Speed"], 3],

    ["Gravitation", "Planets A and B have radii R and 4R and densities rho and rho/3, respectively. The ratio of their surface accelerations g_A : g_B is:",
     ["3:16", "4:3", "1:16", "3:4"], 3],

    ["Gravitation", "The time period of a satellite revolving at a height equal to Earth's radius R above the surface is (g = 1 m/s^2):",
     ["sqrt(32 pi^2 R)", "sqrt(4 pi^2 R)", "sqrt(8 pi^2 R)", "sqrt(2 pi^2 R)"], 0],

    ["Gravitation", "Two satellites of masses m and 3m revolve around Earth in circular orbits of radii r and 3r, respectively. The ratio of their orbital speeds is:",
     ["3:1", "sqrt(3):1", "1:1", "9:1"], 1],

    ["Gravitation", "Assuming Earth has uniform density, a body's weight at depth d = R/2 is what if its surface weight is 200 N?",
     ["100 N", "400 N", "300 N", "500 N"], 0],

    ["Gravitation", "A body weighs 400 N on Earth's surface. Its weight at a depth equal to half Earth's radius is:",
     ["300 N", "200 N", "100 N", "Zero"], 1],

    ["Gravitation", "A body weighs 100 N on Earth's surface. Its gravitational force at a height equal to R/4 above the surface is:",
     ["50 N", "64 N", "25 N", "100 N"], 1],

    ["Gravitation", "Choose the incorrect statement:",
     ["The linear speed of a planet revolving around the Sun remains constant.", "When a body falls towards Earth, Earth's displacement towards the body is negligible.", "The speed of a satellite in a given circular orbit remains constant.", "For a planet revolving around the Sun in an elliptical orbit, its total energy remains constant."], 0],

    ["Gravitation", "A planet has twice Earth's mass and the same average density as Earth. An object weighing W on Earth will weigh on that planet:",
     ["2^(2/3) W", "W", "2W", "2^(1/3) W"], 3],

    ["Gravitation", "The escape velocities of planets A and B are in the ratio 1:2. Their radii are in the ratio 1:3. The ratio g_A : g_B is:",
     ["4:3", "2:3", "3:4", "3:2"], 2],

    ["Gravitation", "Earth has nine times the mass and twice the radius of planet P. If v_E is Earth's escape velocity, the escape velocity from P is v_E/sqrt(z). Find z.",
     ["1", "3", "2", "18"], 2],

    ["Gravitation", "A body of weight W is projected vertically upwards from Earth's surface to a height equal to nine times Earth's radius. Its weight at that height is:",
     ["W/9", "W/3", "W/100", "W/81"], 2],

    ["Gravitation", "At depth d below Earth's surface, g becomes four times its value at height 3R above the surface. If R = 6400 km, find d.",
     ["5260 km", "2560 km", "640 km", "4800 km"], 3],

    ["Gravitation", "An object falls from rest from a height R above Earth, where R is Earth's radius. Neglecting air resistance, its speed on reaching the surface is:",
     ["sqrt(gR/2)", "sqrt(gR)", "sqrt(2gR)", "2sqrt(gR)"], 1],

    ["Gravitation", "The gravitational field is E = -K/r^2. At r = 2 cm, gravitational potential is 10 J/kg. Find the potential at r = 3 cm, given K = 6 J cm/kg.",
     ["9 J/kg", "11 J/kg", "10 J/kg", "12 J/kg"], 1]
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
<title>NEET 2027 Physics - AIATS</title>

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
<div>NEET 2027 PHYSICS • TEST 04</div>
<div class="timer" id="timer">70:00</div>
</header>

<div class="container">

<div id="intro" class="card">

<h1>AIATS-01</h1>

<p><b>50 Questions • 70 Minutes • 200 Marks</b></p>

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
<img id="questionImage"
     alt="Question diagram"
     style="display:none; max-width:100%; max-height:460px; margin:16px 0;">
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
const questionImages = {
    0: "/static/q01_displacement.png",
    8: "/static/q09_acceleration_displacement_graph.png",
    19: "/static/q20_acceleration_time_graph.png",
    29: "/static/q30_velocity_position_graph.png",
    44: "/static/q45_acceleration_time_graph.png"
};

const img = document.getElementById("questionImage");

if (questionImages[i]) {
    img.src = questionImages[i];
    img.style.display = "block";
} else {
    img.removeAttribute("src");
    img.style.display = "none";
}
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

<h2>NEET 2027 PHYSICS • TEST 04</h2>

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

<h2>NEET 2027 PHYSICS • TEST 04</h2>

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
