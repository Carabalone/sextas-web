from flask import Blueprint, render_template, request
import sqlite3

query_bp = Blueprint('query_bp', __name__)

@query_bp.route("/query", methods=["GET", "POST"])
def query_sql():
    resultado = None
    erro = None
    query = ""
    colunas = []

    if request.method == "POST":
        query = request.form["query"]
        try:
            conn = sqlite3.connect("dados.db")
            cur = conn.cursor()
            cur.execute(query)

            if query.strip().lower().startswith("select"):
                resultado = cur.fetchall()
                colunas = [desc[0] for desc in cur.description] if cur.description else []
            else:
                conn.commit()
                resultado = f"Query executada com sucesso. {cur.rowcount} linha(s) afetada(s)."
                colunas = []
            conn.close()
        except Exception as e:
            erro = str(e)
            resultado = None
            colunas = []

    return render_template("query.html", query=query, resultado=resultado, erro=erro, colunas=colunas)