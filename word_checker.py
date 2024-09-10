import csv
import re

def read_file(file_path):
    """Reads a text or CSV file and returns its content as a string."""
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
        print(f"File not found: {file_path}")
    return content

def search_words(content, words):
    """Searches for the list of words in the content and counts their exact occurrences, including line numbers."""
    word_info = {word.strip(): {'count': 0, 'lines': []} for word in words}

    # Split content into lines
    lines = content.splitlines()

    for line_number, line in enumerate(lines, start=1):
        for word in words:
            word = word.strip()  # Clean the word
            # Using regex to match exact words, considering word boundaries (\b)
            pattern = fr'\b{re.escape(word)}\b'
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                word_info[word]['count'] += len(matches)
                word_info[word]['lines'].append(line_number)

    return word_info

def main():
    # Prompt the user for the file path and list of words
    file_path = input("Enter the path of the text or CSV file: ").strip()
    words = input("Enter the list of words to search for (comma-separated): ").strip().split(',')

    # Read the file content
    content = read_file(file_path)

    # Search for the words in the content
    if content:
        results = search_words(content, words)
        # Display the results
        print("\nWord Search Results:")
        for word, info in results.items():
            print(f"'{word}': {info['count']} occurrence(s) on lines {info['lines'] if info['lines'] else 'None'}")
    else:
        print("No content found in the file.")

if __name__ == "__main__":
    main()
