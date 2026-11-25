from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "campusfind-demo-secret"
DB = Path(__file__).with_name("campusfind.db")

CATEGORIES = ["ID Card", "Books & Notes", "Electronics", "Wallet / Keys", "Clothing", "Bags", "Other"]

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL CHECK(kind IN ('Lost','Found')),
            title TEXT NOT NULL, category TEXT NOT NULL,
            description TEXT NOT NULL, location TEXT NOT NULL,
            date TEXT NOT NULL, reporter TEXT NOT NULL,
            contact TEXT NOT NULL, status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        con.execute("""CREATE TABLE IF NOT EXISTS claims (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL, claimant TEXT NOT NULL,
            contact TEXT NOT NULL, details TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(item_id) REFERENCES items(id)
        )""")

@app.route("/")
def home():
    with db() as con:
        lost = con.execute("SELECT COUNT(*) FROM items WHERE kind='Lost' AND status='Open'").fetchone()[0]
        found = con.execute("SELECT COUNT(*) FROM items WHERE kind='Found' AND status='Open'").fetchone()[0]
        recent = con.execute("SELECT * FROM items ORDER BY id DESC LIMIT 6").fetchall()
    return render_template("index.html", lost=lost, found=found, recent=recent)

@app.route("/items")
def items():
    q = request.args.get("q", "").strip()
    kind = request.args.get("kind", "").strip()
    category = request.args.get("category", "").strip()
    sql = "SELECT * FROM items WHERE status='Open'"
    params = []
    if kind in ("Lost", "Found"):
        sql += " AND kind=?"; params.append(kind)
    if category:
        sql += " AND category=?"; params.append(category)
    if q:
        sql += " AND (title LIKE ? OR description LIKE ? OR location LIKE ?)"
        params.extend([f"%{q}%"] * 3)
    sql += " ORDER BY id DESC"
    with db() as con:
        rows = con.execute(sql, params).fetchall()
    return render_template("items.html", items=rows, q=q, kind=kind, category=category, categories=CATEGORIES)

@app.route("/report", methods=["GET","POST"])
def report():
    kind = request.args.get("kind", "Lost")
    if kind not in ("Lost","Found"): kind = "Lost"
    if request.method == "POST":
        data = [request.form.get(k,"").strip() for k in
                ("kind","title","category","description","location","date","reporter","contact")]
        if not all(data):
            flash("Please fill in all required fields.")
            return redirect(url_for("report", kind=kind))
        if data[0] not in ("Lost","Found"):
            data[0] = kind
        with db() as con:
            con.execute("""INSERT INTO items(kind,title,category,description,location,date,reporter,contact)
                          VALUES(?,?,?,?,?,?,?,?)""", data)
        flash("Your report has been published.")
        return redirect(url_for("items"))
    return render_template("report.html", kind=kind, categories=CATEGORIES)

@app.route("/item/<int:item_id>")
def item_detail(item_id):
    with db() as con:
        item = con.execute("SELECT * FROM items WHERE id=?", (item_id,)).fetchone()
    if not item:
        flash("Item report not found.")
        return redirect(url_for("items"))
    return render_template("detail.html", item=item)

@app.route("/claim/<int:item_id>", methods=["POST"])
def claim(item_id):
    data = [request.form.get(k,"").strip() for k in ("claimant","contact","details")]
    if not all(data):
        flash("Please complete the claim form.")
        return redirect(url_for("item_detail", item_id=item_id))
    with db() as con:
        exists = con.execute("SELECT id FROM items WHERE id=? AND status='Open'", (item_id,)).fetchone()
        if not exists:
            flash("This item is no longer open for claims.")
            return redirect(url_for("items"))
        con.execute("INSERT INTO claims(item_id,claimant,contact,details) VALUES(?,?,?,?)", [item_id]+data)
    flash("Claim request submitted. The reporter can contact you using the details provided.")
    return redirect(url_for("item_detail", item_id=item_id))

@app.route("/admin")
def admin():
    with db() as con:
        all_items = con.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
        claims = con.execute("""SELECT claims.*, items.title AS item_title
                                FROM claims JOIN items ON items.id=claims.item_id
                                ORDER BY claims.id DESC""").fetchall()
    return render_template("admin.html", items=all_items, claims=claims)

@app.route("/resolve/<int:item_id>", methods=["POST"])
def resolve(item_id):
    with db() as con:
        con.execute("UPDATE items SET status='Resolved' WHERE id=?", (item_id,))
    flash("Item marked as resolved.")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
