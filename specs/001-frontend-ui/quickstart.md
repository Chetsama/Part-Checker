# Quickstart Guide: Computer Parts Pricing Web UI

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository if you haven't already:
   ```bash
   git clone <repository-url>
   cd PartChecker
   ```

2. Install required dependencies:
   ```bash
   pip install fastapi uvicorn jinja2 python-dotenv
   ```

3. Run the application in development mode:
   ```bash
   uvicorn main:app --reload
   ```
   
   The application will be available at `http://localhost:8000`

## How to Use

1. Navigate to the web interface at `http://localhost:8000`
2. Enter a list of computer parts in the input field (one part per line)
3. Click "Calculate Price" to process your request
4. View individual part prices and total cost on the results page

## Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── api/           # API endpoints
│   │   ├── services/      # Business logic 
│   │   └── models/        # Data models (Pydantic)
│   └── main.py            # Main FastAPI application
├── frontend/
│   ├── src/
│   │   ├── templates/     # Jinja2 HTML templates  
│   │   ├── static/        # CSS, JS, images
│   │   └── components/    # Reusable UI components (if needed)
│   └── tests/
└── partChecker.py         # Original CLI implementation (to be refactored into services)
```

## API Endpoints

The application provides the following RESTful endpoints:
- `POST /parts/submit` - Submit parts for pricing analysis
- `GET /parts/{request_id}/status` - Check processing status 
- `GET /parts/{request_id}/results` - Retrieve results
- `GET /parts/{part_name}/details` - Get detailed part information

## Configuration

Configuration is handled through environment variables. Create a `.env` file in the root directory:
```
API_HOST=localhost
API_PORT=8000
DEBUG=true
```

## Development

To contribute to this project:

1. Fork and clone the repository
2. Create a new feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## Support

For support, please open an issue on the GitHub repository or contact the maintainers.