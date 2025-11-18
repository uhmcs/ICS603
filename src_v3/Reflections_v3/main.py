"""
Main application entry point.

This file imports the assembled app from the frontend package
and runs the server.

To run: python main.py
"""
import sys
import uvicorn

# Import the 'app' object defined in front-end/ui.py
# This app object already has all UI routes and the API mounted.
from frontend.ui import app

# This is now the one and only entry point
if __name__ == "__main__":
    try:
        print("Starting application server on http://localhost:8000")
        # use uvicorn.run() directly for more control
        uvicorn.run(app, host="localhost", port=8000)
    except Exception as e:
        print(f"❌ ERROR: Failed to start server: {e}")
        sys.exit(1)