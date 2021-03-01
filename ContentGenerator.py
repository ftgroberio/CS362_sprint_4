# CS361 - Software Engineering I
# Sprint 3: Content Generator - main function
# Author: Felipe Groberio <teixeirf@oregonstate.edu>
# Date: February 13th, 2021

import argparse
import Content_Generator.beaver_query_gui as gui
import Content_Generator.wikipedia_API_query as wikiAPI
import Content_Generator.file_manager as file_manager
import Content_Generator.communication as cm

from multiprocessing import Queue

def content_generator_microservice(request, receive):
    while True:
        # pop words from queue
        words = request.get()

        # query wikipedia
        wiki = wikiAPI.get_paragraph(words[0], words[1])

        # If no results are returned, inform user and exit
        if (wiki == {}):
            receive.put('Information not available.')
        else:
            receive.put(wiki['content'])
    return


if __name__ == "__main__":
    # Set up arguments
    parser = argparse.ArgumentParser(description='Input csv file may be provided')

    # Add non required argument for input file
    parser.add_argument('input', nargs='?', type=str, help='Takes a .csv file')

    # Parse arguments
    args = parser.parse_args()

    # Check if user provided an input file argument
    if(args.input != None):
        try:
            # Attempt to open user input
            input_file = open(args.input, 'r')
        except:
            # Inform user that the program encountered an issue
            print('File does not exists. Please try again.')
            exit()

        # Grab words from input file
        words = file_manager.get_input_words_from_file(input_file)

        # Query wikipedia 
        wiki = wikiAPI.get_paragraph(words[0],words[1])

        # If no results are returned, inform user and exit
        if(wiki == {}):
            print('Search yields no results.')
            exit()

        # Attempt to create output file
        file_manager.create_output_file(words,wiki['content'])

        # Close file descriptor
        input_file.close()

    # If the user did not provide an input, initialize GUI
    else:
    
        window = gui.BeaverQueryGUI()
        window.mainloop()
        window.p.terminate()
