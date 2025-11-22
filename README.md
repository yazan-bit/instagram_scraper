# instagram_scraper
python + selenium tool to scrape followers & following, compare them and generate mutuals summary

📌 Instagram Follower/Following Scraper

A Python automation tool that logs into an Instagram account (or any similar platform), extracts followers & following lists using Selenium, compares them, and generates a clean summary of mutual connections.


---

🚀 Features

Automated login using Selenium WebDriver

Manual or automatic ChromeDriver setup

Extract followers & following lists (handle scrolling and waits data to load)

calculate results and generate a set of your friends and not_friends (you follow but don't get follow back)

Saves results into:

JSON file (raw data)

TXT summary file (human readable) with some statistics


Fully automated scraping flow with minimal user interaction (just enter your username and password)



---

🗂 Project Structure

project/
│
├── data/                     # Raw scraped data (followers/following)
├── result/                   # Summary output files (json + txt)
├── src/
│   ├── scraper.py            # Main entry point (contains main())
│   └── analyzer.py           # Compares data & generates summary
│
├── requirements.txt          # Dependencies
└── README.md                 # Documentation


---

▶️ How It Works (Scraping Flow)

1. Navigate to login page


2. Enter username + password


3. Handle pop-up pages (“Press OK”)


4. Navigate to profile page


5. Open Followers list waits data to load → scrape


6. Open Following list waits data to load → scrape


7. Compare both sets


8. Save output into JSON + summary text


9. Done!




---

🔧 Installation

1️⃣ Clone the repository

git clone https://github.com/yazan-bit/instagram-scraper.git
cd instagram-scraper


---

2️⃣ Install requirements

pip install -r requirements.txt


---

3️⃣ ChromeDriver Setup

Option A — Manual (What I used)

Download ChromeDriver that matches your Chrome version:
https://chromedriver.chromium.org/downloads

Then place it in your project folder or system PATH.

Option B — Automatic (Recommended for users)

Selenium now supports automatic driver installation:

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

This will install the correct driver automatically.


---

▶️ Running the Scraper

The entry point is scraper.py, which contains the main() function.

python src/scraper.py

You will be asked for:

Username

Password


Then the scraper will automatically:

Login

Handle any pop-ups

Scrape followers

Scrape following

Save results to:


result/
   analysis_timestamp.json
   summary_timestamp.txt


---

📊 Output

JSON File (data)

Contains full raw lists of followers and following.

Summary TXT File (result)

Contains:

Total followers

Total following

and some other info

---

⚠️ Disclaimer

This tool is for educational and personal-use only.
Always respect platform Terms of Service and avoid scraping data you don’t own.


---

🤝 Contributions

PRs and suggestions are welcome!
If you want to extend this scraper or add features, feel free to open an issue.


---

⭐ Show Support

If you found this project useful, please leave a ⭐ on the repository!
