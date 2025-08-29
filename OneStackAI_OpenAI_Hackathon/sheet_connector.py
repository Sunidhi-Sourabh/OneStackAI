 import requests

def fetch_tools_from_sheet():
    # Replace this with your actual deployment URL
    url = "https://script.google.com/macros/s/AKfycbwVZb1bEJZ1eWZzvWJvZqvZfZb9FfF7mH7e6z6uFh7e6z6uFh7e6z6uFh7e6z6uFh7e6z6uFh7e6z6uFh7e6z6uFh7e6z6uFh7e6z6uFh7e6z6uF/exec"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data from Google Sheets API: {e}")
        return []
if __name__ == "__main__":
    data = fetch_tools_from_sheet()
    print("[✅] Sheet data fetched:")
    for row in data[:3]:  # Show first 3 rows
        print(row)
