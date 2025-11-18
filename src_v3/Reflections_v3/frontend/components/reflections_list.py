from fasthtml.common import *
from datetime import datetime
from .layout import PageLayout

# Import backend DB functions
from backend.api import db_get_all_reflections, db_get_all_users

async def render_reflections_page(user_id: str | None = None):
    """
    Renders the list of reflections, with the user filter dropdown.
    """
    
    # Get all users for the dropdown
    users = db_get_all_users()
    
    # Get all reflections
    all_reflections = db_get_all_reflections()
    
    # Filter reflections if a user_id is provided
    if user_id and user_id != "all":
        try:
            uid = int(user_id)
            filtered_reflections = [r for r in all_reflections if r['user_id'] == uid]
        except ValueError:
            filtered_reflections = all_reflections
    else:
        filtered_reflections = all_reflections
        
    filtered_reflections.reverse() # Show newest first

    # Create a simple lookup map to show user names
    user_map = {u.id: (u.firstname or u.email) for u in users}

    # --- Page Content ---
    
    # The Filter Form (using standard HTML form)
    filter_form = Form(
        Label("Filter by User:"),
        Br(),
        Select(
            Option("All Users", value="all", selected=(not user_id or user_id == "all")),
            *[Option(
                f"{u.firstname or u.email}", 
                value=u.id, 
                selected=(user_id and user_id == str(u.id))
              ) for u in users],
            name="user_id",
            id="user_id"
        ),
        Br(),
        Button("Filter", type="submit"),
        
        # Standard form submission
        action="/reflections",
        method="get"
    )

    # The List of Reflections
    # The List of Reflections
    reflection_list = Div(
        *[
            A(
                Div(
                    H3(r['title']),
                    Small(f"By {user_map.get(r['user_id'], 'Unknown')}, {r['timestamp'].strftime('%Y-%m-%d') if isinstance(r['timestamp'], datetime) else r['timestamp']}"),
                    Ul(*[Li(topic) for topic in r['topics']]),
                ),
                href=f"/reflections/{r['id']}" # Link to the detail page
            )
            for r in filtered_reflections
        ],
        id="reflection-list"
    )

    return PageLayout(
        "All Reflections",
        H1("All Reflections"),
        filter_form,
        Hr(),
        reflection_list
    )