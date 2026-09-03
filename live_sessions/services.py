"""Live-room lifecycle and participant-control boundary."""

def can_control_session(user, session):
    return user.is_authenticated and session.lecture.owner_id == user.id
