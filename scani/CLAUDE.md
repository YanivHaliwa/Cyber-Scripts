# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Lint/Test Commands
- Run scanner: `python3 main.py`
- Run with UI update: `./run` (runs pyuic6 appui.ui -o appui.py and then main.py)
- Install dependencies: `pip install -r requirements.txt`
- Update UI from template: `pyuic6 appui.ui -o appui.py`

## Code Style Guidelines
- Imports: Group in order of stdlib, third-party (PyQt6, requests), then local modules
- Use snake_case for variables and functions
- Class names use PascalCase
- Error handling: Implement try/except blocks with specific exception types
- Threading: Use threading module for subprocess handling and parallel tasks
- UI components: Follow PyQt6 conventions with descriptive object names
- Config handling: Use JSON config files with defaults when file is missing
- Timeout handling: Implement proper process termination with signals
- Variable names: Descriptive names that indicate purpose and type
- Docstrings: Add function descriptions for complex methods
- Log format: Use consistent logging patterns for reporting status