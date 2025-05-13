# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- **Run application**: `python app.py` or `./run.sh`
- **Setup project**: `./init.sh --venv`
- **Install dependencies**: `pip install -r requirements.txt`
- **Docker setup**: `docker-compose up -d`
- **Test risk categorizer**: `python test_risk_categorizer.py`
- **Generate key**: `python generate_key.py`
- **Generate sample scan data**: `python utils/sample_generator.py -o test_scan.txt`

## Project Overview
This is a Flask-based web application that analyzes security scan outputs (Nmap, Nikto, SQLMap, Gobuster, etc.) and leverages AI (OpenAI API) to categorize vulnerabilities and provide exploitation guidance. The application has a modern cybersecurity-themed UI and focuses on helping penetration testers organize and analyze scan results.

## Core Components
- **app.py**: Main Flask application and routing
- **analyzer.py**: Handles scan parsing and AI-powered analysis
- **utils/risk_categorizer.py**: Vulnerability risk assessment algorithm
- **utils/sample_generator.py**: Creates sample scan outputs for testing
- **templates/**: HTML templates for the web interface
- **static/**: CSS, JavaScript, and assets
- **generate_key.py**: Utility to generate secure Flask session keys

## Architecture
The application follows a Flask-based MVC pattern:
1. User submits scan outputs via the web interface
2. The app processes the data through the analyzer
3. The analyzer uses OpenAI's API to enrich the data
4. Scan results are categorized using risk assessment rules
5. The UI presents findings in organized tabs by category

## Environment Variables
Setup in `.env` file:
- `OPENAI_API_KEY`: API key for OpenAI integration
- `SECRET_KEY`: Flask session security key
- `ENABLE_STREAMING`: Enable/disable streaming responses
- `AI_PROVIDER`: AI provider selection (openai or claude)

## Data Flow
1. Scan data input (file upload or text paste)
2. Parsing and extraction of key elements
3. OpenAI API analysis for enrichment
4. Risk categorization and assessment
5. Presentation in UI with categorized findings

## Testing Approach
Use the included test_risk_categorizer.py to test the risk classification algorithm and analyzer integration. This helps verify that vulnerabilities are correctly categorized by severity (critical, high, medium, low).

## Docker Configuration
The application can be containerized using the provided Dockerfile and docker-compose.yml. This creates an isolated environment with all dependencies and exposes the application on port 5000.

## Security Considerations
- API keys are stored in .env file (not in version control)
- User-uploaded scan files are stored in the uploads/ directory
- The application uses Flask's session handling for temporary data
- Keep OpenAI API key secure and don't expose it in logs/responses

## Common Operations
- Adding new scan types: Extend the analyzer.py module's parsing logic
- UI customization: Modify the templates/ and static/css files
- Adding new analysis categories: Update both analyzer.py and templates/results.html