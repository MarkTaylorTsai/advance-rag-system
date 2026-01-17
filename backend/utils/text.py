import hashlib


def calculate_sha256_string(string: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(string.encode("utf-8"))
    return sha256_hash.hexdigest()


def sanitize_text_for_db(text: str) -> str:
    """Remove null bytes and invalid UTF-8 surrogates from text for PostgreSQL storage."""
    if not isinstance(text, str):
        return text
    text = text.replace("\x00", "").replace("\u0000", "")
    try:
        text = text.encode("utf-8", errors="surrogatepass").decode(
            "utf-8", errors="ignore"
        )
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return text


def sanitize_data_for_db(obj):
    """Recursively sanitize all strings in a data structure for database storage."""
    if isinstance(obj, str):
        return sanitize_text_for_db(obj)
    if isinstance(obj, dict):
        return {k: sanitize_data_for_db(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_data_for_db(v) for v in obj]
    return obj
