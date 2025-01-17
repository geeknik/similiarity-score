#!/usr/bin/env python3

import urllib.request
import sqlite3
import os.path
import re
import math

# This function takes a url and returns its text content
def get_text(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(e)
        return ''

# This function takes a text string and returns a list of words
def get_words(text):
    # Remove all non-alphanumeric characters
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Split into a list of words
    words = text.split()
    # Remove stop words
    stop_words = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with']
    words = [w for w in words if w not in stop_words]
    return words

# This function takes a url and returns a dictionary of words and their frequencies
def get_word_frequencies(url):
    text = get_text(url)
    words = get_words(text)
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] += 1
        else:
            frequencies[word] = 1
    return frequencies

# This function takes two dictionaries of words and their frequencies and returns a score between 0 and 1
# indicating how similar the two are.
def get_similarity(f1, f2):
    # Get the list of unique words
    unique_words = set(list(f1.keys()) + list(f2.keys()))
    # Initialize the numerator and denominator
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    # Calculate the numerator and denominators
    for word in unique_words:
        if word in f1 and word in f2:
            numerator += f1[word] * f2[word]
            denominator1 += f1[word] ** 2
            denominator2 += f2[word] ** 2
        elif word in f1:
            denominator1 += f1[word] ** 2
        else:
            denominator2 += f2[word] ** 2
    # Prevent division by zero
    if denominator1 == 0 or denominator2 == 0:
        return 0
    # Calculate and return the similarity score
    return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))

# This function takes a url and returns a dictionary of link destinations and their frequencies
def get_link_frequencies(url):
    text = get_text(url)
    # Find all links in the text
    links = re.findall('<a href="([^"]+)">', text)
    # Initialize the dictionary
    frequencies = {}
    # Calculate the frequencies
    for link in links:
        if link in frequencies:
            frequencies[link] += 1
        else:
            frequencies[link] = 1
    return frequencies

# This function takes two dictionaries of link destinations and their frequencies and returns a score between 0 and 1
# indicating how similar the two are.
def get_link_similarity(f1, f2):
    # Get the list of unique link destinations
    unique_links = set(list(f1.keys()) + list(f2.keys()))
    # Initialize the numerator and denominator
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    # Calculate the numerator and denominators
    for link in unique_links:
        if link in f1 and link in f2:
            numerator += f1[link] * f2[link]
            denominator1 += f1[link] ** 2
            denominator2 += f2[link] ** 2
        elif link in f1:
            denominator1 += f1[link] ** 2
        else:
            denominator2 += f2[link] ** 2
    # Prevent division by zero
    if denominator1 == 0 or denominator2 == 0:
        return 0
    # Calculate and return the similarity score
    return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))

# This function takes a url and returns a dictionary of css file names and their frequencies
def get_css_frequencies(url):
    text = get_text(url)
    # Find all css file names in the text
    css = re.findall('<link href="([^"]+.css)"', text)
    #css = re.findall('(\<style\>)(.+)(<\/style>)', text)
    # Initialize the dictionary
    frequencies = {}
    # Calculate the frequencies
    for file in css:
        if file in frequencies:
            frequencies[file] += 1
        else:
            frequencies[file] = 1
    return frequencies

# This function takes two dictionaries of css file names and their frequencies and returns a score between 0 and 1
# indicating how similar the two are.
def get_css_similarity(f1, f2):
    # Get the list of unique css file names
    unique_css = set(list(f1.keys()) + list(f2.keys()))
    # Initialize the numerator and denominator
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    # Calculate the numerator and denominators
    for file in unique_css:
        if file in f1 and file in f2:
            numerator += f1[file] * f2[file]
            denominator1 += f1[file] ** 2
            denominator2 += f2[file] ** 2
        elif file in f1:
            denominator1 += f1[file] ** 2
        else:
            denominator2 += f2[file] ** 2
    # Prevent division by zero
    if denominator1 == 0 or denominator2 == 0:
        return 0
    # Calculate and return the similarity score
    return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))

# This function takes a url and returns a dictionary of javascript file names and their frequencies
def get_javascript_frequencies(url):
    text = get_text(url)
    # Find all javascript file names in the text
    javascript = re.findall('<script src="([^"]+.js)"', text)
    # Initialize the dictionary
    frequencies = {}
    # Calculate the frequencies
    for file in javascript:
        if file in frequencies:
            frequencies[file] += 1
        else:
            frequencies[file] = 1
    return frequencies

