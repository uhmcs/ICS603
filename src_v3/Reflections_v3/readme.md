Reflection App

This is a single-process, full-stack web application built with FastHTML (front-end) and FastAPI (back-end). It allows users to write personal reflections, which are then automatically classified into topics using an AI model.

The application runs as a single monolith, with the FastHTML front-end importing and mounting the FastAPI back-end. This allows the front-end to call back-end functions directly in Python for maximum performance (zero network latency) while still exposing a fully functional JSON API.

Tech Stack

Front-End: FastHTML

Back-End: FastAPI

Database: SQLAlchemy with PostgreSQL (via Supabase)

AI Classification: PydanticAI (using gpt-4o-mini)

Server: Uvicorn

Features

User Management: Add and list users.

Reflection Management:

Create new reflections.

View all reflections.

View a single reflection by ID.

AI Topic Classification: When a new reflection is submitted, it is automatically sent to an AI agent to generate a list of relevant topics.

User Filtering: The main reflections list can be filtered by user. 

Many-to-Many Relationships:

Each reflection is linked to one user.

Each reflection is linked to multiple topics via the reflection_topics table.

Project Structure

Reflections  
├── backend/  
│   ├── api.py               # Defines the FastAPI app and all API endpoints  
│   ├── classifier.py        # AI topic classification logic  
│   ├── create_db.py         # Script to initialize database tables  
│   ├── models.py            # SQLAlchemy database models (User, Reflection, Topic)  
│   └── __init__.py  
├── frontend/  
│   ├── components/          # Holds individual page components  
│   │   ├── layout.py  
│   │   ├── reflection_detail.py  
│   │   ├── reflection_form.py  
│   │   └── reflection_list.py  
│   ├── ui.py               # Defines all front-end UI routes and mounts the API  
│   └── __init__.py  
├── main.py                 # The main entry point to run the application  
└── .env.example            # Example environment variables  


Setup & Installation  

1. Clone the Repository  

git clone <your-repo-url>
cd <your-repo-name>


2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate


3. Install Dependencies

You will need to create a requirements.txt file with the following content:

requirements.txt

fastapi
fasthtml
uvicorn[standard]
sqlalchemy
psycopg2-binary
python-dotenv
pydantic-ai


Then, install the requirements:

pip install -r requirements.txt


4. Set Up Environment Variables

Create a .env file in the root directory. Copy the contents of .env.example (or create it) and fill in your details.

.env

# Your PostgreSQL Session Pooler connection string  
# SUPABASE_DB_URL="postgresql://user:password@host:port/dbname"  
user=[YOUR_USER_NAME]   
password=[Your_Password]  
host=aws-1-us-west-1.pooler.supabase.com   
port=5432   
dbname=postgres  

# Your OpenAI API Key for the classifier  
OPENAI_API_KEY="sk-..."  


5. Initialize the Database

Run the create_db.py script from the root folder to create all the necessary tables (users, topics, reflections, reflection_topics) and seed the initial topics.

python backend/create_db.py


You only need to do this once.

How to Run the App

From the root folder (src_v3/Reflections_v4/), run the main application:

python main.py


The server will start. You can access the application at:

Front-End: http://localhost:8000/reflections

API Docs: http://localhost:8000/api/docs

Using the API

The application also exposes a full JSON API, which is mounted at the /api path.

User Endpoints

POST /api/users: Create a new user.

GET /api/users: Get a list of all users.

GET /api/users/{user_id}: Get a specific user.

Reflection Endpoints

POST /api/reflections: Create a new reflection.

GET /api/reflections: Get all reflections.

GET /api/reflections/{reflection_id}: Get a specific reflection.

POST /api/reflections/classify: Classify text to get topics.

Topic Endpoints

POST /api/topics: Create new topics.

GET /api/topics: Get all topics.
