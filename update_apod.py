import requests
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# NASA APOD API endpoint
apod_url = "https://api.nasa.gov/planetary/apod"

def get_apod(api_key):
    """Fetches the NASA APOD data."""
    params = {"api_key": api_key}
    response = requests.get(apod_url, params=params)
    response.raise_for_status()  # Raise an exception for bad responses
    return response.json()

def update_readme(apod_data, readme_path="README.md"):
    """Updates the README file with the APOD data and last updated timestamp."""
    with open(readme_path, "r") as f:
        readme_content = f.read()
    # Find and replace the APOD section in the README
    start_marker = "<!-- APOD Start -->"
    end_marker = "<!-- APOD End -->"
    
    # Generate the last updated timestamp
    timestamp = datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p (in %Z)")
    last_updated_section = f"> _Last Updated: {timestamp}_"
    apod_section = f"{start_marker}\n{apod_data['date']}: {apod_data['title']}\n![{apod_data['title']}]({apod_data['url']})\n{apod_data['explanation']}\n{last_updated_section}\n{end_marker}"
    updated_readme = readme_content.split(start_marker)[0] + apod_section + readme_content.split(end_marker)[1]
    with open(readme_path, "w") as f:
        f.write(updated_readme)

def commit_and_push(readme_path="README.md"):
    """Commits the changes and pushes to GitHub."""
    os.system(f"git config --global user.name 'Atanu0341'")
    os.system(f"git config --global user.email 'atanumajumder2004@gmail.com'")
    os.system(f"git add {readme_path}")
    os.system(f'git commit -m "Update APOD for {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"')
    os.system("git push")

if __name__ == "__main__":
    api_key = os.getenv("NASA_API_KEY")  # Get API key from environment variable
    if not api_key:
        raise ValueError("NASA_API_KEY environment variable is not set. Make sure you have a .env file with the key.")

    apod_data = get_apod(api_key)
    update_readme(apod_data)
    commit_and_push()
    print("README updated successfully!")
