import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("config/credentials.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet
sheet = client.open("Applied Jobs").sheet1  # Select first sheet

def store_job(job_title, company, job_link):
    """Store job details in Google Sheets to avoid duplicate applications."""
    existing_jobs = sheet.col_values(3)  # Get all applied job links
    if job_link not in existing_jobs:
        sheet.append_row([job_title, company, job_link])
        print(f"✅ Job '{job_title}' at '{company}' stored successfully.")
    else:
        print(f"⚠️ Job '{job_title}' already applied, skipping.")

if __name__ == "__main__":
    store_job("Software Engineer", "Google", "https://example-job.com")
