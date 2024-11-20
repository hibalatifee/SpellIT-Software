import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfReader
import random
import requests
import json
import pdfplumber

# Define the PDF file path
PDF_FILE = 'words.pdf'

# Define difficulty levels
DIFFICULTY_LEVELS = {
    'one_bee': 'one_bee',
    'two_bee': 'two_bee',
    'three_bee': 'three_bee'
}

# Define API key for dictionary lookup
#API_KEY = '77c81f4-189d-4000-b947-fafd0a226f2d'

# Define categories
categories = {
    'one_bee': [],
    'two_bee': [],
    'three_bee': []
}

def extract_words_from_pdf(pdf_path):
    words = {
        'one_bee': [],
        'two_bee': [],
        'three_bee': []
    }
    
    current_category = None

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    # Split the line into parts
                    parts = line.split()
                    
                    if not parts:
                        continue
                    
                    # Check if the first part is a valid category
                    potential_category = parts[0]
                    if potential_category in words:
                        current_category = potential_category
                        # Skip to the next line to avoid adding the category name itself
                        continue
                    
                    # If we are in a valid category, add words to that category
                    if current_category and len(parts) > 0:
                        words_list = parts
                        words[current_category].extend(words_list)
    
    return words

# Load words from PDF
all_words = extract_words_from_pdf(PDF_FILE)

def generate_words(difficulty_level, num_words):
    if difficulty_level not in DIFFICULTY_LEVELS:
        return []

    category_words = all_words[difficulty_level]
    #print(f"Number of words in {difficulty_level}: {len(category_words)}")
    
    if len(category_words) < num_words:
        words_to_use = category_words
    else:
        words_to_use = random.sample(category_words, num_words)
    
    return words_to_use

def connect_mw_dictionary(word):
    URL = f"https://dictionaryapi.com/api/v3/references/learners/json/{word}?key=cc613e92-70a4-413a-ad20-af03266e45d2"
    try:
        r = requests.get(url=URL)
        r.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return True, r.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Failed to connect to the dictionary API: {e}")
        return False, None

def fetch_dictionary_result(res):
    if res is None or res.strip() == "":
        return "No definition found."

    try:
        data = json.loads(res)
        if isinstance(data, list) and len(data) > 0:
            #dict_txt = str(data[0]['fl']) # functional label, working
            #dict_txt = str(data[0]['fl']) + "\n" + (str(data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1]).replace("{bc}", "")) # def and functional label working
            #dict_txt = str(data[0]['hwi']['prs'][0]['sound']['audio']) #working
            dict_txt = "\nPart of Speech: "+ str(data[0]['fl']) + "\n" + "🕪 " + str(data[0]['hwi']['hw']) + " | " + str(data[0]['hwi']['prs'][0]['ipa']) + "\nDefinition: "+ str(data[0]['shortdef'][0]) + ".\nSentence: "+  str(data[0]['def'][0]['sseq'][0][0][1]['dt'][1][1][0]['t']).replace('{it}', '').replace('{/it}', '').replace('[]', '')
            return dict_txt
        else:
            return "No definition found."
    except (IndexError, KeyError, TypeError, json.JSONDecodeError) as e:
        return "Error parsing dictionary result."

def on_generate():
    difficulty_level = difficulty_var.get()
    try:
        num_words = int(num_words_entry.get())
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number of words.")
        return
    
    if not difficulty_level:
        messagebox.showwarning("Input Error", "Please select a difficulty level.")
        return

    words = generate_words(difficulty_level, num_words)

    # Clear previous buttons
    for widget in button_frame.winfo_children():
        widget.destroy()

    if words:
        for word in words:
            # Create a button for each word
            btn = tk.Button(button_frame, text=word, command=lambda w=word: on_word_click(w))
            btn.pack(pady=2)
    else:
        messagebox.showinfo("Result", "No words found for the selected difficulty level.")

def on_word_click(word):
    status, result = connect_mw_dictionary(word)
    if status:
        definition = fetch_dictionary_result(result)
        messagebox.showinfo("Word Definition", f"{word} {definition}")
    else:
        messagebox.showinfo("Word Definition", "Failed to fetch definition.")

#def on_exit():
#    root.destroy()

# Create GUI
root = tk.Tk()
root.title("Spelling Bee Word Generator")

tk.Label(root, text="Select Difficulty Level").pack()
difficulty_var = tk.StringVar()
tk.Radiobutton(root, text="One Bee", variable=difficulty_var, value='one_bee').pack()
tk.Radiobutton(root, text="Two Bee", variable=difficulty_var, value='two_bee').pack()
tk.Radiobutton(root, text="Three Bee", variable=difficulty_var, value='three_bee').pack()

tk.Label(root, text="Number of Words to Generate").pack()
num_words_entry = tk.Entry(root)
num_words_entry.pack()

tk.Button(root, text="Generate Words", command=on_generate).pack()
#tk.Button(root, text="Exit", command=on_exit).pack()

# Frame to contain buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

root.mainloop()
