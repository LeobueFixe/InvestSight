from fastapi import Request, HTTPException
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User


def get_current_user(request: Request) -> User:
    session_key = request.cookies.get("sessionid")
    if not session_key:
        raise HTTPException(status_code=401, detail="Not authenticated")
    session = SessionStore(session_key=session_key)
    user_id = session.get("_auth_user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found")
