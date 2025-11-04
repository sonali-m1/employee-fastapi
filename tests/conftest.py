import sys # access to pythons runtime environment including module search path (sys.path)
from pathlib import Path # object oriented way to handle paths

""" 
- ROOT holds absolute path to project root (where main lives) 
- __file__ refers to this file config tests
- resolve() converts to absolute path
- parent.parent moves us two levels up to the project root
"""
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT)) # addds project root to beginning of pythons module search path

import pytest
from fastapi.testclient import TestClient
from main import app

# defines reusable test fixture that lasts the entire testing session
@pytest.fixture(scope="session")
def client():
    return TestClient(app)