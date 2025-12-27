# Part Checker

A command-line tool for checking and managing parts inventory.

## Setup

Create and activate a virtual environment:
```bash
python3 -m venv PartChecker
source PartChecker/bin/activate
```

## Usage

List available parts:
```bash
python3 partChecker.py --list
```

## Features

- Check part availability
- Manage inventory
- Search for specific parts
- Generate reports

## Requirements

- Python 3.x
- Virtual environment setup (as shown above)

## Web UI Features

This project now includes a web-based user interface built with:
- FastAPI backend framework 
- Jinja2 templating engine
- Vanilla HTML/CSS/JS frontend

The new web UI allows users to:
1. Enter lists of computer parts through a web form
2. Receive accurate pricing for each part individually (not just the most expensive)
3. View detailed information about each component including price variations and sources
4. Handle invalid input gracefully with helpful error messages

To run the web application:
```bash
cd backend/src/
python3 main.py
```

The application will be available at http://localhost:8000