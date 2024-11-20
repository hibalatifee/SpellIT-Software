import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfReader
import random
import pdfplumber

# Define the PDF file path
PDF_FILE = 'words.pdf'

# Define difficulty levels
DIFFICULTY_LEVELS = {
    'one_bee': 'one_bee',
    'two_bee': 'two_bee',
    'three_bee': 'three_bee'
}

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
    if words:
        output_text.set("\n".join(words))
    else:
        output_text.set("No words found for the selected difficulty level.")

def on_exit():
    root.destroy()

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
tk.Button(root, text="Exit", command=on_exit).pack()

output_text = tk.StringVar()
tk.Label(root, textvariable=output_text).pack()

root.mainloop()
