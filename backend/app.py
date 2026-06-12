"""
app.py - Flask Application Entry Point

This is the main entry point for the Inventory Management System backend.
It initializes the Flask app, database, CORS, and registers API routes.
"""

import time
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routes import products_bp
from prometheus_client import Counter, generate_latest
from flask import Response

REQUESTS = Counter(
    "app_requests_total",
    "Total application requests"
)

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype="text/plain"
    )
# ─── Logging Setup ────────────────────────────────────────────────────────────
# Structured logging so we can see what's happening in production containers.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── Track App Start Time (for uptime metric) ─────────────────────────────────
APP_START_TIME = time.time()


def create_app():
    """
    Application Factory Pattern.
    Creates and configures the Flask app.
    Returns the configured app instance.
    """
    app = Flask(__name__)

    # Load config from config.py (reads environment variables)
    app.config.from_object(Config)

    # Enable Cross-Origin Resource Sharing so the frontend can call this API
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize SQLAlchemy with this app instance
    db.init_app(app)

    # Register the products API blueprint (all /api/products routes)
    app.register_blueprint(products_bp)

    # ─── Health Check Endpoint ─────────────────────────────────────────────
    @app.route("/health")
    def health():
        """
        Simple health check endpoint.
        Used by Docker health checks and load balancers.
        Returns 200 OK if the app is running.
        """
        return jsonify({"status": "healthy"}), 200

    # ─── Metrics Endpoint ──────────────────────────────────────────────────
    @app.route("/metrics")
    def metrics():
        """
        Returns basic application metrics:
        - Total product count
        - Database connection status
        - Application uptime in seconds
        """
        from models import Product

        # Check database health
        db_status = "connected"
        total_products = 0
        try:
            total_products = Product.query.count()
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            db_status = "disconnected"

        uptime_seconds = round(time.time() - APP_START_TIME, 2)

        return jsonify({
            "success": True,
            "data": {
                "total_products": total_products,
                "database_status": db_status,
                "uptime_seconds": uptime_seconds,
            }
        }), 200

    # ─── Auto-create Tables ────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        logger.info("Database tables verified/created successfully.")

    logger.info("Flask application initialized successfully.")
    return app


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=Config.DEBUG
    )
