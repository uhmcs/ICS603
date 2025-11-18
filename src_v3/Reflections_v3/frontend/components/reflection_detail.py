from fasthtml.common import *
from datetime import datetime
from .layout import PageLayout

# Import backend DB functions
from backend.api import db_get_reflection, db_get_user

async def render_reflection_detail_page(reflection_id: int):
    """
    Renders a single reflection by its ID.
    """
    
    # Call the DB functions directly
    try:
        reflection = db_get_reflection(reflection_id)
        user = db_get_user(reflection['user_id'])
        user_name = user.firstname or user.email
    except Exception:
        return PageLayout("Not Found", H1("Reflection not found."))

    return PageLayout(
        reflection['title'],
        H1(reflection['title']),
        # P(f"By {user_name} on {datetime.fromisoformat(reflection['timestamp']).strftime('%Y-%m-%d %H:%M')}"),
        P(f"By {user_name} on {reflection['timestamp'].strftime('%Y-%m-%d %H:%M')}"),
        H3("Topics:"),
        Ul(*[Li(topic) for topic in reflection['topics']]),
        
        Hr(),
        
        # Display the reflection text
        P(reflection['text'])
    )