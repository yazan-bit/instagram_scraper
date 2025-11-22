from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import time
import json
import getpass
import csv

class InstagramAnalyzer:
    def __init__(self,username):
        self.username = username
        self.driver = None
        self.wait = None
        self.is_logged_in = False
        
    def setup_driver(self):
        """Initialize the Chrome driver with appropriate options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        service = Service(r"C:\Drivers\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service,options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 15)
        
    def login(self, username=None, password=None):
        """Login to Instagram"""
        try:
            if not self.username:
                self.username = input("Enter Instagram username: ")
                self.username = username
            if not password:
                password = getpass.getpass("Enter Instagram password: ")
            
            print("Navigating to Instagram login page...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            # Wait for login form to load
            self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            
            # Fill login form
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.clear()
            password_field.clear()
            
            username_field.send_keys(self.username)
            time.sleep(1)
            password_field.send_keys(password)
            time.sleep(2)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            time.sleep(5)
            
            # Handle "Save Login Info" prompt
            try:
                not_now_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not now')]"))
                )
                not_now_button.click()
                time.sleep(2)
            except TimeoutException:
                pass
            
            # Handle "OK" button for "message tab has a new look" tab
            try:
                ok_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='OK' or text()='موافق']"))
                )
                ok_button.click()
                time.sleep(2)
            except TimeoutException:
                pass


            # Handle notifications dialog
            try:
                not_now_notifications = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
                )
                not_now_notifications.click()
                time.sleep(2)
            except TimeoutException:
                pass
            
            # Verify login success
            if "accounts/login" not in self.driver.current_url:
                self.is_logged_in = True
                print("Login successful!")
                return True
            else:
                print("Login failed - please check credentials")
                return False
                
        except Exception as e:
            print(f"Login error: {str(e)}")
            return False
    
    def get_my_followers_list(self):
        """Get list of my followers for a user"""
        if not self.is_logged_in:
            print("Please login first!")
            return []
        
        try:
            print(f"Fetching followers for @{self.username}...")
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(5)
            followers_link = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"a[href$='/followers/']"))
            )
            followers_link.click()
            time.sleep(2)
            
            # Wait for followers dialog to load
            followers_dialog = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@role, 'dialog')]"))
            )

            # get scroll box tp prefrom scrolling
            scroll_box = self.driver.find_element(By.XPATH,"//div[contains(@class,'x6nl9eh')]")
            
            followers = set()
            last_height = 0
            
            while True:
                # Find all follower(username) elements in the dialog
                followers_username = followers_dialog.find_elements(
                    By.XPATH, ".//span[contains(@class,'_ap3a') or contains(@class,'_aaco')]"
                )
                
                for follower_name in followers_username:
                    username = follower_name.text.strip()
                    followers.add(username)
                
                # Scroll down
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box
                )
                time.sleep(3)
                
                # Check if we've reached the bottom
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", scroll_box)
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                
                print(f"Collected {len(followers)} followers so far...")
            
            return followers
            
        except Exception as e:
            print(f"Error getting followers: {str(e)}")
            return []
    
    def get_my_following_list(self):
        """Get list of my following for a user"""
        if not self.is_logged_in:
            print("Please login first!")
            return []
        
        try:
            print(f"Fetching following for @{self.username}...")
            self.driver.get(f"https://www.instagram.com/{self.username}/")
            time.sleep(5)
            following_link = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"a[href$='/following/']"))
            )
            following_link.click()
            time.sleep(2)
            
            # Wait for followers dialog to load
            following_dialog = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@role, 'dialog')]"))
            )

            # get scroll box tp prefrom scrolling
            scroll_box = self.driver.find_element(By.XPATH,"//div[contains(@class,'x6nl9eh')]")
            
            following = set()
            last_height = 0
            
            while True:
                # Find all follower(username) elements in the dialog
                following_username = following_dialog.find_elements(
                    By.XPATH, ".//span[contains(@class,'_ap3a') or contains(@class,'_aaco')]"
                )
                print()
                
                for following_name in following_username:
                    username = following_name.text.strip()
                    following.add(username)
                
                # Scroll down
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", scroll_box
                )
                time.sleep(3)
                
                # Check if we've reached the bottom
                new_height = self.driver.execute_script("return arguments[0].scrollHeight", scroll_box)
                if new_height == last_height:
                    break
                else:
                    last_height = new_height
                
                print(f"Collected {len(following)} following so far...")
        
            return following
            
        except Exception as e:
            print(f"Error getting followers: {str(e)}")
            return []
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\nBrowser closed.")


class InstagramDataSaver:
    def __init__(self,username):
        self.username = username
        self.timestamp = datetime.now().strftime("Y%m%d_%H%M%S")
        self.base_filename = f"instagram_analysis_{self.timestamp}"


    def save_to_json(self,followers:set,following:set,friends:set,not_friends:set):
        #save all data to ajson file
        data = {
            "analysis_info":{
                "username":self.username,
                "total_followers":len(followers),
                "total_following":len(following),
                "total_friends":len(friends),
                "total_not_friends":len(not_friends)
            },
            "followers":list(followers),
            "following":list(following),
            "friends":list(friends),
            "not_friends":list(not_friends)
        }

        filename = f"{self.base_filename}.json"
        
        try:
            with open(f"../data/{filename}", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved to JSON: {filename}")
            return filename
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return None


    def save_summary_report(self, followers:set, following:set, friends:set, not_friends:set):
        """Save a summary report as text file"""
        filename = f"{self.base_filename}_summary.txt"
        
        try:
            with open(f"../result/{filename}", 'w') as f:
                f.write("=" * 50 + "\n")
                f.write("INSTAGRAM FRIENDSHIP ANALYSIS REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Analysis for: @{self.username}\n")
                f.write(f"Total Followers: {len(followers):,}\n")
                f.write(f"Total Following: {len(following):,}\n")
                f.write(f"Mutual Friends: {len(friends):,}\n")
                f.write(f"Not Following Back: {len(not_friends):,}\n")
                f.write(f"Fans (follow you but you don't follow back): {len(followers - following):,}\n\n")
                
                friendship_ratio = len(friends) / len(following) * 100 if following else 0
                f.write(f"Friendship Ratio: {friendship_ratio:.1f}% of people you follow follow you back\n\n")
            
            print(f"Summary report saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"Error saving summary: {e}")
            return None