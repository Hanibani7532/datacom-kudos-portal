from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kudos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  team = db.Column(db.String(50), nullable=False)
  role = db.Column(db.String(20), default="employee")  # 'employee' or 'admin'


class Kudos(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  message = db.Column(db.String(500), nullable=False)
  category = db.Column(db.String(50), default="🌟 Great work")
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  is_visible = db.Column(db.Boolean, default=True)
  moderated_by = db.Column(db.Integer, nullable=True)
  moderated_at = db.Column(db.DateTime, nullable=True)
  reason_for_moderation = db.Column(db.String(200), nullable=True)

  sender = db.relationship("User", foreign_keys=[sender_id])
  recipient = db.relationship("User", foreign_keys=[recipient_id])


with app.app_context():
  db.create_all()
  if not User.query.first():
    u1 = User(name="Sarah Jenkins", team="Engineering", role="employee")
    u2 = User(name="James Smith", team="Product", role="employee")
    u3 = User(name="Admin User", team="Management", role="admin")
    db.session.add_all([u1, u2, u3])
    db.session.commit()


@app.route("/")
def index():
  filter_type = request.args.get("filter", "all")
  current_user_id = 1  # Simulating logged-in user Sarah Jenkins

  users = User.query.filter(User.id != current_user_id).all()
  current_user = User.query.get(current_user_id)

  query = Kudos.query.filter_by(is_visible=True)
  if filter_type == "received":
    query = query.filter_by(recipient_id=current_user_id)
  elif filter_type == "given":
    query = query.filter_by(sender_id=current_user_id)

  kudos_list = query.order_by(Kudos.created_at.desc()).all()

  # Stats calculation
  received_count = Kudos.query.filter_by(
      recipient_id=current_user_id, is_visible=True
  ).count()
  given_count = Kudos.query.filter_by(
      sender_id=current_user_id, is_visible=True
  ).count()
  total_week = Kudos.query.filter_by(is_visible=True).count()

  return render_template(
      "index.html",
      users=users,
      kudos=kudos_list,
      current_user=current_user,
      received_count=received_count,
      given_count=given_count,
      total_week=total_week,
      current_filter=filter_type,
  )


@app.route("/api/kudos", methods=["POST"])
def submit_kudos():
  data = request.form
  sender_id = int(data.get("sender_id", 1))
  recipient_id = int(data.get("recipient_id"))
  message = data.get("message", "").strip()
  category = data.get("category", "🌟 Great work")

  if not recipient_id or not message:
    return redirect(url_for("index"))
  if len(message) > 500:
    return redirect(url_for("index"))

  new_kudos = Kudos(
      sender_id=sender_id,
      recipient_id=recipient_id,
      message=message,
      category=category,
  )
  db.session.add(new_kudos)
  db.session.commit()
  return redirect(url_for("index"))


@app.route("/admin")
def admin_dashboard():
  all_kudos = Kudos.query.order_by(Kudos.created_at.desc()).all()
  return render_template("admin.html", kudos=all_kudos)


@app.route("/admin/moderate/<int:kudos_id>", methods=["POST"])
def moderate_kudos(kudos_id):
  k = Kudos.query.get_or_404(kudos_id)
  action = request.form.get("action")
  reason = request.form.get("reason", "Inappropriate content")

  if action == "toggle":
    k.is_visible = not k.is_visible
    k.moderated_by = 3
    k.moderated_at = datetime.utcnow()
    k.reason_for_moderation = reason if not k.is_visible else None
    db.session.commit()
  elif action == "delete":
    db.session.delete(k)
    db.session.commit()

  return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
  app.run(debug=True)