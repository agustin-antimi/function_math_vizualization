import os

# --- Base directory ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Directories ---
DIRS = {
    "pages": os.path.join(BASE_DIR, "pages"),
    "src": os.path.join(BASE_DIR, "src"),
    "test": os.path.join(BASE_DIR, "test"),
}

# --- Pages ---
PAGES = {
    "welcome": os.path.join(DIRS["pages"], "welcome_page.py"),
    "calculator": os.path.join(DIRS["pages"], "calculator_vizualizator.py"),
}

# --- Source modules ---
SRC = {
    "DerivateManager": os.path.join(DIRS["src"], "DerivateManager.py"),
    "functions": os.path.join(DIRS["src"], "functions.py"),
}

# --- Tests ---
TESTS = {
    "DerivateManager_test": os.path.join(DIRS["test"], "DerivateManager_test.ipynb"),
    "plots_manager": os.path.join(DIRS["test"], "plots_manager.ipynb"),
}

# --- Root files ---
ROOT_FILES = {
    "start": os.path.join(BASE_DIR, "start.py"),
    "config": os.path.join(BASE_DIR, "config.py"),
    "requirements": os.path.join(BASE_DIR, "requirements.txt"),
    "readme": os.path.join(BASE_DIR, "README.md"),
    "license": os.path.join(BASE_DIR, "LICENSE"),
    "gitignore": os.path.join(BASE_DIR, ".gitignore"),
}
