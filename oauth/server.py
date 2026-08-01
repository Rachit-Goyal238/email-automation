import os
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, request, url_for
from authlib.integrations.flask_client import OAuth
from werkzeug.middleware.proxy_fix import ProxyFix
from oauth.token_store import get_token, save_token

load_dotenv()

app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "FLASK_SECRET_KEY is missing from .env"
    )

oauth = OAuth(app)

oauth.register(
    name="google",
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile https://www.googleapis.com/auth/gmail.compose"
    },
)


@app.route("/")
def home():
    return {
        "status": "running",
        "service": "OAuth Server"
    }


@app.route("/login")
def login():

    redirect_uri = url_for(
        "authorize",
        _external=True
    )

    return oauth.google.authorize_redirect(
        redirect_uri
    )


@app.route("/authorize")
def authorize():

    try:

        token = oauth.google.authorize_access_token()

        key = save_token(token)

        streamlit_url = os.getenv(
            "STREAMLIT_URL",
            "http://localhost:8501"
        )

        return redirect(
            f"{streamlit_url}/?token={key}"
        )

    except Exception as e:

        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500


@app.route("/token/<token_id>")
def token(token_id):

    token_data = get_token(token_id)

    if token_data is None:

        return jsonify(
            {
                "success": False,
                "message": "Invalid or expired token."
            }
        ), 404

    return jsonify(token_data)


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "OAUTH_PORT",
                5000
            )
        ),
        debug=True,
    )