import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import csv
import re

# Function to read text or CSV files
def read_file(file_path):
    content = ""
    try:
        if file_path.endswith('.csv'):
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    content += ' '.join(row) + ' '
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {file_path}")
    return content

# Function to search words in the content
def search_words(content, words):
    word_info = {word.strip(): {'count': 0, 'lines': []} for word in words}
    lines = content.splitlines()

    for line_number, line in enumerate(lines, start=1):
        for word in words:
            word = word.strip()
            pattern = fr'\b{re.escape(word)}\b'
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                word_info[word]['count'] += len(matches)
                word_info[word]['lines'].append(line_number)

    return word_info

# Function to start the search process
def start_search():
    file_path = file_path_var.get()
    words = words_entry.get().split(',')
    if not file_path or not words:
        messagebox.showwarning("Input Error", "Please select a file and enter words to search.")
        return

    content = read_file(file_path)
    if content:
        results = search_words(content, words)
        display_results(results)

# Function to display results in the GUI
def display_results(results):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Word Search Results:\n\n")
    for word, info in results.items():
        result_text.insert(tk.END, f"'{word}': {info['count']} occurrences on lines {info['lines']}\n")

# Function to select a file
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a Text or CSV File",
        filetypes=(("Text files", "*.txt"), ("CSV files", "*.csv"))
    )
    file_path_var.set(file_path)

# Setting up the main window
root = tk.Tk()
root.title("Word Search Tool")

# File path selection
file_path_var = tk.StringVar()
tk.Label(root, text="File:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
tk.Entry(root, textvariable=file_path_var, width=40).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Word input
tk.Label(root, text="Words to Search (comma-separated):").grid(row=1, column=0, padx=10, pady=10, sticky='e')
words_entry = tk.Entry(root, width=40)
words_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

# Search button
tk.Button(root, text="Search", command=start_search).grid(row=2, column=0, columnspan=3, pady=10)

# Result display area
result_text = scrolledtext.ScrolledText(root, width=60, height=20)
result_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()

