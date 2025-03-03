uv venv --python 3.11  # Create virtual environment
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate  # Windows

uv pip install browser-use langchain_openai gspread playwright python-dotenv pypdf2
playwright install
