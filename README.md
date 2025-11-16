# test-agent

An AI-powered testing agent that uses Claude to automate web testing and interaction. The agent intelligently navigates websites, performs actions, and validates test cases.

## Overview

**test-agent** is an autonomous testing framework powered by Anthropic's Claude AI. It supports two distinct workflows:
1. **Test Plan Generation**: Analyze websites and create detailed step-by-step test plans
2. **Test Script Generation**: Execute test cases and generate automated Playwright scripts

The agent uses browser automation and intelligent decision-making to complete testing scenarios, with outputs organized by type (plans vs scripts).

## Features

- **Dual-Mode Testing**: Generate test plans OR execute test scripts based on user selection
- **AI-Driven Analysis**: Uses Claude AI to understand and execute complex test cases
- **Browser Automation**: Powered by Playwright for reliable web interactions
- **Screenshot Capture**: Automatically captures screenshots for debugging and validation
- **Smart Output Organization**: Plans saved to `plans/` directory, scripts to `scripts/`
- **Tool Integration**: Extensible tool system for adding custom capabilities
- **AWS Integration**: Built-in support for AWS services via boto3
- **Secure API Key Management**: Uses environment variables for sensitive credentials

## Project Structure

```
src/
├── main.py              # Entry point - menu-driven interface
├── loops/
│   └── agent_loop.py    # Core agent loop - handles AI-tool interactions
├── config/
│   ├── plan_prompt.py   # System prompt for test plan generation
│   └── script_prompt.py # System prompt for test script generation
├── tools/
│   ├── base.py          # Base tool class
│   ├── browser.py       # Browser automation (Playwright)
│   ├── collection.py    # Tool collection manager
│   └── script_writer.py # File writing tool
└── util/
    └── read_test_file.py # Test case file parser

plans/                  # Generated test plan files
scripts/                # Generated test scripts
screenshots/            # Captured screenshots during execution
```

## Prerequisites

- Python 3.x
- Anthropic API key (set as `ANTHROPIC_API_KEY` environment variable. Must retrieve key from Claude CLI)
- Dependencies listed in `packages.txt`

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r packages.txt
```

4. Set your Anthropic API key as an environment variable:
```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "your-api-key-here"

# Windows (cmd)
set ANTHROPIC_API_KEY=your-api-key-here

# macOS/Linux
export ANTHROPIC_API_KEY=your-api-key-here
```

## Usage

### Running the Agent

From the `src/` directory, run:
```bash
python main.py
```

This displays a menu with two options:

```
==================================================
Test Agent Menu
==================================================
1) Generate Test Plan
2) Generate Test Script
==================================================

Select an option (1 or 2): 
```

### Option 1: Generate Test Plan

- Reads test specifications from `../plan.txt`
- Uses the plan generation prompt to analyze the website
- Takes screenshots and documents a step-by-step testing plan
- Saves output to `plans/` directory
- Returns success/failure status

### Option 2: Generate Test Script

- Reads test specifications from `../test.txt`
- Uses the script generation prompt to execute the test
- Takes screenshots only when necessary to verify state changes
- Generates a Playwright Python script
- Saves output to `scripts/` directory
- Returns success/failure status

## Test File Format

Both `plan.txt` and `test.txt` should follow this text format:

```
Website - https://example.com

Instructions (Write plan instructions below):
Your test instructions or feature to test here
```

Example:
```
Website - https://youtube.com

Instructions (Write test instructions below):
You are on youtube.com website.
Search for 'lofi music' in the search bar.
Verify search results appear.
```

## How It Works

### Agent Loop Flow

1. **Plan/Test Reading**: Loads test or plan specifications from the appropriate file
2. **Browser Launch**: Starts a Playwright browser session
3. **Agent Loop**: 
   - Sends test case to Claude with available tools
   - Claude analyzes the request and decides which tools to use
   - Browser tool captures pages and executes actions
   - Script writer tool generates test code
   - Loop continues until test completes
4. **Result Evaluation**: Final message is checked for success indicator ("success")
5. **Cleanup**: Browser session is closed and resources are released

### Output Routing

- **Plans**: Saved to `plans/` directory
- **Scripts**: Saved to `scripts/` directory
- **Screenshots**: Saved to `screenshots/` directory during execution

## Configuration

### System Prompts

Edit the prompt files to customize the agent's behavior:
- `src/config/plan_prompt.py` - Controls test plan generation strategy
- `src/config/script_prompt.py` - Controls test script execution strategy

### API Configuration

The agent uses Claude Sonnet 4.5 by default. This can be modified in `src/loops/agent_loop.py`:
```python
MODEL = "claude-sonnet-4-5-20250929"
```

## Dependencies

- `anthropic` - Claude API client
- `playwright` - Browser automation
- `jsonschema` - Schema validation
- `boto3` - AWS services integration

## Status Indicators

- **Success**: Test passes (output contains "success")
- **Failure**: Test fails (output does not contain "success")

## Potential Improvements

### Test Plan Prompt Optimization

The plan generation prompt could be tweaked in the future to allow the LLM to execute faster. Currently, the plan prompt is comprehensive and thorough, but future iterations could:
- Reduce the level of detail captured per step
- Streamline the analysis phase to reduce API tokens
- Implement more efficient screenshot capture strategies
- Add caching mechanisms for repeated test scenarios

These optimizations would trade some detail for speed, making plan generation suitable for rapid iteration scenarios.

### Other Future Enhancements

- Parallel test execution for multiple test cases
- Report generation with formatted plan/script outputs
- Test result comparison and regression detection
- Custom tool plugins for specialized testing scenarios
- Local caching of screenshots to reduce storage overhead
- Configure to run on AWS Bedrock so that agent can be integrated to run on CI/CD environment
