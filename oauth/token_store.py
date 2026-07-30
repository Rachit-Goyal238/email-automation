import threading
import time
import uuid

# Token lifetime (seconds)
TOKEN_TTL = 300  # 5 minutes

_lock = threading.Lock()
_tokens = {}


def _cleanup():
    """Remove expired tokens."""
    now = time.time()

    expired = [
        key
        for key, value in _tokens.items()
        if now - value["created_at"] > TOKEN_TTL
    ]

    for key in expired:
        _tokens.pop(key, None)


def save_token(token):
    """
    Save an OAuth token temporarily.

    Returns:
        UUID string used by Streamlit to retrieve it.
    """

    with _lock:
        _cleanup()

        key = str(uuid.uuid4())

        _tokens[key] = {
            "token": token,
            "created_at": time.time()
        }

        return key


def get_token(key):
    """
    Retrieve the token once.

    Token expires automatically or is removed after first use.
    """

    with _lock:
        _cleanup()

        data = _tokens.pop(key, None)

        if data is None:
            return None

        return data["token"]