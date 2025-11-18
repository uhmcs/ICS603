from fasthtml.common import *
from starlette.responses import RedirectResponse

# --- Import from your backend ---
from backend.api import app as api_app

# --- Import your new page components ---
from .components.layout import PageLayout
from .components.reflections_list import render_reflections_page
from .components.reflection_detail import render_reflection_detail_page
from .components.reflection_form import (
    render_new_reflection_page,
    handle_create_reflection
)

# Initialize your main FastHTML app
app = FastHTML()

# Mount your FastAPI app at the /api path
# All routes from backend/api.py will now be served under /api
app.mount("/api", api_app)


# --- Main Page Routes ---

@app.get("/")
def home():
    # Redirect the root URL to the main reflections list
    return RedirectResponse(url="/reflections", status_code=302)

@app.get("/reflections")
async def reflections_list_page(user_id: str = None):
    """
    Tab 2: Show reflections.
    (With user filter dropdown)
    """
    return await render_reflections_page(user_id)

@app.get("/reflections/new")
async def new_reflection_page():
    """
    Tab 1: Form to enter new reflections.
    """
    return await render_new_reflection_page()

@app.get("/reflections/{reflection_id}")
async def reflection_detail_page(reflection_id: int):
    """
    Show a single reflection when clicked.
    """
    return await render_reflection_detail_page(reflection_id)
    
# --- Form Handling Routes ---

@app.post("/reflections/create")
async def create_reflection_handler(user_id: str, title: str, text: str):
    """
    Handles the ENTIRE creation process:
    1. Classifies reflection
    2. Creates reflection (and any new topics)
    3. Redirects to the reflection list
    """
    await handle_create_reflection(user_id, title, text)
    return RedirectResponse(url="/reflections", status_code=303)