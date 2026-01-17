from typing import Callable, Optional, Any

Base = None
JSONField = None
get_db = None
get_db_context = None
ScopedSession = None


def configure_db(
    base,
    json_field,
    get_db_fn: Callable,
    get_db_context_fn: Callable,
    scoped_session: Optional[Any] = None,
):
    global Base, JSONField, get_db, get_db_context, ScopedSession
    Base = base
    JSONField = json_field
    get_db = get_db_fn
    get_db_context = get_db_context_fn
    ScopedSession = scoped_session


def get_scoped_session():
    if ScopedSession is None:
        raise RuntimeError("RAG DB not configured with ScopedSession")
    return ScopedSession
