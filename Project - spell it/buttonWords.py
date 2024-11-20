import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfReader
import random

# Define the PDF file path
PDF_FILE = 'words.pdf'

# Define difficulty levels
DIFFICULTY_LEVELS = {
    'one_bee': 'one_bee',
    'two_bee': 'two_bee',
    'three_bee': 'three_bee'
}

# Load and categorize words from PDF
def extract_words_from_pdf(pdf_path):
    words = {
        'one_bee': [],
        'two_bee': [],
        'three_bee': []
    }
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                parts = line.split()
                if len(parts) > 1:
                    difficulty = parts[0]
                    if difficulty in words:
                        words_list = parts[1:]
                        words[difficulty].extend(words_list)
    return words

# Load words from PDF
all_words = extract_words_from_pdf(PDF_FILE)

def generate_words(difficulty_level, num_words):
    if difficulty_level not in DIFFICULTY_LEVELS:
        return []

    category_words = all_words[difficulty_level]
    
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
    messagebox.showinfo("Word Clicked", f"You clicked on: {word}")

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
#tk.Button(root, text="Exit", command=on_exit).pack()

# Frame to contain buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

root.mainloop()
