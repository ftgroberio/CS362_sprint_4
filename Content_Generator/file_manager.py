# CS361 - Software Engineering I
# Sprint 3: Content Generator - file manager function
# Author: Felipe Groberio <teixeirf@oregonstate.edu>
# Date: February 13th, 2021

import argparse

def get_input_words_from_file(file_name):
    # Discart header
    file_name.readline()
    
    # Grab words
    line = file_name.readline()

    # Split primary and secondary keywords
    words = line.split(';')
    second_word = words[1].split('\n')
    words[1] = second_word[0]
    return words

def create_output_file(words, content):
    try:
        # Attempt to create output file
        f = open('output.csv', 'w')

        # Insert .csv header
        f.write('input_keywords,output_content\n')
        
        if(type(words) == type([])):
            # Concatenate input keywords in one cell
            input_keywords = words[0] + ';' + words[1] + ','
        else:
            input_keywords = words + ','
        f.write(input_keywords)

        # Clean the content and insert quotes
        content = content.replace('\"','\'')
        content = '\"' + content + '\"'

        # Output to file
        f.write(content)

        # Inform the user if the file was created or not
        print('output.csv file created')
    except:
        print('Program was unable to create output.csv')
