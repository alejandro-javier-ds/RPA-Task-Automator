import time
import logging
import pyodbc
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

DB_CONFIG = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=(localdb)\\MSSQLLocalDB;"
    "Database=RPADatabase;"
    "Trusted_Connection=yes;"
)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

def execute_rpa_pipeline(target_url: str, max_pages: int = 10):
    start_time = time.time()
    extracted_data = []
    status = 'FAILED'
    
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    
    logging.info(f"PROCESS: Initializing WebDriver targeting {target_url}")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        for page in range(1, max_pages + 1):
            page_url = f"{target_url}/page/{page}/"
            logging.info(f"PROCESS: Navigating to {page_url}")
            driver.get(page_url)
            time.sleep(1.5) 
            
            elements = driver.find_elements(By.CLASS_NAME, "quote")
            
            if not elements:
                logging.warning("PROCESS: No elements found. Terminating loop.")
                break
                
            for el in elements:
                text = el.find_element(By.CLASS_NAME, "text").text
                author = el.find_element(By.CLASS_NAME, "author").text
                extracted_data.append({"Quote": text, "Author": author})
        
        driver.quit()
        
        df = pd.DataFrame(extracted_data)
        df.to_csv("data/extracted_items.csv", index=False)
        
        status = 'COMPLETED'
        logging.info(f"PROCESS: Extraction finished. {len(extracted_data)} objects serialized to data/extracted_items.csv")
        
    except Exception as e:
        logging.error(f"SYSTEM_ERROR: WebDriver failure - {str(e)}")
        
    finally:
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        try:
            conn = pyodbc.connect(DB_CONFIG)
            cursor = conn.cursor()
            query = """
                INSERT INTO AutomationLogs (TargetURL, ExecutionStatus, ItemsProcessed, DurationSeconds)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (target_url, status, len(extracted_data), duration))
            conn.commit()
            conn.close()
            logging.info(f"SQL_SYNC: Telemetry registered. Execution time: {duration}s.")
        except Exception as db_error:
            logging.error(f"SYSTEM_ERROR: Database sync failure - {str(db_error)}")

if __name__ == "__main__":
    execute_rpa_pipeline("https://quotes.toscrape.com")