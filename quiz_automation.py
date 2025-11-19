import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging
import json

class QuizAutomation:
    def __init__(self, base_url="http://localhost:9000"):
        self.base_url = base_url
        self.driver = None
        self.wait = None
        self.test_results = []
        self.start_time = None
        self.setup_logging()
        self.setup_driver()
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = "test_logs"
        os.makedirs(log_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/quiz_test_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("detach", True)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def take_screenshot(self, step_name):
        """Take screenshot at each step"""
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshots_dir}/{step_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved: {filename}")
        time.sleep(1)  # Add delay after screenshot
        
    def verify_landing_page(self):
        """Step 1: Verify Landing Page"""
        self.logger.info("Step 1: Verifying Landing Page")
        
        self.driver.get(self.base_url)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        
        # Verify URL and Title
        current_url = self.driver.current_url
        page_title = self.driver.title
        
        self.logger.info(f"Current URL: {current_url}")
        self.logger.info(f"Page Title: {page_title}")
        
        # Verify page elements
        assert "Quiz Home" in page_title, f"Expected 'Quiz Home' in title, got: {page_title}"
        
        heading = self.driver.find_element(By.TAG_NAME, "h1").text
        assert "Dynamic Quiz App" in heading, f"Expected 'Dynamic Quiz App' in heading, got: {heading}"
        
        self.take_screenshot("landing_page")
        self.logger.info("Landing page verification completed successfully")
        time.sleep(2)  # Add delay after landing page verification
        
    def start_quiz(self, category="math", difficulty="easy"):
        """Step 2: Start Quiz"""
        self.logger.info(f"Step 2: Starting Quiz - Category: {category}, Difficulty: {difficulty}")
        
        # Select category
        category_dropdown = Select(self.driver.find_element(By.ID, "category"))
        category_dropdown.select_by_value(category)
        self.logger.info(f"Selected category: {category}")
        
        # Select difficulty
        difficulty_dropdown = Select(self.driver.find_element(By.ID, "difficulty"))
        difficulty_dropdown.select_by_value(difficulty)
        self.logger.info(f"Selected difficulty: {difficulty}")
        
        self.take_screenshot("quiz_setup")
        time.sleep(1)  # Add delay after quiz setup
        
        # Click Start Quiz button
        start_button = self.driver.find_element(By.XPATH, "//button[text()='Start Quiz']")
        start_button.click()
        
        # Wait for quiz page to load
        self.wait.until(EC.presence_of_element_located((By.ID, "question-box")))
        
        # Verify first question is displayed
        question_box = self.driver.find_element(By.ID, "question-box")
        assert question_box.is_displayed(), "First question is not displayed"
        
        self.take_screenshot("quiz_started")
        self.logger.info("Quiz started successfully, first question displayed")
        time.sleep(2)  # Add delay after quiz start
        
    def answer_questions(self):
        """Step 3: Answer all questions"""
        self.logger.info("Step 3: Answering all questions")
        
        question_count = 0
        
        while True:
            try:
                # Wait for question to load
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
                
                question_count += 1
                
                # Get question text
                question_element = self.driver.find_element(By.TAG_NAME, "h3")
                question_text = question_element.text
                self.logger.info(f"Question {question_count}: {question_text}")
                
                # Get answer options
                answer_options = self.driver.find_elements(By.NAME, "answer")
                
                if not answer_options:
                    self.logger.info("No more questions found, quiz completed")
                    break
                
                # Log available options
                labels = self.driver.find_elements(By.XPATH, "//label")
                for i, label in enumerate(labels):
                    if label.text.strip():
                        self.logger.info(f"Option {i}: {label.text}")
                
                # Select the first answer (you can modify this logic)
                answer_options[0].click()
                selected_answer = labels[0].text if labels else "Option 1"
                self.logger.info(f"Selected answer: {selected_answer}")
                
                self.take_screenshot(f"question_{question_count}_answered")
                time.sleep(1)  # Add delay after answering
                
                # Click Next button
                next_button = self.driver.find_element(By.ID, "nextBtn")
                next_button.click()
                
                # Small delay to allow page transition
                time.sleep(2)
                
            except Exception as e:
                self.logger.info(f"Quiz completed or error occurred: {str(e)}")
                break
                
        self.logger.info(f"Answered {question_count} questions")
        
    def verify_results(self):
        """Step 4: Verify results page"""
        self.logger.info("Step 4: Verifying results page")
        
        # Wait for results page to load
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result-container")))
        
        # Verify we're on results page
        current_url = self.driver.current_url
        assert "/result" in current_url, f"Expected to be on results page, current URL: {current_url}"
        
        # Get score
        score_element = self.driver.find_element(By.CSS_SELECTOR, ".score-box h2")
        score = score_element.text
        self.logger.info(f"Quiz Score: {score}")
        
        # Verify chart is present
        chart_element = self.driver.find_element(By.ID, "chart")
        assert chart_element.is_displayed(), "Results chart is not displayed"
        
        self.take_screenshot("final_results")
        self.logger.info("Results page verification completed successfully")
        time.sleep(2)  # Add delay after results verification
        
        return score
        
    def run_complete_test(self, category="math", difficulty="easy"):
        """Run the complete test scenario"""
        self.start_time = datetime.now()
        test_result = {
            "category": category,
            "difficulty": difficulty,
            "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "FAILED",
            "score": "N/A",
            "error": None
        }
        
        try:
            self.logger.info("Starting complete quiz automation test")
            
            # Step 1: Verify Landing Page
            self.verify_landing_page()
            
            # Step 2: Start Quiz
            self.start_quiz(category, difficulty)
            
            # Step 3: Answer Questions
            self.answer_questions()
            
            # Step 4: Verify Results
            final_score = self.verify_results()
            
            test_result["status"] = "PASSED"
            test_result["score"] = final_score
            test_result["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.logger.info(f"Test completed successfully! Final Score: {final_score}")
            
        except Exception as e:
            test_result["error"] = str(e)
            test_result["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.error(f"Test failed with error: {str(e)}")
            self.take_screenshot("error_state")
            raise
        finally:
            self.test_results.append(test_result)
            
    def generate_test_report(self):
        """Generate JSON test report"""
        reports_dir = "test_reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{reports_dir}/test_report_{timestamp}.json"
        
        report_data = {
            "report_info": {
                "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_tests": len(self.test_results),
                "passed_tests": sum(1 for r in self.test_results if r['status'] == 'PASSED'),
                "failed_tests": sum(1 for r in self.test_results if r['status'] == 'FAILED')
            },
            "test_cases": self.test_results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        self.logger.info(f"Test report generated: {report_file}")
        return report_file
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")

if __name__ == "__main__":
    # Create automation instance
    quiz_test = QuizAutomation()
    
    try:
        # Run test with different categories and difficulties
        test_scenarios = [
            ("math", "easy"),
            ("gk", "medium"),
            ("math", "hard")
        ]
        
        for category, difficulty in test_scenarios:
            print(f"\n{'='*50}")
            print(f"Running test: {category.upper()} - {difficulty.upper()}")
            print(f"{'='*50}")
            
            try:
                quiz_test.run_complete_test(category, difficulty)
            except Exception as e:
                print(f"Test failed: {e}")
                continue
            
    except Exception as e:
        print(f"Error running tests: {e}")
    finally:
        # Generate test report
        report_file = quiz_test.generate_test_report()
        print(f"\nTest report generated: {report_file}")
        quiz_test.cleanup()