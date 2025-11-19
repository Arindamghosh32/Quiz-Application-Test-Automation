# Quiz Application Automation

This project contains automated tests for a dynamic quiz application using Selenium WebDriver.

## Project Structure

```
questions/
├── quiz_automation.py          # Main automation script
├── index.js                    # Quiz application server
├── package.json               # Node.js dependencies
├── requirements.txt           # Python dependencies
├── public/                    # Static CSS files
├── views/                     # EJS templates
├── test_logs/                 # Test execution logs
├── screenshots/               # Test screenshots
├── test_reports/              # JSON test reports
└── README.md                  # This file
```

## Prerequisites

### Software Requirements
- Python 3.7+
- Node.js 14+
- Chrome Browser
- ChromeDriver (matching your Chrome version)

### Python Dependencies
```bash
pip install selenium
```

### Node.js Dependencies
```bash
npm install
```

## Setup Instructions

1. **Install ChromeDriver:**
   - Download from https://chromedriver.chromium.org/
   - Add to system PATH or place in project directory

2. **Start Quiz Application:**
   ```bash
   node index.js
   ```
   Application runs on http://localhost:9000

3. **Run Automation Tests:**
   ```bash
   python quiz_automation.py
   ```

## Test Scenarios

The automation covers these test cases:

### 1. Landing Page Verification
- Opens quiz URL
- Verifies page title and heading
- Takes screenshot

### 2. Quiz Start
- Selects category and difficulty
- Clicks Start Quiz button
- Verifies first question display

### 3. Question Navigation & Answer Selection
- Answers all quiz questions
- Takes screenshots at each step
- Logs question text and selected answers

### 4. Results Verification
- Verifies results page display
- Captures final score
- Validates chart presence

## Test Categories & Difficulties

- **Categories:** Math, General Knowledge (GK)
- **Difficulties:** Easy, Medium, Hard

## Output Files

### Screenshots
- Saved in `screenshots/` directory
- Captured at each test step
- Timestamped filenames

### Logs
- Saved in `test_logs/` directory
- Detailed execution information
- Error tracking and debugging info

### Test Reports
- Generated in `test_reports/` directory
- JSON format with structured test data
- Pass/fail status for each scenario
- Execution timestamps and scores

## Test Report Features

- **Test Summary:** Total, passed, and failed test counts
- **Individual Results:** Status, timing, and scores for each test
- **Error Details:** Failure reasons when tests don't pass
- **Machine Readable:** JSON format for easy integration with other tools

## Test Execution Timing

The automation includes strategic delays for reliability:
- 1-2 second delays between test steps
- Screenshot capture with 1 second delay
- Page transition waits of 2 seconds
- Enhanced stability for element interactions

## Customization

### Modify Test Scenarios
Edit the `test_scenarios` list in `quiz_automation.py`:
```python
test_scenarios = [
    ("math", "easy"),
    ("gk", "medium"),
    ("math", "hard")
]
```

### Change Answer Selection Logic
Update the `answer_questions()` method to implement custom answer selection strategies.

### Adjust Timeouts and Delays
- Modify WebDriverWait timeout in `setup_driver()` method
- Adjust step delays by changing `time.sleep()` values throughout the code
- Current delays: 1-2 seconds between major steps for stability

## Troubleshooting

### Common Issues

1. **ChromeDriver not found:**
   - Ensure ChromeDriver is in PATH
   - Check Chrome and ChromeDriver version compatibility

2. **Quiz application not running:**
   - Start the Node.js server: `node index.js`
   - Verify http://localhost:9000 is accessible

3. **Element not found errors:**
   - Check if quiz application UI has changed
   - Verify element selectors in the code

4. **Permission errors:**
   - Run with appropriate permissions
   - Check directory write access for logs/screenshots

## Browser Configuration

The automation uses Chrome with these options:
- Maximized window
- Detached mode (browser stays open after test)
- 10-second element wait timeout
