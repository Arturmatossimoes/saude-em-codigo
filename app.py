from flask import Flask, render_template, request, redirect, Response
import sqlite3
from dados_reais import dados_setores

app = Flask(__name__)

@app.route("/")
def dashboard():
    conn = sqlite3.connect("saude.db")
    db = conn.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS dados (horas INT, dor TEXT, estresse INT)")
    dados = db.execute("SELECT * FROM dados").fetchall()
    conn.close()

    total = len(dados)
    media_horas = sum([row[0] for row in dados]) / total if total > 0 else 0
    media_estresse = sum([row[2] for row in dados]) / total if total > 0 else 0
    frequencia_dor = sum([1 for row in dados if row[1] == "sim"]) / total * 100 if total > 0 else 0

    setores = [d["setor"] for d in dados_setores]
    burnout = [d["burnout"] for d in dados_setores]
    sintomas = [d["sintomas"] for d in dados_setores]

    return render_template("dashboard.html", horas=media_horas, estresse=media_estresse, dor=frequencia_dor,
                           setores=setores, burnout=burnout, sintomas=sintomas)

@app.route("/inserir", methods=["POST"])
def inserir():
    horas = int(request.form["horas"])
    dor = request.form["dor"]
    estresse = int(request.form["estresse"])

    conn = sqlite3.connect("saude.db")
    db = conn.cursor()
    db.execute("INSERT INTO dados VALUES (?, ?, ?)", (horas, dor, estresse))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/exportar")
def exportar_csv():
    conn = sqlite3.connect("saude.db")
    db = conn.cursor()
    dados = db.execute("SELECT horas, dor, estresse FROM dados").fetchall()
    conn.close()

    conteudo = "Horas,Dor Física,Estresse\n"
    for row in dados:
        conteudo += f"{row[0]},{row[1]},{row[2]}\n"

    return Response(
        conteudo,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=dados_usuarios.csv"}
    )

# ...código existente...
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
# ...código e
