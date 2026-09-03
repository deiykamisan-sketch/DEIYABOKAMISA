"""User profile and preference services."""

def display_name(user):
    return user.get_full_name().strip() or user.username