# This function takes two dictionaries of javascript file names and their frequencies and returns a score between 0 and 1
# indicating how similar the two are.
def get_javascript_similarity(f1, f2):
    # Get the list of unique javascript file names
    unique_javascript = set(list(f1.keys()) + list(f2.keys()))
    # Initialize the numerator and denominator
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    # Calculate the numerator and denominators
    for file in unique_javascript:
        if file in f1 and file in f2:
            numerator += f1[file] * f2[file]
            denominator1 += f1[file] ** 2
            denominator2 += f2[file] ** 2
        elif file in f1:
            denominator1 += f1[file] ** 2
        else:
            denominator2 += f2[file] ** 2
    # Prevent division by zero
    if denominator1 == 0 or denominator2 == 0:
        return 0
    # Calculate and return the similarity score
    return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))

# This function takes a url and returns a dictionary of server header names and their frequencies
def get_header_frequencies(url):
    # Get the server headers
    headers = urllib.request.urlopen(url).getheaders()
    # Initialize the dictionary
    frequencies = {}
    # Calculate the frequencies
    for header in headers:
        name = header[0]
        if name in frequencies:
            frequencies[name] += 1
        else:
            frequencies[name] = 1
    return frequencies

# This function takes two dictionaries of server header names and their frequencies and returns a score between 0 and 1
# indicating how similar the two are.
def get_header_similarity(f1, f2):
    # Get the list of unique server header names
    unique_headers = set(list(f1.keys()) + list(f2.keys()))
    # Initialize the numerator and denominator
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    # Calculate the numerator and denominators
    for header in unique_headers:
        if header in f1 and header in f2:
            numerator += f1[header] * f2[header]
            denominator1 += f1[header] ** 2
            denominator2 += f2[header] ** 2
        elif header in f1:
            denominator1 += f1[header] ** 2
        else:
            denominator2 += f2[header] ** 2
    # Prevent division by zero
    if denominator1 == 0 or denominator2 == 0:
        return 0
    # Calculate and return the similarity score
    return numerator / (math.sqrt(denominator1) * math.sqrt(denominator2))

# This function calculates the similarity score for two URLs and stores it in the database.
# If the score in the database is stale, it is updated.
def calculate_similarity(url1, url2):
    # Get the word frequencies
    word_frequencies1 = get_word_frequencies(url1)
    word_frequencies2 = get_word_frequencies(url2)
    # Get the link frequencies
    link_frequencies1 = get_link_frequencies(url1)
    link_frequencies2 = get_link_frequencies(url2)
    # Get the css frequencies
    css_frequencies1 = get_css_frequencies(url1)
    css_frequencies2 = get_css_frequencies(url2)
    # Get the javascript frequencies
    javascript_frequencies1 = get_javascript_frequencies(url1)
    javascript_frequencies2 = get_javascript_frequencies(url2)
    # Get the header frequencies
    header_frequencies1 = get_header_frequencies(url1)
    header_frequencies2 = get_header_frequencies(url2)
    # Get the similarities
    word_similarity = get_similarity(word_frequencies1, word_frequencies2)
    link_similarity = get_link_similarity(link_frequencies1, link_frequencies2)
    css_similarity = get_css_similarity(css_frequencies1, css_frequencies2)
    javascript_similarity = get_javascript_similarity(javascript_frequencies1, javascript_frequencies2)
    header_similarity = get_header_similarity(header_frequencies1, header_frequencies2)
    # Calculate the overall similarity
    similarity = (word_similarity + link_similarity + css_similarity + javascript_similarity + header_similarity) / 5
    # Connect to the database
    conn = sqlite3.connect('similarity.db')
    c = conn.cursor()
    # Create the scores table if it doesn't exist
    c.execute('CREATE TABLE IF NOT EXISTS scores (url1 TEXT, url2 TEXT, score REAL, stale BOOLEAN)')
    # Get the score from the database
    c.execute('SELECT * FROM scores WHERE url1=? AND url2=?', (url1, url2))
    row = c.fetchone()
    # If the score is not in the database, insert it
    if row is None:
        c.execute('INSERT INTO scores VALUES (?, ?, ?, ?)', (url1, url2, similarity, 0))
    # If the score is in the database, update it if it is stale
    else:
        if row[2] < similarity or row[3] == 1:
            c.execute('UPDATE scores SET score=?, stale=? WHERE url1=? AND url2=?', (similarity, 0, url1, url2))
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()
    return similarity

# This function calculates the similarity between two URLs and displays the results.
def main():
    # Get the two URLs
    url1 = input('Enter the first URL: ')
    url2 = input('Enter the second URL: ')
    # Calculate the similarity score
    similarity = calculate_similarity(url1, url2)
    # Display the results
    print('The similarity score is ' + str(similarity))

# Run the main function
if __name__ == '__main__':
    main()
