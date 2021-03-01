# CS361 - Software Engineering I
# Sprint 3: Content Generator - GUI
# Author: Felipe Groberio <teixeirf@oregonstate.edu>
# Date: February 13th, 2021

import tkinter as tk
from tkinter import *
from warnings import resetwarnings
import Content_Generator.wikipedia_API_query as wikiAPI
import Content_Generator.file_manager as file_manager


from multiprocessing import Process, Queue
import LifeGenerator as LG

# https://stackoverflow.com/questions/20399243/display-message-when-hovering-over-something-with-mouse-cursor-in-python
import Content_Generator.tool_tip as tt

import Content_Generator.communication as comms


class BeaverQueryGUI(tk.Tk):
    def __init__(self):
        super(BeaverQueryGUI, self).__init__()


        self.title('BeaverQuery')
        self.resizable(0, 0)
        self.wm_geometry("480x640")

        self.init_grid()
        self.init_labels()
        self.init_text_boxes()
        self.init_buttons()
        self.init_LG_process()

        self.wiki = {}

    def init_LG_process(self):
        self.request = Queue()
        self.receive = Queue()
        self.p = Process(target=LG.life_generator_microservice,
                         args=(self.request, self.receive))
        self.p.start()

    def init_grid(self):
        # Initialize main frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Setting up weights
        weight = [3,    # Index 0 - Title
                  1,      # Index 1 - Primary/secondary word label
                  1,      # Index 2 - Input text box
                  1,      # Index 3 - Search button
                  1,      # Index 4 - URL label
                  1,      # Index 5 - URL text box
                  1,      # Index 6 - Content label
                  5,      # Index 7 - Content text box
                  1]      # Index 8 - Output and exit button

        # Configuring each row with a custom weight
        for i in range(len(weight)):
            container.grid_rowconfigure(i, weight=weight[i])

        # Configuring columns with same weight
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        self.container = container

    def init_labels(self):
        # TITLE LABEL
        top_title = tk.Label(self.container, text='Beaver')
        top_title.config(font=("Courier", 24), foreground='orange')
        top_title.grid(row=0, column=0, sticky=tk.E)
        top_title = tk.Label(self.container, text='Query')
        top_title.config(font=("Courier", 24))
        top_title.grid(row=0, column=1, sticky=tk.W)

        # INPUT LABELS
        label = tk.Label(self.container, text='Primary search word:')
        label.grid(row=1, column=0, sticky=tk.SW, padx=(10, 0))
        label = tk.Label(self.container, text='Secondary search word:')
        label.grid(row=1, column=1, sticky=tk.SW, padx=(16, 0))

        # OUTPUT LABELS
        # self.url = tk.StringVar()
        # self.paragraph = tk.StringVar()
        url_label = tk.Label(self.container, text='Wikipedia URL:')
        url_label.grid(row=4, column=0, columnspan=2,
                       sticky=tk.SW, padx=(10, 0))
        par_label = tk.Label(self.container, text='Wikipedia content:')
        par_label.grid(row=6, column=0, columnspan=2,
                       sticky=tk.SW, padx=(10, 0), pady=(0, 0))

        self.url = url_label
        self.par = par_label

    def life_generator_labels(self):
        self.url.config(text='(Life Generator) Amazon Item Category:')
        self.par.config(text='(Life Generator) Amazon Item Description:')
        self.update_gui_message('Sending request to Life Generator...')

    def wikipedia_labels(self):
        self.url.config(text='Wikipedia URL:')
        self.par.config(text='Wikipedia content:')

    def init_buttons(self):
        # Search button
        search_btn = tk.Button(self.container, width=20, text="SEARCH WORDS",
                               command=self.button_func)
        search_btn.grid(row=3, column=0)

        message = "Searches Wikipedia using the\nprimary and secondary words."
        tt.CreateToolTip(search_btn, message)

        # Output and exit button
        output_btn = tk.Button(self.container, text="OUTPUT AND EXIT",
                               command=self.btn_output)
        output_btn.grid(row=8, column=0, columnspan=2, pady=(4, 10))

        # Get lucky button
        get_lucky_btn = tk.Button(self.container, text="...OR, GET LUCKY!",
                                  command=self.get_lucky_btn)
        get_lucky_btn.grid(row=3, column=1, pady=(4, 10))

        message = "Requests from the Life Generator\n"
        message = message + "microservice to send a pair of words."
        tt.CreateToolTip(get_lucky_btn, message)

    def init_text_boxes(self):
        # Primary keyword input box
        self.primary_word = tk.StringVar(self.container)
        self.input_pw = tk.Entry(
            self.container, textvariable=self.primary_word)
        self.input_pw.grid(row=2, column=0, sticky=tk.E+tk.W, padx=(10, 15))

        # Secondary keyword input box
        self.secondary_word = tk.StringVar(self.container)
        self.input_sw = tk.Entry(
            self.container, textvariable=self.secondary_word)
        self.input_sw.grid(row=2, column=1, sticky=tk.E+tk.W, padx=(15, 10))

        # URL output box
        self.url_t = tk.Text(self.container, height=1)
        self.url_t.grid(row=5, column=0, columnspan=2,
                        sticky=tk.E+tk.W, padx=10)

        # Content output box
        self.content_t = tk.Text(self.container, height=15)
        self.content_t.grid(row=7, column=0, columnspan=2,
                            sticky=tk.N+tk.S+tk.E+tk.W, padx=10, pady=6)

    def button_func(self):
        self.wikipedia_labels()
        # Clear data
        self.wiki = {}

        # Get input fields
        pw = self.primary_word.get()
        sw = self.secondary_word.get()

        # Check if any field is empty
        if(pw == '' or sw == ''):
            self.update_gui_message(
                'Primary and secondary keyword must be provided.')
            return

        # Inform user that the program is goign to query wikipedia
        self.update_gui_message('Searching...')

        # Query wikipedia and store results
        self.wiki = wikiAPI.get_paragraph(pw, sw)
        if(self.wiki == {}):
            # Disregard second word if no results
            print("Bad search, using only first word")
            sw = self.primary_word.get()
            self.wiki = wikiAPI.get_paragraph(pw, sw)

        # Output results
        if(self.wiki == {}):
            self.update_gui_message('Search yields no results.')
        else:
            # Add words to the dictionary
            self.wiki.update({'words': [pw, sw]})
            self.update_gui_message(self.wiki['url'], self.wiki['content'])

    def btn_output(self):
        # Check if there exists data to be output
        if(self.wiki == {}):
            self.update_gui_message('Nothing to output.')
        else:
            # Output file
            file_manager.create_output_file(
                self.wiki['words'], self.wiki['content'])
            # Exit program
            self.p.terminate()
            exit()

    def get_lucky_btn(self):
        self.wiki = {}
        print("Sending a requesting for toy categories to Life Generator...")
        self.request.put(1)

        words = (self.receive.get())
        print("Words received: ", words, "\n")

        self.input_pw.delete(0, END)
        self.input_pw.insert(INSERT, words[0])
        self.input_sw.delete(0, END)
        self.input_sw.insert(INSERT, words[1])

    def update_gui_message(self, url_field, content_field=''):
        # Check if the second argument was supplied
        if(content_field == ''):
            content_field = url_field

        # Clear both fields
        self.url_t.delete('1.0', END)
        self.content_t.delete('1.0', END)

        # Insert new data
        self.url_t.insert(INSERT, url_field)
        self.content_t.insert(INSERT, content_field)

        # Update the gui
        self.update()
