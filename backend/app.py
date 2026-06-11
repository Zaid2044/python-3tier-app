from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://admin:admin@postgres:5432/inventory"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)


@app.route("/")
def home():
    return {"message": "Inventory API Running"}


@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {
            "status": "UP",
            "database": "CONNECTED"
        }
    except Exception as e:
        return {
            "status": "DOWN",
            "error": str(e)
        }, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)