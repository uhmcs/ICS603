from fasthtml.common import *
from datetime import datetime
from starlette.responses import Response

from .layout import PageLayout

# Import backend DB functions
from backend.api import (
    db_get_all_users,
    db_classify_reflection,
    db_create_reflection,
    ClassifyReflectionInput,
    CreateReflectionInput
)

async def render_new_reflection_page():
    """
    Renders the initial form to add a new reflection.
    """
    users = db_get_all_users()
    
    # This form will now post to a single endpoint
    initial_form = Form(
        # This is the user dropdown you requested
        Label("Select User"),
        Br(),
        Select(
            *[Option(f"{u.firstname or u.email} (ID: {u.id})", value=u.id) for u in users],
            name="user_id",
            id="user_id"
        ),
        Br(), Br(),
        
        Label("Title"),
        Br(),
        Input(name="title", id="title", placeholder="Reflection Title"),
        Br(), Br(),
        
        Label("Text"),
        Br(),
        Textarea(name="text", id="text", placeholder="Write your reflection...", rows="10", cols="50"),
        Br(), Br(),
        
        Button("Submit Reflection", type="submit"),
        
        # Standard form submission
        action="/reflections/create",
        method="post"
    )
    
    return PageLayout(
        "Add New Reflection",
        H1("Add New Reflection"),
        initial_form
    )

async def handle_create_reflection(user_id: str, title: str, text: str):
    """
    Process:
    1. Classifies the reflection to get a list of topics.
    2. Creates ONE reflection, linking it to ALL topics.
    """
    
    # --- Step 1: Call Classifier ---
    classify_input = ClassifyReflectionInput(
        title=title,
        text=text,
        timestamp=datetime.now()
    )
    # Call the DB function directly
    classified_output = await db_classify_reflection(classify_input)
    topic_list = classified_output.topics # e.g., ["learning", "python"]

    # --- Step 2: Call Create Reflection ONCE ---
    reflection_input = CreateReflectionInput(
        title=title,
        text=text,
        timestamp=datetime.now(),
        topics=topic_list,  # <-- Pass the full list
        user_id=int(user_id) # Cast user_id to int
    )
        
    # Call the create function one time
    await db_create_reflection(reflection_input)