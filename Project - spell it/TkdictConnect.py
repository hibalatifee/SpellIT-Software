import logging
import requests
import json
import tkinter as tk
from tkinter import messagebox

# Configure logging
logging.basicConfig(level=logging.INFO)

def connect_mw_dictionary(word):
    logging.info("Connecting...")
    URL = f"https://dictionaryapi.com/api/v3/references/learners/json/{word}?key=cc613e92-70a4-413a-ad20-af03266e45d2"
    try:
        r = requests.get(url=URL)
        r.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        logging.info("Connection successful.")
        logging.debug(f"Response content: {r.text}")  # Log raw response text
        return True, r.text  # Return raw text to handle manually
    except requests.exceptions.RequestException as e:
        logging.error(f"Connection failed: {e}")
        return False, None

def fetch_dictionary_result(res):
    if res is None or res.strip() == "":
        logging.error("Response content is empty or None.")
        return "No definition found."

    try:
        data = json.loads(res)  # Parse JSON from raw text
        if isinstance(data, list) and len(data) > 0:
            dict_txt = str(data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1]).replace("{bc}", "")
            return dict_txt
        else:
            logging.error("Unexpected JSON structure.")
            return "No definition found."
    except (IndexError, KeyError, TypeError, json.JSONDecodeError) as e:
        logging.error(f"Error parsing dictionary result: {e}")
        return "No definition found."

def search_word():
    word = entry.get()
    if not word:
        messagebox.showwarning("Input Error", "Please enter a word.")
        return

    status, result = connect_mw_dictionary(word)
    if status:
        definition = fetch_dictionary_result(result)
        result_text.set(f"Definition: {definition}")
    else:
        result_text.set("Failed to fetch dictionary results.")

# Create main window
root = tk.Tk()
root.title("Dictionary Lookup")

# Create and place widgets
tk.Label(root, text="Enter a word:").pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search_word)
search_button.pack(pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=500)
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
