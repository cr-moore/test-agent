# test-agent

An AI-powered testing agent that uses Claude to automate web testing and interaction. The agent intelligently navigates websites, performs actions, and validates test cases.

## Overview

**test-agent** is an autonomous testing framework powered by Anthropic's Claude AI. It reads test specifications and automatically executes them against websites, using browser automation and intelligent decision-making to complete testing scenarios.

## Features

- **AI-Driven Testing**: Uses Claude AI to understand and execute complex test cases
- **Browser Automation**: Powered by Playwright for reliable web interactions
- **Screenshot Capture**: Automatically captures screenshots for debugging and validation
- **Script Generation**: Generates test scripts dynamically based on requirements
- **Tool Integration**: Extensible tool system for adding custom capabilities
- **AWS Integration**: Built-in support for AWS services via boto3

## Architecture

```
src/
├── main.py           # Entry point - reads test file and runs the agent loop
├── agent_loop.py     # Core agent loop - handles AI-tool interactions with Claude
├── config/           # Configuration files
│   └── prompt.py     # System prompt for the AI agent
├── tools/            # Tool implementations
│   ├── base.py       # Base tool class
│   ├── browser.py    # Browser automation tool (Playwright)
│   ├── collection.py # Tool collection manager
│   └── script_writer.py  # Script generation tool
└── util/             # Utility functions
    └── read_test_file.py # Test file parser
```

## Prerequisites

- Python 3.x
- Anthropic API key
- Dependencies listed in `packages.txt`

## Installation

1. Install dependencies:
```bash
pip install -r packages.txt
```

2. Set your Anthropic API key (currently needs to be configured in `agent_loop.py`)

## Usage

1. Create a test file (`test.txt`) with the following structure:
```json
{
  "website": "https://example.com",
  "instructions": "Your test instructions here"
}
```

2. Run the agent:
```bash
python src/main.py
```

The agent will:
- Read your test specifications
- Launch a browser session
- Execute the test using AI-powered decision making
- Capture screenshots during execution
- Return a success/failure status

## Output

- **Console Output**: Test progress and AI decisions
- **Screenshots**: Saved to `screenshots/` directory for debugging
- **Generated Scripts**: Saved to `scripts/output/` directory

## Dependencies

- `anthropic` - Claude API client
- `playwright` - Browser automation
- `jsonschema` - Schema validation
- `boto3` - AWS services integration

## How It Works

1. **Test Reading**: Loads test specifications from `test.txt`
2. **Agent Loop**: 
   - Sends test case to Claude with browser and script-writing tools
   - Claude analyzes the request and decides which tools to use
   - Browser tool captures pages and executes actions
   - Script writer generates test code as needed
   - Loop continues until test completes
3. **Result Evaluation**: Final message is checked for success indicator
4. **Cleanup**: Browser session is closed and resources are released

## Configuration

Edit `src/config/prompt.py` to customize the system prompt that guides the AI's behavior.

## Status Indicators

- ✓ **Success**: Test passes (output contains "success")
- ✗ **Failure**: Test fails (output does not contain "success")
