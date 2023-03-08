# !/usr/bin/env python3
# *************************************************************
# import packages
import tkinter
import tkinter.ttk
from builtins import int, tuple
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from fuzzywuzzy import fuzz
from stemming.porter2 import stem
import xlwt
import networkx as nx
from rdflib import URIRef
from rdflib.namespace import RDFS
import rdflib
from pyvis.network import Network
import re
from owlready2 import *
#import owlready2
#from owlready2 import pellet
owlready2.JAVA_EXE = "C:/path/to/java.exe"
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
import pickle


# *************************************************************
class NodeType_concept:
    def __init__(self, concept_name, concept_axioms, super_concept_axioms, concept_color, previous_concept_color,
                 concept_origin, concept_note, concept_color_listmark):
        self.concept_name = concept_name
        self.concept_axioms = concept_axioms
        self.concept_color = concept_color
        self.concept_origin = concept_origin
        self.super_concept_axioms = super_concept_axioms
        self.concept_note = concept_note
        self.concept_color_listmark = concept_color_listmark
        self.previous_concept_color = previous_concept_color

    def set_concept_name(self, name):
        self.concept_name = name

    def set_concept_axioms(self, axioms):
        self.concept_axioms = axioms

    def set_super_concept_axioms(self, axioms):
        self.super_concept_axioms = axioms

    def set_concept_color(self, color):
        self.concept_color = color

    def set_concept_origin(self, origin):
        self.concept_origin = origin

    def set_concept_note(self, note):
        self.concept_note = note

    def set_concept_color_listmark(self, color):
        self.concept_color_listmark = color

    def set_previous_concpet_color(self, p):
        self.previous_concept_color = p

    def get_concept_name(self):
        return self.concept_name

    def get_concept_axioms(self):
        return self.concept_axioms

    def get_super_concept_axioms(self):
        return self.super_concept_axioms

    def get_concept_color(self):
        return self.concept_color

    def get_concept_origin(self):
        return self.concept_origin

    def get_concept_note(self):
        return self.concept_note

    def get_concept_color_listmark(self):
        return self.concept_color_listmark

    def get_previous_concpet_color(self):
        return self.previous_concept_color


class NodeType_phrase:
    def __init__(self, phrase_name, topics_name_phrase_in, phrase_refinedf, ext_concepts, phrase_color, phrase_note,
                 phrase_relatedc, phrase_listmark_color, validation_label):
        self.phrase_name = phrase_name
        self.topics_name_phrase_in = topics_name_phrase_in
        self.phrase_refinedf = phrase_refinedf
        self.ext_concepts = ext_concepts
        self.phrase_color = phrase_color
        self.phrase_note = phrase_note
        self.phrase_relatedc = phrase_relatedc
        self.phrase_listmark_color = phrase_listmark_color
        self.validation_label = validation_label

    def set_phrase_name(self, name):
        self.phrase_name = name

    def set_topics_name_phrase_in(self, name):
        self.topics_name_phrase_in = name

    def set_phrase_refinedf(self, r):
        self.phrase_refinedf = r

    def set_ext_concepts(self, ext):
        self.ext_concepts = ext

    def set_phrase_color(self, c):
        self.phrase_color = c

    def set_phrase_note(self, n):
        self.phrase_note = n

    def set_phrase_related_concepts(self, c):
        self.phrase_relatedc = c

    def set_phrase_listmark_color(self, p):
        self.phrase_listmark_color = p

    def set_validation_label(self, v):
        self.validation_label = v

    def get_phrase_name(self):
        return self.phrase_name

    def get_topics_name_phrase_in(self):
        return self.topics_name_phrase_in

    def get_phrase_refinedf(self):
        return self.phrase_refinedf

    def get_ext_concepts(self):
        return self.ext_concepts

    def get_phrase_color(self):
        return self.phrase_color

    def get_phrase_note(self):
        return self.phrase_note

    def get_phrase_note(self):
        return self.phrase_note

    def get_phrase_related_concepts(self):
        return self.phrase_relatedc

    def get_phrase_listmark_color(self):
        return self.phrase_listmark_color

    def get_validation_label(self):
        return self.validation_label


class NodeType_Topic_Labeling:
    def __init__(self, origin_topic, topic_label, representative_phrases, comments):
        self.origin_topic = origin_topic
        self.topic_label = topic_label
        self.representative_phrases = representative_phrases
        self.comments = comments

    def set_origin_topic(self, origin_topic):
        self.origin_topic = origin_topic

    def set_topic_representative_phrases(self, topic_label):
        self.topic_label = topic_label

    def set_list_selected_phrases(self, representative_phrases):
        self.representative_phrases = representative_phrases

    def set_comment(self, c):
        self.comments = c

    def get_origin_topic(self):
        return self.origin_topic

    def get_topic_label(self):
        return self.topic_label

    def get_representative_phrases(self):
        return self.representative_phrases

    def get_comment(self):
        return self.comments


class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = root.winfo_pointerx() + 20
        y = root.winfo_pointery()  # + 10
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT, background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError  # , "cannot use pack with this widget"

    def place(self, **kw):
        raise TclError  # , "cannot use place with this widget"
# *************************************************************
# Related to find in the menu bar
def check(e):
    typed = search.get()
    if typed == '':
        data = phrases
    else:
        data = []
        for item in phrases:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


def update(data):
    listbox_search.delete(0, END)
    for item in data:
        listbox_search.insert(END, item)


def search_click_phrases(e):
    try:
        curselection = listbox_search.curselection()[0]
        search.delete(0, END)
        search.insert(0, listbox_search.get(curselection))
        clear_searched_phrase()
        s = listbox_search.get(curselection)
        i = phrases.index(s)
        listbox1.see(i)
        listbox1.itemconfig(i, {'bg': 'lightBlue1'})
        global index_searched
        index_searched = i
        notebook_main.select(higher_view_phrase_window)
    except:
        pass


def fillout(e):
    search.delete(0, END)
    search.insert(0, listbox_search.get(ACTIVE))


def find_window(e=None):
    def find_phrases():
        global index_searched
        if index_searched != -1:
            try:
                listbox1.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass
            try:
                listbox1_concept_names.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass
        global findwindow
        x = findwindow.winfo_x()
        y = findwindow.winfo_y()
        findwindow.destroy()
        findwindow = Toplevel(root)
        findwindow.title("Find")
        t = "500x300+" + str(x) + "+" + str(y)
        findwindow.geometry(t)
        findwindow.configure(background='white')
        # findwindow.resizable(0, 0)
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        findwindow.wm_iconphoto(False, photo)
        frame1 = Frame(findwindow)
        global find_var
        find_var.set(find_var.get())
        b_phrase = Radiobutton(frame1, text="Find in Phrases", variable=find_var, value=0,command=lambda: find_phrases(), bg='white')
        b_phrase.grid(row=1, column=1)
        b_concept = Radiobutton(frame1, text="Find in Concepts", variable=find_var, value=1,command=lambda: find_concepts(), bg='white')
        b_concept.grid(row=1, column=2)
        b_axiom = Radiobutton(frame1, text="Find in Axioms", variable=find_var, value=2, command=lambda: find_axioms(),bg='white')
        b_axiom.grid(row=1, column=3)
        frame1.pack(pady=20)
        global search
        search = Entry(findwindow, font=("Helvetica", 11), borderwidth=0, highlightthickness=0)
        search.pack(pady=10)
        search.focus()
        frame2 = Frame(findwindow)
        global listbox_search
        listbox_search = Listbox(frame2, width=50, borderwidth=0, highlightthickness=0)
        scrollbary_listbox_search = AutoScrollbar(frame2, command=scroll_view(listbox_search))
        listbox_search.config(yscrollcommand=scrollbary_listbox_search.set)
        scrollbary_listbox_search.config(command=listbox_search.yview)
        listbox_search.grid(row=1, column=1)
        scrollbary_listbox_search.grid(row=1, column=2, sticky="ns")
        frame2.pack(pady=10)
        update(phrases)
        search.bind("<KeyRelease>", check)
        findwindow.bind("<Destroy>", clear_search_flag)
        listbox_search.bind("<<ListboxSelect>>", search_click_phrases)
        global flag_find_window
        flag_find_window = 1
        findwindow.lift()
    def find_concepts():
        global findwindow
        global index_searched
        if index_searched != -1:
            try:
                listbox1.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass
            try:
                listbox1_concept_names.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass
        def check_concepts_2(e):
            typed = search.get()
            if typed == '':
                data = main_concept_names
            else:
                data = []
                for item in main_concept_names:
                    if typed.lower() in item.lower():
                        data.append(item)
            update(data)

        x = findwindow.winfo_x()
        y = findwindow.winfo_y()
        findwindow.destroy()
        findwindow = Toplevel(root)
        findwindow.title("Find...")
        t = "500x300+" + str(x) + "+" + str(y)
        findwindow.geometry(t)
        findwindow.configure(background='white')
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        findwindow.wm_iconphoto(False, photo)
        frame1 = Frame(findwindow)
        global find_var
        find_var.set(find_var.get())
        b_phrase = Radiobutton(frame1, text="Find in Phrases", variable=find_var, value=0,
                               command=lambda: find_phrases(), bg='white')
        b_phrase.grid(row=1, column=1)
        b_concept = Radiobutton(frame1, text="Find in Concepts", variable=find_var, value=1,
                                command=lambda: find_concepts(), bg='white')
        b_concept.grid(row=1, column=2)
        b_axiom = Radiobutton(frame1, text="Find in Axioms", variable=find_var, value=2, command=lambda: find_axioms(),
                              bg='white')
        b_axiom.grid(row=1, column=3)
        frame1.pack(pady=20)
        global search
        search = Entry(findwindow, font=("Helvetica", 11), borderwidth=0, highlightthickness=0)
        search.pack(pady=10)
        search.focus()
        global listbox_search
        frame2 = Frame(findwindow)
        listbox_search = Listbox(frame2, width=50, borderwidth=0, highlightthickness=0)
        scrollbary_listbox_search = AutoScrollbar(frame2, command=scroll_view(listbox_search))
        listbox_search.config(yscrollcommand=scrollbary_listbox_search.set)
        scrollbary_listbox_search.config(command=listbox_search.yview)
        listbox_search.grid(row=1, column=1)
        scrollbary_listbox_search.grid(row=1, column=2, sticky="ns")
        frame2.pack(pady=10)
        update(main_concept_names)
        search.bind("<KeyRelease>", check_concepts_2)
        findwindow.bind("<Destroy>", clear_search_flag)
        listbox_search.bind("<<ListboxSelect>>", search_click_concepts)
        global flag_find_window
        flag_find_window = 1
        findwindow.lift()
    def find_axioms():
        global index_searched
        if index_searched != -1:
            try:
                listbox1.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass
            try:
                listbox1_concept_names.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass
        clear_search_flag()
        global findwindow

        def check_axioms(e):
            typed = search.get()
            if typed == '':
                data = complete_relations_edge
            else:
                data = []
                for item in sub_concepts:
                    if typed.lower() in item.lower():
                        i = sub_concepts.index(item)
                        if complete_relations_edge[i] not in data:
                            data.append(complete_relations_edge[i])
                for item in super_concepts:
                    if typed.lower() in item.lower():
                        i = super_concepts.index(item)
                        if complete_relations_edge[i] not in data:
                            data.append(complete_relations_edge[i])
            update(data)

        x = findwindow.winfo_x()
        y = findwindow.winfo_y()
        findwindow.destroy()
        findwindow = Toplevel(root)
        findwindow.title("Find...")
        t = "500x300+" + str(x) + "+" + str(y)
        findwindow.geometry(t)
        findwindow.configure(background='white')
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        findwindow.wm_iconphoto(False, photo)
        frame1 = Frame(findwindow)
        global find_var
        find_var.set(find_var.get())
        b_phrase = Radiobutton(frame1, text="Find in Phrases", variable=find_var, value=0,
                               command=lambda: find_phrases(), bg='white')
        b_phrase.grid(row=1, column=1)
        b_concept = Radiobutton(frame1, text="Find in Concepts", variable=find_var, value=1,
                                command=lambda: find_concepts(), bg='white')
        b_concept.grid(row=1, column=2)
        b_axiom = Radiobutton(frame1, text="Find in Axioms", variable=find_var, value=2, command=lambda: find_axioms(),
                              bg='white')
        b_axiom.grid(row=1, column=3)
        frame1.pack(pady=20)
        global search
        search = Entry(findwindow, font=("Helvetica", 11), borderwidth=0, highlightthickness=0)
        search.pack(pady=10)
        search.focus()
        search.config(width=0)
        frame2 = Frame(findwindow)
        global listbox_search
        listbox_search = Listbox(frame2, width=50, borderwidth=0, highlightthickness=0)
        scrollbary_listbox_search = AutoScrollbar(frame2, command=scroll_view(listbox_search))
        listbox_search.config(yscrollcommand=scrollbary_listbox_search.set)

        scrollbary_listbox_search.config(command=listbox_search.yview)
        listbox_search.grid(row=1, column=1)
        scrollbary_listbox_search.grid(row=1, column=2, sticky="ns")
        frame2.pack(pady=10)
        # save all defined axioms of ontology
        complete_relations_edge = []
        sub_concepts = []
        super_concepts = []
        for r in relations_edge:
            sub_concepts.append(r[0])
            super_concepts.append(r[1])
            t = r[0] + "   is-a   " + r[1]
            complete_relations_edge.append(t)
        update(complete_relations_edge)
        listbox_search.bind("<<ListboxSelect>>", fillout)
        search.bind("<KeyRelease>", check_axioms)
        findwindow.bind("<Destroy>", clear_search_flag)
        global flag_find_window
        flag_find_window = 1
        findwindow.lift()
    def clear_search_flag(e=None):
        global flag_find_window
        flag_find_window = 0
        global index_searched
        global find_var
        x = find_var.get()
        if x == 0 and index_searched != -1:
            try:
                listbox1.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass
        if x == 1 and index_searched != -1:
            try:
                listbox1_concept_names.itemconfig(index_searched, {'bg': 'white'})
            except:
                pass

    global findwindow
    global flag_find_window
    if flag_find_window == 0:
        flag_find_window = 1
        global findwindow
        findwindow = Toplevel(root)
        findwindow.title("Find...")
        #findwindow.geometry("500x300+500+200")
        findwindow.geometry('')
        findwindow.resizable(0, 0)
        findwindow.configure(background='white')
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        findwindow.wm_iconphoto(False, photo)
        frame1 = Frame(findwindow)
        global find_var
        find_var.set(find_var.get())
        b_phrase = Radiobutton(frame1, text="Find in Phrases", variable=find_var, value=0,
                               command=lambda: find_phrases(), bg='white')
        b_phrase.grid(row=1, column=1)
        b_concept = Radiobutton(frame1, text="Find in Concepts", variable=find_var, value=1,
                                command=lambda: find_concepts(), bg='white')
        b_concept.grid(row=1, column=2)
        b_axiom = Radiobutton(frame1, text="Find in Axioms", variable=find_var, value=2, command=lambda: find_axioms(),
                              bg='white')
        b_axiom.grid(row=1, column=3)
        frame1.pack(pady=20)
        x = find_var.get()
        if x == -1:
            global search
            search = Entry(findwindow, font=("Helvetica", 11), borderwidth=0, highlightthickness=0)
            search.pack(pady=10)
            search.focus()
            global listbox_search
            listbox_search = Listbox(findwindow, width=50, borderwidth=0, highlightthickness=0)
            listbox_search.pack(pady=10)
            findwindow.bind("<Destroy>", clear_search_flag)
            findwindow.lift()
        if x == 0:
            find_phrases()
        if x == 1:
            find_concepts()
        if x == 2:
            find_axioms()
    else:
        findwindow.lift()


def exit_program():
    sys.exit(0)


# Related to load ontology
def load_ontology():
    owl_files = filedialog.askopenfilenames(title="Select OWL files to load", filetypes=(("OWL Files", "*.owl"),))
    root.update()
    paths = root.tk.splitlist(owl_files)
    read_owl(paths)


def read_owl(paths):
    if paths:
        restart_new_ontology()
        global ontology_help_owl
        ontology_help_owl = paths[0]
        global ontology_loaded_label
        global ontology_loaded_path
        ontology_loaded_path.config(state="normal")
        ontology_loaded_label.config(text="")
        ontology_loaded_path.delete('1.0', END)
        ontology_loaded_path_values.clear()
        count = 0
        for path in paths:
            path = str(path)
            print(path)
            origin_path = path.split('/')[-1]
            g = rdflib.Graph()
            g.parse(path, format='xml')
            graph_ontology.parse(path, format='xml')
            query = """
            select ?class
            where {?class a owl:Class}
                    """
            result = g.query(query)
            for i in result:
                s = str(i)
                if "rdflib.term.URIRef" in s:
                    j = re.findall("'(.*?)'", s)[0]
                    x = j.rsplit('/', 1)[-1]
                    y = str(x.rsplit('#')[-1])
                    if y not in main_concept_names:
                        if count == 0:
                            main_concept_names.append(y)
                            x = NodeType_concept(y, [], [], 'black', 'black', origin_path, ' ', '')
                            size = len(main_concepts)
                            if size > 0:
                                main_concepts[0] = x
                            else:
                                main_concepts.append(x)
                            count += 1
                        else:
                            main_concept_names.append(y)
                            x = NodeType_concept(y, [], [], 'black', 'black', origin_path, ' ', '')
                            main_concepts.append(x)
            for subj, obj in g.subject_objects(predicate=RDFS.subClassOf):
                if type(subj) == URIRef and type(obj) == URIRef:
                    print(subj.rsplit('/')[-1], "======", obj.rsplit('/')[-1])
                    x1 = str(subj.rsplit('/')[-1])
                    x2 = str(obj.rsplit('/')[-1])
                    y1 = str(x1.rsplit('#')[-1])
                    y2 = str(x2.rsplit('#')[-1])
                    try:
                        index = main_concept_names.index(y1)
                        temp_axioms = []
                        t = main_concepts[index].get_concept_axioms()
                        for t1 in t:
                            temp_axioms.append(t1)
                        temp_axioms.append(y2)
                        axiom_color_edge.append((y1, y2))
                        relations_edge.append((y1, y2))
                        axiom_color.append('red')
                        main_concepts[index].set_concept_axioms(temp_axioms)
                    except:
                        pass
            ontology_loaded_path.insert(END, path)
            ontology_loaded_path.insert(END, '\n')
            ontology_loaded_path_values.append(path)

        ontology_loaded_path.config(state="disabled")
        ontology_loaded_label.config(text="The ontology has been loaded successfully!", font='Helvetica 11 bold')
        length = len(main_concepts)
        for i in range(0, length):
            name = main_concepts[i].get_concept_name()
            origin = main_concepts[i].get_concept_origin()
            listbox1_concept_names.insert(END, name)
            listbox1_concept_names_only.insert(END, name)
            if origin != "main":
                listbox2_concept_origin.insert(END, origin)
                listbox2_concept_origin_only.insert(END, origin)
            else:
                listbox2_concept_origin.insert(END, " ")
                listbox2_concept_origin_only.insert(END, " ")
            listbox_mark_concepts.insert(END, " ")
            listbox_mark_concepts_only.insert(END, " ")
        listbox1_concept_names_only.selection_set(0)
        notebook_main.tab(3, state="normal")
        notebook_main.tab(4, state="normal")
        try:
            if window_concept_only:
                window_concept_axiom_focus_view.destroy()
            if window_concept_only_note_view:
                window_concept_only_note_view.destroy()
            curselection = listbox1_concept_names_only.curselection()[0]
            ph = listbox1_concept_names_only.get(curselection)
            if ph != '':
                cocenpt_only_tab1(ph)
                concept_only_info(ph)
                if previous_tab_id_concept_only == 0:
                    notebook_concepts_only.select(window_concept_only)
                else:
                    notebook_concepts_only.select(window_concept_only_note_view)
        except:
            pass
        listbox1_concept_names.selection_set(0)
        try:
            if window_concept_axiom_focus_view:
                window_concept_axiom_focus_view.destroy()
            if window_concept_note_view:
                window_concept_note_view.destroy()
            curselection = listbox1_concept_names.curselection()[0]
            concept_name.config(text=listbox1_concept_names.get(curselection))
            ph = concept_name.cget("text")
            if ph != '':
                index = main_concept_names.index(ph)
                concept_origin.config(text=main_concepts[index].get_concept_origin())
                concept_tab_axiom_view(ph)
                concept_note(ph)
                if previous_tab_id_concept == 0:
                    notebook_concepts.select(window_concept_axiom_view)
                elif previous_tab_id_concept == 1:
                    notebook_concepts.select(window_concept_note_view)
        except:
            pass


def yview_concept_view(*args):
    """ scroll both listboxes together """
    listbox1_concept_names.yview(*args)
    listbox2_concept_origin.yview(*args)
    listbox_mark_concepts.yview(*args)


def OnMouseWheel_concept_view(event):
    listbox1_concept_names.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox2_concept_origin.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox_mark_concepts.yview_scroll(-1 * int(event.delta / 120), "units")
    return "break"


def click_on_concept(e):
    try:
        if window_concept_axiom_focus_view:
            window_concept_axiom_focus_view.destroy()
        if window_concept_note_view:
            window_concept_note_view.destroy()
        curselection = listbox1_concept_names.curselection()[0]
        concept_name.config(text=listbox1_concept_names.get(curselection))
        ph = concept_name.cget("text")
        if ph != '':
            index = main_concept_names.index(ph)
            concept_origin.config(text=main_concepts[index].get_concept_origin())
            concept_tab_axiom_view(ph)
            concept_note(ph)
            if previous_tab_id_concept == 0:
                notebook_concepts.select(window_concept_axiom_view)
            elif previous_tab_id_concept == 1:
                notebook_concepts.select(window_concept_note_view)
    except:
        pass


def save_concept_note(note, ph):
    index = main_concept_names.index(ph)
    global main_concepts
    x = main_concepts[index]
    x.set_concept_note(note)
    main_concepts[index] = x
    info_window("The note has been saved!", "Info", 2000)


def save_concept_note_bind(e, note, ph):
    index = main_concept_names.index(ph)
    global main_concepts
    x = main_concepts[index]
    x.set_concept_note(note)
    main_concepts[index] = x
    info_window("The note has been saved!", "Info", 2000)


def mark_concept(e):
    try:
        curselection = listbox_mark_concepts.curselection()
        index = curselection[0]
        bg_color = listbox_mark_concepts.itemcget(index, "background")
        if bg_color == 'red':
            listbox_mark_concepts.itemconfig(index, {'bg': 'white'})
            listbox_mark_concepts.selection_clear(0, END)
            listbox_mark_concepts_only.itemconfig(index, {'bg': 'white'})
            listbox_mark_concepts_only.selection_clear(0, END)
        else:
            listbox_mark_concepts.itemconfig(index, {'bg': 'red'})
            listbox_mark_concepts.selection_clear(0, END)
            listbox_mark_concepts_only.itemconfig(index, {'bg': 'darkred'})
            listbox_mark_concepts_only.selection_clear(0, END)
    except:
        return None


def my_popup_listbox1_concept_view(e):
    currentselection = listbox1_concept_names.curselection()[0]
    selection = listbox1_concept_names.get(listbox1_concept_names.curselection()[0])
    if selection:
        x_position = e.widget.winfo_rootx()
        y_position = e.widget.winfo_rooty()
        itemx, itemy, itemwidth, itemheight = e.widget.bbox(currentselection)
        listbox_mark_concepts_menu.tk_popup(x_position + e.widget.winfo_width() - 10, y_position + itemy + 10)


def info_window_2(message, title, time, xposition, yposition):
    window = Toplevel(root)
    window.title(title)
    s = "+" + str(xposition) + "+" + str(yposition)
    window.geometry(s)
    window.configure(background='white')
    window.resizable(0, 0)
    ico = Image.open('p2o.png')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)
    my_label = Label(window, text=message, bg='white', font='Helvetica 9 bold')
    my_label.pack()
    if time != -1:
        window.after(time, window.destroy)


def mark_concept_done():
    concept_name.config(text=listbox1_concept_names.get(ANCHOR))
    ph = concept_name.cget("text")
    if ph != '':
        i = main_concept_names.index(ph)
        if main_concepts[i].get_concept_color() != 'green':
            main_concepts[i].set_previous_concpet_color(main_concepts[i].get_concept_color())
            main_concepts[i].set_concept_color('green')
            listbox1_concept_names.itemconfig(i, fg='green')


def unmark_concept_done():
    concept_name.config(text=listbox1_concept_names.get(ANCHOR))
    ph = concept_name.cget("text")
    if (ph != ''):
        i = main_concept_names.index(ph)
        previous_color = main_concepts[i].get_previous_concpet_color()
        main_concepts[i].set_concept_color(previous_color)
        listbox1_concept_names.itemconfig(i, fg=previous_color)


def yview_main(*args):
    """ scroll both listboxes together """
    listbox1.yview(*args)
    listbox2.yview(*args)


def scroll_view(listbox, *args):
    listbox.yview(*args)


def OnMouseWheel(listbox, *args):
    listbox.yview_scroll(-1 * int(*args.delta / 120), "units")
    return "break"


def OnMouseWheel(event):
    listbox1.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox2.yview_scroll(-1 * int(event.delta / 120), "units")
    return "break"


def yview_main_topics_phrases(*args):
    """ scroll both listboxes together """
    listbox1_topics_phrases.yview(*args)
    listbox2_topics_phrases.yview(*args)


def OnMouseWheel_topics_phrases(event):
    listbox1_topics_phrases.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox2_topics_phrases.yview_scroll(-1 * int(event.delta / 120), "units")
    return "break"


def click_on_phrase(e):
    try:
        curselection = listbox1.curselection()[0]
        p1.config(text=listbox1.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            add_meta_data_tab(ph)
            matching_tab(ph)
            add_note_phrase(ph)
            if previous_tab_id == 0:
                notebook_phrases.select(window_phrase_add_metadata_view)
            else:
                if previous_tab_id == 1:
                    notebook_phrases.select(window_phrase_matching_view)
                else:
                    notebook_phrases.select(window_phrase_note_view)
    except:
        pass


def add_note_phrase(ph):
    i = phrases.index(ph)
    global window_phrase_note_view
    if window_phrase_note_view:
        window_phrase_note_view.destroy()
        window_phrase_note_view = Frame(notebook_phrases, bg="white")  # , width=950, height=450
    Frame_note = Frame(window_phrase_note_view, borderwidth=1, bg='azure')
    Frame_note_temp = Frame(window_phrase_note_view, borderwidth=0, bg='azure')
    textbox_note = Text(Frame_note_temp, width=100, height=20, undo=True, borderwidth=0, bg='azure',font=('comicsans bold', 12))
    scrollbary_textbox_note = Scrollbar(Frame_note_temp, command=textbox_note.yview)
    textbox_note.config(yscrollcommand=scrollbary_textbox_note.set)
    textbox_note.pack(side="left", fill=Y, expand=False)
    scrollbary_textbox_note.pack(side="right", fill=Y, expand=False)
    Frame_note_temp.pack(fill='both', expand=True)
    b = Button(Frame_note, text="Save Note", width=15, height=2, fg='black', bg='lightBlue1', font=('comicsans', 12),
               command=lambda: save_phrase_note((textbox_note.get("1.0", END)[:-1]), ph))
    b.pack(padx=10, pady=20, anchor=W)
    Frame_note.pack(fill='both', expand=True)
    notebook_phrases.add(window_phrase_note_view, text="Add note to selected phrase")
    textbox_note.insert('1.0', all_phrases[i].get_phrase_note())


def click_on_listbox_concepts_metadata(e, listboxname):
    try:
        if window_concept_axiom_focus_view:
            window_concept_axiom_focus_view.destroy()
        curselection = listboxname.curselection()[0]
        listbox1_concept_names.selection_clear(0, END)
        concept_name.config(text=listboxname.get(curselection))
        ph = concept_name.cget("text")
        if ph != '':
            index = main_concept_names.index(ph)
            listbox1_concept_names.see(index)
            listbox1_concept_names.selection_set(index)
            concept_origin.config(text=listbox2_concept_origin.get(index))
            concept_tab_axiom_view(ph)
            concept_note(ph)
            notebook_main.select(higher_view_concept_window)
            if previous_tab_id_concept == 0:
                notebook_concepts.select(window_concept_axiom_view)
            elif previous_tab_id_concept == 1:
                notebook_concepts.select(window_concept_note_view)
    except:
        pass


def add_meta_data_tab(ph):
    def fillout_3(e):
        search_3.delete(0, END)
        try:
            curselection = listbox_search_3.curselection()
            index = curselection[0]
            ph = listbox_search_3.get(index)
            search_3.insert(0, ph)
        except:
            pass

    def check_3(e):
        typed = search_3.get()
        if typed == '':
            data = main_concept_names
        else:
            data = []
            for item in main_concept_names:
                if typed.lower() in item.lower():
                    data.append(item)
        update_3(data)

    def update_3(data):
        listbox_search_3.delete(0, END)
        listbox_search_3.insert(END, *data)

    def exist_m_relate_concept(phrase, related_concept):
        index = phrases.index(phrase)
        value_list = ['', ' ', 'EXIST', 'EXIST-m', 'EXIST or EXIST-m']
        validation_label = all_phrases[i].get_validation_label()
        if (validation_label in value_list):
            if related_concept in main_concept_names:
                assigned_concepts.config(fg='navy')
                all_phrases[index].set_validation_label("EXIST or EXIST-m")
                listbox2.delete(index)
                listbox2.insert(index, all_phrases[i].get_validation_label())
                index = phrases.index(phrase)
                if (related_concept not in all_phrases[index].get_phrase_related_concepts()):
                    listbox_related_concepts.insert(END, related_concept)
                    listbox_related_concepts.itemconfig(END, bg='lightcyan')
                    related_concepts_list = all_phrases[index].get_phrase_related_concepts()
                    if related_concepts_list == '' or related_concepts_list == " ":
                        related_concepts_list = []
                    related_concepts_list.append(related_concept)
                    all_phrases[index].set_phrase_related_concepts(related_concepts_list)
                    search_3.delete(0, END)
                else:
                    info_window("This concept is already assigned to the selected phrase.", "Error", 3000)
                    search_3.delete(0, END)
            else:
                info_window("There is not such concept! Please enter the correct concept name.", "Error", 3000)
                search_3.delete(0, END)
        else:
            info_window("The concept cannot be related to the phrase", "Error", 3000)
            search_3.delete(0, END)

    def use_of_phrase_ityself():
        textbox2.delete("1.0", END)
        ph_temp = ph.strip()
        if concept_name_style_var.get() == 1:
            ph_temp = camelcase_concept_name(ph_temp)
        textbox2.insert(END, ph_temp)
        textbox2.config(state="disabled")

    def use_of_other_form_of_phrase():
        textbox2.config(state="normal")
        textbox2.delete("1.0", END)
        ph_temp = ph.strip()
        if concept_name_style_var.get() == 1:
            ph_temp = camelcase_concept_name(ph_temp)
        textbox2.insert(END, ph_temp)
        textbox2.focus_set()

    def on_enter_listbox(e):
        index = listbox_search_3.index("@%s,%s" % (e.x, e.y))
        if index >= 0:
            toolTip.showtip(listbox_search_3.get(index))
            global element_display_popup
            element_display_popup = index

    def on_leave_listbox(e):
        toolTip.hidetip()
        global element_display_popup
        element_display_popup = -1

    def on_motion_listbox(e):
        global element_display_popup
        index = listbox_search_3.index("@%s,%s" % (e.x, e.y))
        if index >= 0:
            if index != element_display_popup:
                toolTip.hidetip()
                element_display_popup = index
                toolTip.showtip(listbox_search_3.get(index))

    def OnKeyPress_textbox2(e):
        global state_add_concpet_var
        if state_add_concpet_var.get() != 1 and state_add_concpet_var.get() != 0:
            state_add_concpet_var.set(1)
            refined_button1 = Radiobutton(Frame12, text="Use the phrase itself", variable=state_add_concpet_var,value=0,command=use_of_phrase_ityself, bg='whitesmoke')
            refined_button1.grid(row=0, column=1, sticky='W')
            refined_button2 = Radiobutton(Frame12, text="Define new form of the phrase", variable=state_add_concpet_var,value=1, command=use_of_other_form_of_phrase, bg='whitesmoke')
            refined_button2.grid(row=1, column=1, sticky='W')

    global notebook_phrases
    global window_phrase_add_metadata_view
    if window_phrase_add_metadata_view:
        window_phrase_add_metadata_view.destroy()
        window_phrase_add_metadata_view = Frame(notebook_phrases, bg="white")  # width=950, height=450,
    i = phrases.index(ph)
    frame_main_1 = Frame(window_phrase_add_metadata_view, borderwidth=0, highlightthickness=0, bg='whitesmoke')
    Frame12 = Frame(frame_main_1, borderwidth=1, bg='whitesmoke')
    global state_add_concpet_var
    state_add_concpet_var.set(-1)
    refined_button1 = Radiobutton(Frame12, text="Use the phrase itself", variable=state_add_concpet_var, value=0,
                                  command=use_of_phrase_ityself, bg='whitesmoke')
    refined_button1.grid(row=0, column=1, sticky='W')
    refined_button2 = Radiobutton(Frame12, text="Define new form of the phrase", variable=state_add_concpet_var,
                                  value=1, command=use_of_other_form_of_phrase, bg='whitesmoke')
    refined_button2.grid(row=1, column=1, sticky='W')
    state_add_concpet_var.set(-1)
    global textbox2
    textbox2 = Text(Frame12, width=35, height=2, undo=True, borderwidth=2)
    textbox2.bind("<KeyRelease>", OnKeyPress_textbox2)
    textbox2.grid(row=3, column=1, sticky='w', padx=5)
    Button12 = Button(Frame12, text="Add to concepts", width=12, fg='black', bg='lightBlue1', font=('comicsans', 11),
                      command=lambda: add_to_concepts((textbox2.get("1.0", END)[:-1]), ph, state_add_concpet_var.get()))
    Button12.grid(row=3, column=2, padx=10)
    Frame12.grid(row=0, column=0, sticky='e', padx=5, pady=5)
    Frame15 = Frame(frame_main_1, borderwidth=1, bg='whitesmoke')
    Label(Frame15, text="Extracted Concepts from Phrase", bg='whitesmoke', font='Helvetica 10 bold', fg='navy').grid(
        row=1, column=1)
    global listbox_concepts_metadata
    listbox_concepts_metadata = Listbox(Frame15, width=40, height=5)
    listbox_concepts_metadata.grid(row=2, column=1)
    scrollbary_listbox_concepts_metadata = AutoScrollbar(Frame15, command=scroll_view(listbox_concepts_metadata))
    listbox_concepts_metadata.config(yscrollcommand=scrollbary_listbox_concepts_metadata.set)
    scrollbary_listbox_concepts_metadata.grid(row=2, column=2, sticky="ns")
    r = all_phrases[i].get_ext_concepts()
    if r:
        listbox_concepts_metadata.insert(END, *r)
    listbox_concepts_metadata.bind("<<ListboxSelect>>",
                                   lambda e: click_on_listbox_concepts_metadata(e, listbox_concepts_metadata))
    Frame15.grid(row=0, column=1, sticky='w', padx=5, pady=5)
    frame_main_1.grid(row=0, column=0, padx=15, pady=30)
    Frame14 = Frame(window_phrase_add_metadata_view, borderwidth=1, bg='whitesmoke')
    label1 = Label(Frame14, text='Relate Concepts to Phrase', bg='whitesmoke', font='Helvetica 10 bold', fg='navy')
    label1.grid(row=0, column=1, padx=10, pady=5)
    search_3 = Entry(Frame14, font=("Helvetica", 11), borderwidth=2, width=30)
    search_3.grid(row=1, column=1, padx=10)
    global listbox_search_3
    listbox_search_3 = Listbox(Frame14, width=40, height=7, borderwidth=0, highlightthickness=0, bg='whitesmoke')
    listbox_search_3.grid(row=2, column=1, padx=10, pady=5)
    update_3(main_concept_names)
    listbox_search_3.bind("<<ListboxSelect>>", fillout_3)
    listbox_search_3.bind('<FocusOut>', lambda e: listbox_search_3.selection_clear(0, END))
    search_3.bind("<KeyRelease>", check_3)
    scrollbary_listbox_search_3 = AutoScrollbar(Frame14, command=scroll_view(listbox_search_3))
    scrollbary_listbox_search_3.configure(command=listbox_search_3.yview)
    listbox_search_3.config(yscrollcommand=scrollbary_listbox_search_3.set)
    scrollbary_listbox_search_3.grid(row=2, column=2, sticky="ns")
    element_display_popup = -1
    listbox_search_3.bind("<Enter>", on_enter_listbox)
    listbox_search_3.bind("<Leave>", on_leave_listbox)
    listbox_search_3.bind("<Motion>", on_motion_listbox)
    global assigned_concepts
    assigned_concepts = Label(Frame14, text='Related Concepts to Phrase', bg='whitesmoke', font='Helvetica 9 bold',
                              borderwidth=0, highlightthickness=0, fg='whitesmoke')
    assigned_concepts.grid(row=3, column=1, padx=10, pady=10)
    Button16 = Button(Frame14, text="Assign", width=7, height=2, fg='black', bg='lightBlue1', font=('comicsans', 11),
                      command=lambda: exist_m_relate_concept(ph, search_3.get()))
    Button16.grid(row=2, column=3, padx=5, pady=5, sticky='n')
    listbox_related_concepts = Listbox(Frame14, width=40, height=3, borderwidth=0, highlightthickness=0,
                                       bg='whitesmoke')
    listbox_related_concepts.bind("<MouseWheel>",
                                  lambda event: OnMouseWheel_function(e=event, listname=listbox_related_concepts))
    listbox_related_concepts.grid(row=4, column=1, padx=10)
    scrollbary_listbox_related_concepts = AutoScrollbar(Frame14, command=scroll_view(listbox_related_concepts))
    listbox_related_concepts.config(yscrollcommand=scrollbary_listbox_related_concepts.set)
    listbox_related_concepts.config(yscrollcommand=scrollbary_listbox_related_concepts.set)
    scrollbary_listbox_related_concepts.grid(row=4, column=2, sticky="ns")
    rc = all_phrases[i].get_phrase_related_concepts()
    if rc and rc != '' and rc != " ":
        assigned_concepts.config(fg='black')
        for item in rc:
            listbox_related_concepts.insert(END, item)
            listbox_related_concepts.itemconfig(END, bg='lightcyan')
    listbox_related_concepts.bind("<<ListboxSelect>>",
                                  lambda e: click_on_listbox_concepts_metadata(e, listbox_related_concepts))
    i = phrases.index(ph)
    Frame14.grid(row=1, column=0, sticky='w', padx=15, pady=10)
    window_phrase_add_metadata_view.pack()
    notebook_phrases.add(window_phrase_add_metadata_view, text="Define concept from selected phrase")


def refresh_meta_data_tabs_2():
    try:
        curselection = listbox1.curselection()[0]
        p1.config(text=listbox1.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            global window_concept_axiom_view
            if window_concept_axiom_view:
                window_concept_axiom_view.destroy()
            global window_concept_note_view
            if window_concept_note_view:
                window_concept_note_view.destroy()
            add_meta_data_tab(ph)
            add_note_phrase(ph)
    except:
        pass


def add_to_concepts(text, ph, var):
    notebook_main.tab(3, state="normal")
    notebook_main.tab(4, state="normal")
    temp = text.strip()
    temp = camelcase_concept_name(temp)
    if concept_name_style_var.get() == 1:
        text = camelcase_concept_name(text)
    if text != "" and temp != "":
        if var == 0:
            p1.config(text=ph)
            i = phrases.index(ph)
            ext_concepts = all_phrases[i].get_ext_concepts()
            if ext_concepts == '':
                ext_concepts = []
            temp_text = text
            if temp_text not in main_concept_names and temp_text not in ext_concepts:
                listbox_concepts_metadata.insert(END, temp_text)
                textbox2.config(state=NORMAL)
                textbox2.delete('1.0', END)
                state_add_concpet_var.set(None)
                ext_concepts.append(temp_text)
                all_phrases[i].set_ext_concepts(ext_concepts)
                if all_phrases[i].get_validation_label() == ('' or ' '):
                    all_phrases[i].set_validation_label('ADD')
                else:
                    temp = all_phrases[i].get_validation_label().replace('ADD-m', '')
                    if "ADD" not in temp:
                        if "ADD-m" in all_phrases[i].get_validation_label():
                            all_phrases[i].set_validation_label("ADD , " + all_phrases[i].get_validation_label())
                listbox2.delete(i)
                listbox2.insert(i, all_phrases[i].get_validation_label())
                temp_name = text
                main_concept_names.append(temp_name)
                x_concept = NodeType_concept(temp_name, [], [], 'blue', 'blue', '', ' ', '')
                main_concepts.append(x_concept)
                listbox1_concept_names.insert(END, temp_name)
                listbox_mark_concepts.insert(END, " ")
                i = listbox1_concept_names.get(0, END).index(temp_name)
                listbox1_concept_names.itemconfig(i, fg='blue')
                listbox1_concept_names_only.insert(END, temp_name)
                listbox_mark_concepts_only.insert(END, " ")
                i = listbox1_concept_names_only.get(0, END).index(temp_name)
                listbox1_concept_names_only.itemconfig(i, fg='blue')
            else:
                messagebox.showerror("Error", "The concept \"" + ph + "\" already exists in concepts!")
                textbox2.config(state=NORMAL)
                textbox2.delete('1.0', END)
                state_add_concpet_var.set(None)
        elif var == 1:
            state_add_concpet_var.set(1)
            p1.config(text=listbox1.get(ANCHOR))
            i = phrases.index(ph)
            ext_concepts = all_phrases[i].get_ext_concepts()
            if ext_concepts == '':
                ext_concepts = []
            temp_text = text
            if temp_text not in main_concept_names and temp_text not in ext_concepts:
                listbox_concepts_metadata.insert(END, temp_text)
                textbox2.config(state=NORMAL)
                textbox2.delete('1.0', END)
                state_add_concpet_var.set(None)
                ext_concepts.append(temp_text)
                all_phrases[i].set_ext_concepts(ext_concepts)
                if "ADD-m" not in all_phrases[i].get_validation_label():
                    if "ADD" not in all_phrases[i].get_validation_label():
                        temp_label = "ADD-m"
                    else:
                        temp_label = all_phrases[i].get_validation_label() + " , " + "ADD-m"
                    all_phrases[i].set_validation_label(temp_label)
                    listbox2.delete(i)
                    listbox2.insert(i, temp_label)
                temp_name = text
                main_concept_names.append(temp_name)
                x_concept = NodeType_concept(temp_name, [], [], 'purple', 'purple', ph, ' ', '')
                main_concepts.append(x_concept)
                listbox1_concept_names.insert(END, temp_name)
                listbox2_concept_origin.insert(END, ph)
                listbox_mark_concepts.insert(END, " ")
                i = listbox1_concept_names.get(0, END).index(temp_name)
                listbox1_concept_names.itemconfig(i, fg='purple')
                listbox1_concept_names_only.insert(END, temp_name)
                listbox_mark_concepts_only.insert(END, " ")
                i = listbox1_concept_names_only.get(0, END).index(temp_name)
                listbox1_concept_names_only.itemconfig(i, fg='purple')
            else:
                temp_name = text
                messagebox.showerror("Error", "The concept \"" + temp_name + "\" already exists in concepts!")
                textbox2.config(state=NORMAL)
                textbox2.delete('1.0', END)
                state_add_concpet_var.set(None)
    else:
        textbox2.delete('1.0', END)


def save_phrase_note(note, ph):
    index = phrases.index(ph)
    all_phrases[index].set_phrase_note(note)
    info_window("The note has been saved!", "Info", 2000)


def add_to_concepts_new(text, ph, var):
    if text != "":
        temp_name = text
        main_concept_names.append(temp_name)
        x_concept = NodeType_concept(temp_name, [], [], 'blue', 'blue', ph, ' ', '')
        main_concepts.append(x_concept)
        listbox1_concept_names.insert(END, temp_name)
        listbox2_concept_origin.insert(END, "")
        listbox_mark_concepts.insert(END, " ")
        i = listbox1_concept_names.get(0, END).index(temp_name)
        listbox1_concept_names.itemconfig(i, fg='blue')
        listbox2_concept_origin.itemconfig(i, fg='blue')
        refresh_meta_data_tabs_2()
    else:
        messagebox.showerror("Error", "The name of the concept is invalid!")


def refresh_meta_data_tabs():
    try:
        curselection = listbox1_concept_names.curselection()[0]
        p1.config(text=listbox1_concept_names.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            global window_concept_axiom_view
            if window_concept_axiom_view:
                window_concept_axiom_view.destroy()
            global window_concept_note_view
            if window_concept_note_view:
                window_concept_note_view.destroy()
            concept_tab_axiom_view(ph)
            concept_note(ph)
    except:
        pass


def find_relations_super_2(main_concept, super, result_relations, result_concepts, relations):
    i = main_concept_names.index(super)
    super_relations = main_concepts[i].get_concept_axioms()
    for r in super_relations:
        if r != main_concept:
            if r not in result_concepts:
                result_concepts.append(r)
            relation = super + '  is-a  ' + r
            if relation not in result_relations:
                relations.append(relation)
                t = super + ' is-a ' + r
                result_relations.append(r)
            if r:
                find_relations_super(main_concept, r, result_relations, result_concepts, relations)
    return result_relations, result_concepts, relations


def find_relations_super(main_concept, super, result_relations, result_concepts, relations):
    for r in relations_edge:
        c1 = r[0]
        c2 = r[1]
        if c2 != main_concept:
            if super == c1:
                if c1 not in result_concepts:
                    result_concepts.append(c2)
                if r not in result_relations:
                    t = c1 + '  is-a  ' + c2
                    relations.append(t)
                    result_relations.append(r)
                if c2 and (r not in result_relations):
                    find_relations_super(main_concept, c2, result_relations, result_concepts, relations)
    return result_relations, result_concepts, relations


def find_relations_sub(main_concept, sub, result_relations, result_concepts, relations):
    for r in relations_edge:
        c1 = r[0]
        c2 = r[1]
        if c1 == main_concept:
            return result_relations, result_concepts, relations
        if c2 != main_concept:
            if sub == c2:
                if c1 not in result_concepts:
                    result_concepts.append(c2)
                if r not in result_relations:
                    t = c1 + '  is-a  ' + c2
                    relations.append(t)
                    result_relations.append(r)
                if c2:
                    find_relations_sub(main_concept, c1, result_relations, result_concepts, relations)
    return result_relations, result_concepts, relations


def find_relations_sub_2(main_concept, sub, result_relations, result_concepts, relations):
    for r in relations_edge:
        c1 = r[0]
        c2 = r[1]
        if c1 != main_concept:
            if sub == c2:
                if c1 not in result_concepts:
                    result_concepts.append(c2)
                if r not in result_relations:
                    t = c1 + '  is-a  ' + c2
                    relations.append(t)
                    result_relations.append(r)
                if c2:
                    find_relations_sub(main_concept, c1, result_relations, result_concepts, relations)
    return result_relations, result_concepts, relations


def save_metadata_relation(textbox1):
    p1.config(text=listbox1_concept_names.get(ANCHOR))
    ph = p1.cget("text")
    if (ph != ''):
        index = main_concept_names.index(ph)
        list_relations = []
        try:
            length = textbox1.size()
            for i in range(0, length):
                x = textbox1.get(i)
                list_relations.append(x)
        except:
            pass
        p = ph
        rela = main_concepts[index].get_concept_axioms()
        if rela:
            for j in rela:
                if (p, j) not in relations_edge:
                    relations_edge.append((p, j))
                    axiom_color_edge.append((p, j))
                    axiom_color.append('blue')
                    network_colors.append("YES")
                    all_axioms.append((p, j))
        rela = main_concepts[index].get_super_concept_axioms()
        if rela:
            for j in rela:
                if (j, p) not in relations_edge:
                    relations_edge.append((j, p))
                    axiom_color_edge.append((j, p))
                    axiom_color.append('blue')
                    network_colors.append("YES")
                    all_axioms.append((j, p))
        global save_flag_meta_data
        save_flag_meta_data = 1


def cycles_in_graph(sub, super):
    G = nx.DiGraph()
    flag = False
    result_relations = []
    result_concepts = []
    for i in main_concept_names:
        G.add_node(i)
    for edge in relations_edge:
        G.add_edge(edge[0], edge[1])
    G.add_edge(sub, super)
    for cycle in nx.simple_cycles(G):
        if sub in cycle and super in cycle:
            print(cycle)
            flag = True
            result_concepts = cycle
            for r in relations_edge:
                if (r[0] in cycle) and (r[1] in cycle):
                    if r not in result_relations:
                        result_relations.append(r)
    return flag, result_concepts, result_relations


def add_relation(ph, relations, phrase1, phrase2, direction, window):
    global selected_concept
    selected_concept = ''

    def destroy_equivalent_window(question_w, main_window, e):
        question_w.destroy()
        main_window.destroy()

    def select_concpet_to_keep(sub, super, main_window, result_relation_list, phrase1):
        # Which concept name do the user want to keep, sub or super?
        question_window = Toplevel(root)
        question_window.title("Equivalent concept names")
        question_window.geometry("500x200+450+200")
        question_window.configure(background='white')
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        question_window.wm_iconphoto(False, photo)
        Label(question_window, text="Because of the created cycle, the concepts presented bellow would be equivalent:",
              bg='white',
              font='Helvetica 9 bold').grid(row=1, column=1, padx=5, pady=5)
        listbox_e = Listbox(question_window)
        listbox_e.grid(row=2, column=1)
        listbox_e.config(width=0, height=0)
        equivalent_concepts = []
        for r in result_relation_list:
            if r[0] not in equivalent_concepts:
                equivalent_concepts.append(r[0])
            if r[1] not in equivalent_concepts:
                equivalent_concepts.append(r[1])
        flag = 0
        index_equivalent_concepts_list = -1
        for list in equivalent_concepts_list:
            for r in list:
                if r in equivalent_concepts:
                    flag = 1
                    i = equivalent_concepts_list.index(list)
                    index_equivalent_concepts_list = i
                    for c in equivalent_concepts:
                        if c not in list:
                            list.append(c)
                    break
        if flag == 0:
            equivalent_concepts_list.append(equivalent_concepts)
        if index_equivalent_concepts_list != -1:
            for c in equivalent_concepts_list[index_equivalent_concepts_list]:
                listbox_e.insert(END, c)
        else:
            for c in equivalent_concepts:
                listbox_e.insert(END, c)
        listbox_axiom_view.insert(END, temp)
        if direction == 0:
            i = main_concept_names.index(ph)
            s = []
            s = main_concepts[i].get_concept_axioms()
            if s == '':
                s = []
            if phrase1 not in main_concept_names:
                if concept_name_style_var.get() == 1:
                    phrase1 = camelcase_concept_name(phrase1)
            s.append(phrase1)
            main_concepts[i].set_concept_axioms(s)
            axiom_color_edge.append((ph, phrase1))
            axiom_color.append('blue')
            relations_edge.append((ph, phrase1))
            if phrase1 not in main_concept_names:
                add_to_concepts_new(phrase1, ph, direction)
            save_metadata_relation(listbox_axiom_view)
            refresh_meta_data_tabs()
        else:
            i = main_concept_names.index(sub)
            s = []
            s = main_concepts[i].get_concept_axioms()
            if s == '':
                s = []
            s.append(super)
            main_concepts[i].set_concept_axioms(s)
            axiom_color_edge.append((sub, super))
            axiom_color.append('blue')
            relations_edge.append((sub, super))
            if sub not in main_concept_names:
                add_to_concepts_new(sub, super, direction)
            save_metadata_relation(listbox_axiom_view)
            refresh_meta_data_tabs()
        question_window.bind("<Destroy>", lambda e: destroy_equivalent_window(question_window, main_window, e))

    def adding_axiom_consequences_window(sub, super, result_relation_list):
        temp_value = sub + "   " + relations + "   " + super
        window = Toplevel(root)
        window.title("WARNING:   Cycle Detection")
        window.geometry("600x400+450+100")
        window.configure(background='white')
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        window.wm_iconphoto(False, photo)
        label1 = Label(window,
                       text='The new defined axiom will lead to a cycle because of existing axioms presented below:',
                       bg='white', font='Helvetica 9 bold')
        label1.grid(row=1, column=1, pady=10, padx=20)
        listbox_consequences = Listbox(window)
        listbox_consequences.grid(row=2, column=1, pady=5)
        listbox_consequences.config(width=0, height=0)
        listbox_consequences.insert(END, "Your defined axiom:")
        listbox_consequences.insert(END, temp_value)
        listbox_consequences.itemconfig(END, fg='purple')
        listbox_consequences.insert(END, '\n')
        listbox_consequences.insert(END, "Set of axioms that will lead to a cycle:")
        listbox_consequences.itemconfig(END, fg='navy')
        for r in result_relation_list:
            temp_text = r[0] + "   is-a   " + r[1]
            listbox_consequences.insert(END, temp_text)
        listbox_consequences.insert(END, "\n")
        listbox_consequences.insert(END, "Derived axiom")
        listbox_consequences.itemconfig(END, fg='navy')
        temp_text = super + " " + relations + " " + sub
        listbox_consequences.insert(END, temp_text)
        listbox_consequences.itemconfig(END, fg='purple')
        temp_message = "Do you want to continue to add the axiom? \n If yes, all the concepts in the axioms that leads to a cycle will be equivalent."
        label1 = Label(window, text=temp_message, bg='white', font='Helvetica 9 bold')
        label1.grid(row=3, column=1, pady=10, padx=5)
        b1 = Button(window, text="Cancel", width=10, fg='black', bg='lightBlue1', font=('comicsans', 10),
                    command=window.destroy)
        b1.grid(row=4, column=1, pady=3)
        b2 = Button(window, text="OK", width=10, fg='black', bg='lightBlue1', font=('comicsans', 10),
                    command=lambda: select_concpet_to_keep(sub, super, window, result_relation_list, phrase1))
        b2.grid(row=5, column=1, pady=5)
        window.lift()

    if direction == 0:
        if phrase1 != "":
            phrase1_lower = phrase1.lower()
            main_concept_names_lower = [c.lower() for c in main_concept_names]
            if phrase1 not in main_concept_names:
                if phrase1_lower in main_concept_names_lower:
                    index_lower = main_concept_names_lower.index(phrase1_lower)
                    phrase1 = main_concept_names[index_lower]
                else:
                    if concept_name_style_var.get() == 1:
                        phrase1 = camelcase_concept_name(phrase1)
            if phrase1 != ph:
                temp = ph + " " + relations + " " + phrase1
                if temp not in listbox_axiom_view.get(0, END):
                    flag, result_concepts, result_relations = cycles_in_graph(ph, phrase1)
                    if flag == False:
                        listbox_axiom_view.insert(END, temp)
                        i = main_concept_names.index(ph)
                        s = main_concepts[i].get_concept_axioms()
                        if s == '':
                            s = []
                        s.append(phrase1)
                        main_concepts[i].set_concept_axioms(s)
                        axiom_color_edge.append((ph, phrase1))
                        axiom_color.append('blue')
                        relations_edge.append((ph, phrase1))
                        if phrase1 not in main_concept_names:
                            add_to_concepts_new(phrase1, ph, direction)
                        save_metadata_relation(listbox_axiom_view)
                        refresh_meta_data_tabs()
                    else:
                        adding_axiom_consequences_window(ph, phrase1, result_relations)
                else:
                    info_window("The axiom already exists", "Error", 5000)
            else:
                info_window("Sub and super concept of relation are the same", "Error", 5000)
        else:
            messagebox.showerror("Error", "Select a phrase!", parent=window)
    if direction == 1:
        if phrase2 != "":
            phrase2_lower = phrase2.lower()
            main_concept_names_lower = [c.lower() for c in main_concept_names]
            if phrase2 not in main_concept_names:
                if phrase2_lower in main_concept_names_lower:
                    index_lower = main_concept_names_lower.index(phrase2_lower)
                    phrase2 = main_concept_names[index_lower]
                else:
                    if concept_name_style_var.get() == 1:
                        phrase2 = camelcase_concept_name(phrase2)
            if phrase2 != ph:
                temp = phrase2 + " " + relations + " " + ph
                if temp not in listbox_axiom_view.get(0, END):
                    flag, result_concepts, result_relations = cycles_in_graph(phrase2, ph)
                    if flag == False:
                        if phrase2 not in main_concept_names:
                            add_to_concepts_new(phrase2, ph, direction)
                        phrase2 = phrase2.replace(" ", "")
                        listbox_axiom_view.insert(END, temp)
                        i = main_concept_names.index(phrase2)
                        s = []
                        s = main_concepts[i].get_concept_axioms()
                        if s == '':
                            s = []
                        s.append(ph)
                        main_concepts[i].set_concept_axioms(s)
                        i = main_concept_names.index(ph)
                        s = main_concepts[i].get_super_concept_axioms()
                        if s == '':
                            s = []
                        s.append(phrase2)
                        main_concepts[i].set_super_concept_axioms(s)
                        axiom_color_edge.append((phrase2, ph))
                        axiom_color.append('blue')
                        relations_edge.append((phrase2, ph))
                        save_metadata_relation(listbox_axiom_view)
                        refresh_meta_data_tabs()
                    else:
                        adding_axiom_consequences_window(phrase2, ph, result_relations)
                else:
                    info_window("The axiom already exists", "Error", 5000)
            else:
                info_window("Sub and super concept of relation are the same", "Error", 5000)
        else:
            messagebox.showerror("Error", "Select a phrase!", parent=window)


def OnMouseWheel_function(e, listname):
    listname.yview_scroll(-1 * int(e.delta / 120), "units")
    return "break"


def listbox_copy(listbox, event):
    root.clipboard_clear()
    selected = listbox.get(ANCHOR)
    root.clipboard_append(selected)


def concept_tab_axiom_view(ph):
    def click_on_concept_axiom_view(e, main_phrase):
        try:
            curselection = listbox_axiom_view.curselection()
            index = curselection[0]
            ph = listbox_axiom_view.get(index)
            if ph != '':
                x1 = ph.split('is-a', 1)[0]
                x2 = ph.split('is-a', 1)[1]
                x1_1 = x1.strip()
                x2_2 = x2.strip()
                result_relations = []
                result_concepts = []
                relations = []
                result_concepts, result_realtions, relations = find_relations_super_2(main_phrase,x2_2,result_relations,result_concepts,relations)
                listbox_axiom_view_super_axioms.delete(0, END)
                for r in relations:
                    listbox_axiom_view_super_axioms.insert(END, r)
                result_relations_sub = []
                result_concepts_sub = []
                relations_sub = []
                result_concepts_sub, result_realtions_sub, relations_sub = find_relations_sub_2(main_phrase, x1_1,result_relations_sub,result_concepts_sub,relations_sub)
                listbox_axiom_view_sub_axioms.delete(0, END)
                for r in relations_sub:
                    listbox_axiom_view_sub_axioms.insert(END, r)
        except:
            pass
    def on_enter_search_2(e):
        toolTip.showtip(search_2.get())
    def on_leave_search_2(e):
        toolTip.hidetip()
    def on_enter_search_3(e):
        toolTip.showtip(search_3.get())
    def on_leave_search_3(e):
        toolTip.hidetip()
    def enable_direction1():
        search_2.configure(state='normal')
        search_3.delete(0, END)
        search_3.configure(state='disable')
        listbox_search_2.selection_clear(0, END)
    def enable_direction2():
        search_3.configure(state='normal')
        search_2.delete(0, END)
        search_2.configure(state='disable')
        listbox_search_2.selection_clear(0, END)
    def on_enter_listbox(e, listname):
        try:
            index = listname.index("@%s,%s" % (e.x, e.y))
            if index >= 0:
                toolTip.showtip(listname.get(index))
                global element_display_popup
                element_display_popup = index
        except:
            pass
    def on_leave_listbox_2(e):
        toolTip.hidetip()
        global element_display_popup
        element_display_popup = -1
    def on_leave_listbox_3(e):
        toolTip.hidetip()
        global element_display_popup
        element_display_popup = -1
    def on_motion_listbox(e, listname):
        global element_display_popup
        index = listname.index("@%s,%s" % (e.x, e.y))
        if index >= 0:
            try:
                if index != element_display_popup:
                    toolTip.hidetip()
                    element_display_popup = index
                    toolTip.showtip(listname.get(index))
            except:
                pass
    def on_leave_listbox_1(e):
        toolTip.hidetip()
    def on_motion_listbox(e, listname):
        index = listname.index("@%s,%s" % (e.x, e.y))
        if index >= 0:
            try:
                toolTip.hidetip()
                try:
                    toolTip.showtip(listname.get(index))
                except:
                    pass
            except:
                pass
    axioms = []
    global window_concept_axiom_view
    if window_concept_axiom_view:
        window_concept_axiom_view.destroy()
        window_concept_axiom_view = Frame(notebook_concepts, bg="white")
    global window_concept_note_view
    if window_concept_note_view:
        window_concept_note_view.destroy()
        window_concept_note_view = Frame(notebook_concepts, bg="white")
    Frame12 = Frame(window_concept_axiom_view, borderwidth=1, bg='white')
    Frame11 = Frame(Frame12, borderwidth=1, bg='white')
    global axiom_direction
    b1 = Radiobutton(Frame11, text=" ", variable=axiom_direction, value=0, command=enable_direction1, bg="white")
    b1.grid(row=1, column=1, sticky='W')
    b2 = Radiobutton(Frame11, text=" ", variable=axiom_direction, value=1, command=enable_direction2, bg="white")
    b2.grid(row=2, column=1, pady=30, sticky='W')
    Label(Frame11, text=ph, bg='white', font='Helvetica 9 bold', relief='groove', width=30).grid(row=1, column=2)
    options = ["is-a"]
    variable = StringVar(Frame11)
    variable.set(options[0])
    relations = tkinter.OptionMenu(Frame11, variable, *options)
    relations.grid(row=1, column=3)
    global search_2
    search_2 = Entry(Frame11, font=("Helvetica", 11), width=27)
    search_2.grid(row=1, column=4)
    search_2.bind("<Enter>", on_enter_search_2)
    search_2.bind("<Leave>", on_leave_search_2)
    global search_3
    search_3 = Entry(Frame11, font=("Helvetica", 11), width=27)
    search_3.grid(row=2, column=2, pady=30)
    search_3.bind("<Enter>", on_enter_search_3)
    search_3.bind("<Leave>", on_leave_search_3)
    options = ["is-a"]
    variable2 = StringVar(Frame11)
    variable2.set(options[0])
    relations2 = tkinter.OptionMenu(Frame11, variable2, *options)
    relations2.grid(row=2, column=3, pady=30)
    Label(Frame11, text=ph, bg='white', font='Helvetica 9 bold', relief='groove', width=30).grid(row=2, column=4,pady=5)
    Button10 = Button(Frame11, text="Add to axioms", width=20, fg='black', bg='lightBlue1', font=('comicsans', 11),command=lambda: add_relation(ph, variable.get(), search_2.get(), search_3.get(),
                                                   axiom_direction.get(),window_concept_axiom_view))
    Button10.grid(row=3, column=3)
    Frame11.grid(row=0, column=0)
    if axiom_direction.get() == 0:
        search_2.configure(state='normal')
        search_3.configure(state='disable')
    elif axiom_direction.get() == 1:
        search_2.configure(state='disable')
        search_3.configure(state='normal')
    else:
        search_2.configure(state='disable')
        search_3.configure(state='disable')
    Frame14 = Frame(Frame12, borderwidth=1, bg='white')
    global listbox_search_2
    listbox_search_2 = Listbox(Frame14, width=80, height=10)
    listbox_search_2.grid(row=1, column=1)
    update_2(main_concept_names)
    listbox_search_2.bind("<<ListboxSelect>>", fillout_2)
    listbox_search_2.bind("<Leave>", on_leave_listbox_1)
    listbox_search_2.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox_search_2))
    search_2.bind("<KeyRelease>", check_2)
    search_3.bind("<KeyRelease>", check_3)
    Frame14.grid(row=0, column=1)
    Frame12.grid(row=0, column=0, sticky='e', padx=5, pady=5)
    Frame3 = Frame(window_concept_axiom_view, borderwidth=0, bg='white')
    Label(Frame3, text='Axioms defined for the concept', bg='white', font='Helvetica 11 bold', fg='navy').grid(row=0,
                                                                                                               column=1)
    global listbox_axiom_view
    listbox_axiom_view = Listbox(Frame3, width=120, height=5, bg='azure')
    scrollbary_axiom_focus = AutoScrollbar(Frame3, command=scroll_view(listbox_axiom_view))
    listbox_axiom_view.config(yscrollcommand=scrollbary_axiom_focus.set)
    scrollbary_axiom_focus.config(command=listbox_axiom_view.yview)
    listbox_axiom_view.grid(row=1, column=1)
    scrollbary_axiom_focus.grid(row=1, column=2, sticky="ns")
    listbox_axiom_view.bind('<Double-Button-1>', lambda event: listbox_copy(listbox_axiom_view, event))
    element_display_popup = -1
    listbox_axiom_view.bind("<Enter>", lambda event: on_enter_listbox(e=event, listname=listbox_axiom_view))
    listbox_axiom_view.bind("<Leave>", on_leave_listbox_1)
    listbox_axiom_view.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox_axiom_view))
    Frame3_2 = Frame(Frame3, borderwidth=0, bg='white')
    Label(Frame3_2, text='Axioms related to super-concepts of concept', bg='white', font='Helvetica 10 bold',
          fg='navy').grid(row=0, column=0)
    listbox_axiom_view_super_axioms = Listbox(Frame3_2, width=55, height=7, bg='azure')
    listbox_axiom_view_super_axioms.grid(row=1, column=0, pady=1)
    scrollbary_axiom_focus_super = AutoScrollbar(Frame3_2, command=scroll_view(listbox_axiom_view_super_axioms))
    listbox_axiom_view_super_axioms.config(yscrollcommand=scrollbary_axiom_focus_super.set)
    scrollbary_axiom_focus_super.config(command=listbox_axiom_view_super_axioms.yview)
    scrollbary_axiom_focus_super.grid(row=1, column=1, sticky='nsew', pady=1)
    listbox_axiom_view_super_axioms.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event, listname=listbox_axiom_view_super_axioms))
    listbox_axiom_view_super_axioms.bind('<Double-Button-1>',
                                         lambda event: listbox_copy(listbox_axiom_view_super_axioms, event))
    Label(Frame3_2, text='Axioms related to sub-concepts of concept', bg='white', font='Helvetica 10 bold',
          fg='navy').grid(row=0,column=2)
    listbox_axiom_view_sub_axioms = Listbox(Frame3_2, width=55, height=7, bg='azure')
    scrollbary_axiom_focus_sub = AutoScrollbar(Frame3_2, command=scroll_view(listbox_axiom_view_sub_axioms))
    listbox_axiom_view_sub_axioms.config(yscrollcommand=scrollbary_axiom_focus_sub.set)
    scrollbary_axiom_focus_sub.config(command=listbox_axiom_view_sub_axioms.yview)
    scrollbary_axiom_focus_sub.grid(row=1, column=3, sticky="ns")
    listbox_axiom_view_sub_axioms.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event,
                                                                                           listname=listbox_axiom_view_sub_axioms))
    listbox_axiom_view_sub_axioms.grid(row=1, column=2, padx=20)
    listbox_axiom_view_sub_axioms.bind('<Double-Button-1>',
                                       lambda event: listbox_copy(listbox_axiom_view_sub_axioms, event))
    Frame3_2.grid(row=2, column=1, pady=10)
    Frame3.grid(row=1, column=0, sticky='w', padx=5, pady=20)
    i = main_concept_names.index(ph)
    r = main_concepts[i].get_concept_axioms()
    if r:
        for item in r:
            if "is-a" not in item:
                temp = ph + " is-a " + item
                listbox_axiom_view.insert(END, temp)
                axioms.append(temp)
            else:
                listbox_axiom_view.insert(END, item)
                axioms.append(item)
    r = main_concepts[i].get_super_concept_axioms()
    if r:
        for item in r:
            if "is-a" not in item:
                temp = item + " is-a " + ph
                listbox_axiom_view.insert(END, temp)
                axioms.append(temp)
            else:
                listbox_axiom_view.insert(END, item)
                axioms.append(item)
    listbox_axiom_view.bind("<<ListboxSelect>>", lambda e: click_on_concept_axiom_view(e, ph))
    global listbox8_deleted
    global listbox8_deleted_index
    listbox8_deleted = ''
    listbox8_deleted_index = -1
    listbox_axiom_view_super_axioms.bind("<Enter>", lambda event: on_enter_listbox(e=event,
                                                                                   listname=listbox_axiom_view_super_axioms))
    listbox_axiom_view_super_axioms.bind("<Leave>", on_leave_listbox_2)
    listbox_axiom_view_super_axioms.bind("<Motion>", lambda event: on_motion_listbox(e=event,
                                                                                     listname=listbox_axiom_view_super_axioms))
    listbox_axiom_view_sub_axioms.bind("<Enter>",
                                       lambda event: on_enter_listbox(e=event, listname=listbox_axiom_view_sub_axioms))
    listbox_axiom_view_sub_axioms.bind("<Leave>", on_leave_listbox_3)
    listbox_axiom_view_sub_axioms.bind("<Motion>",
                                       lambda event: on_motion_listbox(e=event, listname=listbox_axiom_view_sub_axioms))
    window_concept_axiom_view.lift()
    window_concept_axiom_view.pack()
    notebook_concepts.add(window_concept_axiom_view, text="Define axioms for the selected concept")
    notebook_concepts.add(window_concept_note_view, text="Add note to selected concept")
    notebook_concepts.select(window_concept_axiom_view)


def concept_note(ph):
    i = main_concept_names.index(ph)
    global window_concept_note_view
    if window_concept_note_view:
        window_concept_note_view.destroy()
        window_concept_note_view = Frame(notebook_concepts, bg="white")  # width=950, height=450,
    Frame_note = Frame(window_concept_note_view, borderwidth=1, bg='azure')
    Frame_note_temp = Frame(window_concept_note_view, borderwidth=0, bg='azure')
    textbox_note = Text(Frame_note_temp, width=100, height=20, undo=True, borderwidth=0, bg='azure',
                        font=('comicsans bold', 12))
    scrollbary_textbox_note = Scrollbar(Frame_note_temp, command=textbox_note.yview)  # , width=30, height=2,
    textbox_note.config(yscrollcommand=scrollbary_textbox_note.set)
    textbox_note.pack(side="left", fill=Y, expand=False)
    scrollbary_textbox_note.pack(side="right", fill=Y, expand=False)
    Frame_note_temp.pack(fill='both', expand=True)
    b = Button(Frame_note, text="Save Note", width=15, height=2, fg='black', bg='lightBlue1',
               font=('comicsans bold', 12),
               command=lambda: save_concept_note((textbox_note.get("1.0", END)[:-1]), ph))
    b.pack(padx=10, pady=20, anchor=W)
    Frame_note.pack(fill='both', expand=True)
    notebook_concepts.add(window_concept_note_view, text="Add note to selected concept")
    textbox_note.delete('1.0', END)
    textbox_note.insert('1.0', main_concepts[i].get_concept_note())


def phrase_stemming(p):
    temp = p
    for word in temp.split():
        t1 = stem(word)
        p = p.replace(word, t1)
    return p


def info_window(message, title, time):
    window = Toplevel(root)
    window.title(title)
    window.geometry("+500+200")
    window.configure(background='white')
    window.resizable(0, 0)
    ico = Image.open('p2o.png')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)
    my_label = Label(window, text=message, bg='white', font='Helvetica 9 bold')
    my_label.pack()
    if time != -1:
        window.after(time, window.destroy)


def camelcase_concept_name(name):
    name = str(name)
    name_1 = name.title()
    name_1 = name_1.strip()
    name_2 = name_1.replace(" ", "")
    return name_2


def substring(phrase1, phrase2):
    for word in phrase1.split():
        for w in phrase2.split():
            if word == w:
                return 1
    return 0


def click_on_concept_listbox(e, listboxname):
    try:
        if window_concept_axiom_focus_view:
            window_concept_axiom_focus_view.destroy()
        curselection = listboxname.curselection()[0]
        concept_name.config(text=listboxname.get(curselection))
        ph = concept_name.cget("text")
        if ph != '':
            index = main_concept_names.index(ph)
            listbox1_concept_names.selection_clear(0, END)
            listbox1_concept_names.see(index)
            listbox_mark_concepts.see(index)
            listbox1_concept_names.selection_set(index)
            concept_origin.config(text=main_concepts[index].get_concept_origin())
            concept_tab_axiom_view(ph)
            concept_note(ph)
            notebook_main.select(higher_view_concept_window)
            if previous_tab_id_concept == 0:
                notebook_concepts.select(window_concept_axiom_view)
            elif previous_tab_id_concept == 1:
                notebook_concepts.select(window_concept_note_view)
    except:
        pass


def click_on_phrase_listbox(e, listboxname):
    try:
        curselection = listboxname.curselection()[0]
        p1.config(text=listboxname.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            index = phrases.index(ph)
            listbox1.selection_clear(0, END)
            listbox1.selection_set(index)
            listbox1.see(index)
            p1.config(text=ph)
            add_meta_data_tab(ph)
            matching_tab(ph)
            add_note_phrase(ph)
            if previous_tab_id == 0:
                notebook_phrases.select(window_phrase_add_metadata_view)
            else:
                if previous_tab_id == 1:
                    notebook_phrases.select(window_phrase_matching_view)
                else:
                    notebook_phrases.select(window_phrase_note_view)
    except:
        pass


def matching_tab(ph):
    def clear_all():
        listbox4.delete(0, END)
        listbox5.delete(0, END)

    def matching():
        listbox4.delete(0, END)
        listbox5.delete(0, END)
        global main_classes
        if ph != '':
            result_c = []
            stem_ph = phrase_stemming(ph)
            for s in main_concept_names:
                x = s.lower()
                r = fuzz.ratio(ph, x)
                if r > 80:
                    result_c.append(s)
                temp = phrase_stemming(x)
                if temp == stem_ph:
                    if s not in result_c:
                        result_c.append(s)
                else:
                    for word in stem_ph.split():
                        if word in temp:
                            if s not in result_c:
                                result_c.append(s)
                            break
            if len(result_c) > 0:
                for i in result_c:
                    listbox5.insert(END, i)
            phrases_2 = phrases
            result_p = []
            result_p_label = []
            stem_result_p = []
            stem_result_p_label = []
            for x in phrases_2:
                if x != ph:
                    r = fuzz.ratio(ph, x)
                    if r > 80:
                        result_p.append(x)
                        i = phrases_2.index(x)
                        result_p_label.append(all_phrases[i].get_validation_label())
                    temp = phrase_stemming(x)
                    if temp == stem_ph:
                        stem_result_p.append(x)
                        i = phrases_2.index(x)
                        stem_result_p_label.append(all_phrases[i].get_validation_label())
                    else:
                        if (substring(temp, stem_ph) == 1):
                            stem_result_p.append(x)
                            i = phrases_2.index(x)
                            stem_result_p_label.append(all_phrases[i].get_validation_label())
        else:
            messagebox.showerror("Error", "Please select a phrase for matching!")
            return False
        if len(stem_result_p) > 0:
            for i in stem_result_p:
                listbox4.insert(END, i)

    def on_enter_listbox(e, listname):
        try:
            index = listname.index("@%s,%s" % (e.x, e.y))
            if index >= 0:
                toolTip.showtip(listname.get(index))
                global element_display_popup
                element_display_popup = index
        except:
            pass

    def on_leave_listbox(e):
        toolTip.hidetip()

    def on_motion_listbox(e, listname):
        index = listname.index("@%s,%s" % (e.x, e.y))
        if index >= 0:
            try:
                toolTip.hidetip()
                try:
                    toolTip.showtip(listname.get(index))
                except:
                    pass
            except:
                pass

    global notebook_phrases
    global window_phrase_matching_view
    if window_phrase_matching_view:
        window_phrase_matching_view.destroy()
        window_phrase_matching_view = Frame(notebook_phrases, bg="white")  # width=950, height=450
    Frame3 = Frame(window_phrase_matching_view, bg='whitesmoke')
    Label(Frame3, text='Matched Phrases', bg='whitesmoke', font='Helvetica 9 bold', fg='navy').grid(row=0, column=0,
                                                                                                    padx=40, sticky='w')
    Label(Frame3, text='', bg='whitesmoke').grid(row=0, column=2)
    Label(Frame3, text='Matched Concepts', bg='whitesmoke', font='Helvetica 9 bold', fg='navy').grid(row=0, column=3,
                                                                                                     padx=40, sticky='w')
    listbox4 = Listbox(Frame3, width=40, height=10, bg='whitesmoke', borderwidth=0, highlightthickness=0)
    listbox4.grid(row=1, column=0)
    listbox4_3 = Listbox(Frame3, width=1, height=10, bg="silver")
    listbox4_3.grid(row=1, column=1)
    listbox5 = Listbox(Frame3, width=40, height=10, bg='whitesmoke', borderwidth=0, highlightthickness=0)
    listbox5.grid(row=1, column=3)
    listbox4.bind("<Double-Button-1>", lambda e: click_on_phrase_listbox(e, listbox4))
    listbox5.bind("<Double-Button-1>", lambda e: click_on_concept_listbox(e, listbox5))
    listbox4.bind("<Enter>", lambda event: on_enter_listbox(e=event, listname=listbox4))
    listbox4.bind("<Leave>", lambda event: on_leave_listbox(e=event))
    listbox4.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox4))
    listbox5.bind("<Enter>", lambda event: on_enter_listbox(e=event, listname=listbox5))
    listbox5.bind("<Leave>", lambda event: on_leave_listbox(e=event))
    listbox5.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox5))
    scrollbary_listbox4 = AutoScrollbar(Frame3, command=scroll_view(listbox4))
    scrollbary_listbox4.configure(command=listbox4.yview)
    listbox4.config(yscrollcommand=scrollbary_listbox4.set)
    scrollbary_listbox4.grid(row=1, column=1, sticky="ns")
    scrollbary_listbox5 = AutoScrollbar(Frame3, command=scroll_view(listbox5))
    scrollbary_listbox5.configure(command=listbox5.yview)
    listbox5.config(yscrollcommand=scrollbary_listbox5.set)
    scrollbary_listbox5.grid(row=1, column=4, sticky="ns")
    Frame6 = Frame(Frame3, bg='whitesmoke')
    Button2 = Button(Frame6, text="Matching", width=20, fg='black', bg='lightBlue1', font=('comicsans', 10),
                     command=matching)
    Button2.pack(padx=10, pady=10, anchor=W)
    Button3 = Button(Frame6, text="Clear Matching Lists", width=20, fg='black', bg='lightBlue1', font=('comicsans', 10),
                     command=clear_all)
    Button3.pack(padx=10, pady=5, anchor=W)
    Frame6.grid(row=1, column=5, padx=30, pady=20)
    Frame3.grid(row=0, column=0, padx=10, pady=10)
    text_temp = "Focus on selected phrase"
    notebook_phrases.add(window_phrase_matching_view, text=text_temp)


def mark_phrase_done():
    p1.config(text=listbox1.get(ANCHOR))
    ph = p1.cget("text")
    if ph != '':
        i = phrases.index(ph)
        listbox1.itemconfig(i, fg='green')
        all_phrases[i].set_phrase_refinedf('green')


def mark_phrase_menu():
    try:
        p1.config(text=listbox1.get(ANCHOR))
        ph = p1.cget("text")
        if ph != '':
            i = phrases.index(ph)
            listbox1.itemconfig(i, fg='red')
            all_phrases[i].set_phrase_listmark_color('red')
    except:
        pass


def unmark_phrase_menu():
    try:
        p1.config(text=listbox1.get(ANCHOR))
        ph = p1.cget("text")
        if ph != '':
            i = phrases.index(ph)
            color = all_phrases[i].get_phrase_color()
            listbox1.itemconfig(i, fg=color)
            all_phrases[i].set_phrase_listmark_color('')
    except:
        pass


def unmark_phrase_done():
    p1.config(text=listbox1.get(ANCHOR))
    ph = p1.cget("text")
    if (ph != ''):
        i = phrases.index(ph)
        color = all_phrases[i].get_phrase_color()
        listbox1.itemconfig(i, fg=color)
        all_phrases[i].set_phrase_listmark_color('')


def my_popup_3(e):
    currentselection = listbox1.curselection()[0]
    selection = listbox1.get(listbox1.curselection()[0])
    if selection:
        x_position = e.widget.winfo_rootx()
        y_position = e.widget.winfo_rooty()
        itemx, itemy, itemwidth, itemheight = e.widget.bbox(currentselection)
        listbox1_menu.tk_popup(x_position + e.widget.winfo_width() - 10, y_position + itemy + 10)


# load topics
def load_topics():
    topics_files = filedialog.askopenfilenames(title="Select Topic files to load", filetypes=(("text Files", "*.txt"),))
    paths = root.tk.splitlist(topics_files)
    if paths:
        read_topic_file(paths)
        update_topics(input_topics, paths)


def read_topic_file(paths):
    if paths:
        input_topics.clear()
        global topics_loaded_label
        global topics_loaded_path
        topics_loaded_path.config(state="normal")
        if not topics_loaded_path:
            topics_loaded_label.config(text="")
            topics_loaded_path.delete('1.0', END)
        global topic_number
        topic_number = []
        for path in paths:
            topics_temp = []
            input_file_1 = open(path, "r")
            lines = input_file_1.readlines()
            s = path.rsplit('/')[-1]
            x = s.replace('.txt', '')
            topic_number.append(x)
            topic_representative_info.update({x: []})
            topic_labelling_info.update({x: []})
            for j in lines:
                temp = re.sub('[^A-Za-z]+', ' ', j)
                temp = temp.lstrip()
                temp = temp.strip()
                if temp != ' ' and temp != '':
                    topics_temp.append(temp)
                    if temp in phrases:
                        index_temp = phrases.index(temp)
                        topics_name_temp = all_phrases[index_temp].get_topics_name_phrase_in()
                        if x not in topics_name_temp:
                            topics_name_temp.append(x)
                        all_phrases[index_temp].set_topics_name_phrase_in(topics_name_temp)
                    else:
                        phrases.append(temp)
                        temp_node = NodeType_phrase(temp, [x], '', [], 'black', '', '', '', '')
                        all_phrases.append(temp_node)
            input_topics.append(topics_temp)
            topics_loaded_path.insert(END, path)
            topics_loaded_path.insert(END, '\n')
            topics_loaded_path_values.append(path)
        topics_loaded_path.config(state="disabled")


def function_find_topicslabels_contains_phrase(p, current_topic_index):
    topics_phrase_in = function_find_topics_contains_phrase(p, current_topic_index)
    topic_labels_temp = []
    for i in topics_phrase_in:
        for temp in topic_labelling_info[i]:
            if p in temp.get_representative_phrases():
                topic_labels_temp.append(temp.get_topic_label())
    return topic_labels_temp


def update_topics(data, paths):
    global topics_loaded_label
    global topics_loaded_path
    global topic_selection_2
    topics_loaded_path.config(state="normal")
    topics_loaded_label.config(text="")
    listbox1_topics_phrases.delete(0, END)
    listbox2_topics_phrases.delete(0, END)
    listbox_mark_topics_phrases.delete(0, END)
    for t in input_topics[0]:
        listbox1_topics_phrases.insert(END, t)
        listbox2_topics_phrases.insert(END, " ")
        listbox_mark_topics_phrases.insert(END, " ")
    try:
        listbox1_topics_phrases.selection_set(0)
        topic_selection_2.current(0)
        try:
            curselection = listbox1_topics_phrases.curselection()[0]
            ph = listbox1_topics_phrases.get(curselection)
            if ph != '':
                topic_representation_tab(ph)
                add_focus_on_phrase_TopicsPhrasesConcepts()
                if previous_tab_id_topic_phraseConcept == 0:
                    notebook_topics_phrases.select(window_topic_representation)
                if previous_tab_id_topic_phraseConcept == 1:
                    notebook_topics_phrases.select(window_topic_representation_focus_on_phrase)
                if previous_tab_id_topic_phraseConcept == 2:
                    notebook_topics_phrases.select(window_TopicsPhrasesConcepts_note)
        except:
            pass
        notebook_main.tab(2, state="normal")
    except:
        pass
    global variable_topic
    topic_selection_2['values'] = topic_number
    topic_selection_2.current(0)
    topics_loaded_label.config(text="The Topics have been loaded successfully!", font='Helvetica 11 bold')
    topics_loaded_path.config(state="disabled")
    update_phrases_2(phrases, paths)
    root.mainloop()


# load frequent phrases file
def load_phrases():
    phrases_files = filedialog.askopenfilenames(title="Select Phrases files to load",
                                                filetypes=(("text Files", "*.txt"),))
    paths = root.tk.splitlist(phrases_files)
    if paths:
        read_phrase_file(paths)
        update_phrases_2(input_phrases, paths)


def read_phrase_file(paths):
    if paths:
        input_phrases.clear()
        global phrases_loaded_label
        global phrases_loaded_path
        phrases_loaded_path.config(state="normal")
        if not phrases_loaded_path:
            phrases_loaded_label.config(text="")
            phrases_loaded_path.delete('1.0', END)
        for path in paths:
            input_file_1 = open(path, "r")
            lines = input_file_1.readlines()
            for j in lines:
                input_phrases.append(re.sub('[^A-Za-z]+', ' ', j))
            phrases_loaded_path.insert(END, path)
            phrases_loaded_path.insert(END, '\n')
            phrases_loaded_path_values.append(path)
        phrases_loaded_path.config(state="disabled")


def update_phrases_2(data, paths):
    global phrases_loaded_label
    global phrases_loaded_path
    phrases_loaded_path.config(state="normal")
    phrases_loaded_label.config(text="")
    global phrases
    global all_phrases
    if not phrases:
        phrases.clear()
        all_phrases.clear()
    listbox1.delete(0, END)
    listbox2.delete(0, END)
    for item in data:
        item = item.strip()
        temp_node = NodeType_phrase(item, [], '', [], 'black', '', '', '', '')
        if item not in phrases:
            phrases.append(item)
            all_phrases.append(temp_node)
    for item in phrases:
        item = item.strip()
        i = phrases.index(item)
        listbox1.insert(END, item)
        listbox2.insert(END, all_phrases[i].get_validation_label())
    listbox1.selection_set(0)
    try:
        curselection = listbox1.curselection()[0]
        p1.config(text=listbox1.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            add_meta_data_tab(ph)
            matching_tab(ph)
            add_note_phrase(ph)
            if previous_tab_id == 0:
                notebook_phrases.select(window_phrase_add_metadata_view)
            else:
                if previous_tab_id == 1:
                    notebook_phrases.select(window_phrase_matching_view)
                else:
                    notebook_phrases.select(window_phrase_note_view)
    except:
        pass
    notebook_main.tab(1, state="normal")
    phrases_loaded_label.config(text="The frequent phrases has been loaded successfully!", font='Helvetica 11 bold')
    phrases_loaded_path.config(state="disabled")
    root.mainloop()


def fillout_2(e):
    search_2.delete(0, END)
    try:
        search_2.insert(0, listbox_search_2.get(listbox_search_2.curselection()))
        search_3.delete(0, END)
        search_3.insert(0, listbox_search_2.get(listbox_search_2.curselection()))
    except:
        pass


def check_2(e):
    typed = search_2.get()
    if typed == '':
        data = main_concept_names
    else:
        data = []
        for item in main_concept_names:
            if typed.lower() in item.lower():
                data.append(item)
    update_2(data)


def check_3(e):
    typed = search_3.get()
    if typed == '':
        data = main_concept_names
    else:
        data = []
        for item in main_concept_names:
            if typed.lower() in item.lower():
                data.append(item)
    update_2(data)


def update_2(data):
    listbox_search_2.delete(0, END)
    listbox_search_2.insert(END, *data)


def save_as_excel_FrequentPhrases():
    myFormats = [("Excel files", "*.xls")]
    filename = filedialog.asksaveasfilename(filetypes=myFormats)
    name_main = filename.rsplit('/', 1)[-1]
    if filename and re.match("^[A-Za-z0-9_-]*$", name_main):
        output_name_phrases = filename + "_phrases.xls"
        output_name_concpets = filename + "_concepts.xls"
        output_name_info = filename + "_info.xls"
        output_name_axioms = filename + "_axioms.xls"
        output_topic_info = filename + "_topic_info.xls"
        output_topic_list = filename + "_topic_list.xls"
        book = xlwt.Workbook()
        sh1 = book.add_sheet("sheet_1")
        sh1.write(0, 0, "Phrase")
        sh1.write(0, 1, "topics included phrase")
        sh1.write(0, 2, "Refined Form")
        sh1.write(0, 3, "Extracted Concepts")
        sh1.write(0, 4, "color")
        sh1.write(0, 5, "Note")
        sh1.write(0, 6, "Related Concepts")
        sh1.write(0, 7, "Color mark column")
        sh1.write(0, 8, "Label")
        counter = 1
        for i in phrases:
            index = phrases.index(i)
            sh1.write(counter, 0, i)
            sh1.write(counter, 1, str(all_phrases[index].get_topics_name_phrase_in()))
            sh1.write(counter, 2, str(all_phrases[index].get_phrase_refinedf()))
            sh1.write(counter, 3, str(all_phrases[index].get_ext_concepts()))
            sh1.write(counter, 4, all_phrases[index].get_phrase_color())
            sh1.write(counter, 5, all_phrases[index].get_phrase_note())
            sh1.write(counter, 6, str(all_phrases[index].get_phrase_related_concepts()))
            sh1.write(counter, 7, all_phrases[index].get_phrase_listmark_color())
            sh1.write(counter, 8, all_phrases[index].get_validation_label())
            counter += 1
        # concepts
        book_concepts = xlwt.Workbook()
        sh2 = book_concepts.add_sheet("sheet_2")
        sh2.write(0, 0, "Concept")
        sh2.write(0, 1, "Axioms")
        sh2.write(0, 2, "super concepts")
        sh2.write(0, 3, "Color")
        sh2.write(0, 4, "Previous color")
        sh2.write(0, 5, "Origin")
        sh2.write(0, 6, "Note")
        sh2.write(0, 7, "color mark column")
        counter = 1
        for i in main_concept_names:
            index = main_concept_names.index(i)
            sh2.write(counter, 0, main_concepts[index].get_concept_name())
            sh2.write(counter, 1, str(main_concepts[index].get_concept_axioms()))
            sh2.write(counter, 2, str(main_concepts[index].get_super_concept_axioms()))
            sh2.write(counter, 3, main_concepts[index].get_concept_color())
            sh2.write(counter, 4, main_concepts[index].get_previous_concpet_color())
            sh2.write(counter, 5, main_concepts[index].get_concept_origin())
            sh2.write(counter, 6, main_concepts[index].get_concept_note())
            sh2.write(counter, 7, main_concepts[index].get_concept_color_listmark())
            counter += 1
        book_axioms = xlwt.Workbook()
        sh3 = book_axioms.add_sheet("sheet_3")
        sh3.write(0, 0, "Axiom")
        sh3.write(0, 1, "Axiom Color")
        counter = 1
        for i in axiom_color_edge:
            index = axiom_color_edge.index(i)
            sh3.write(counter, 0, i)
            sh3.write(counter, 1, axiom_color[index])
            counter += 1
        book_info = xlwt.Workbook()
        sh4 = book_info.add_sheet("sheet_4")
        sh4.write(0, 0, "ontology Path")
        sh4.write(0, 1, "FrequentPhrases Path")
        sh4.write(0, 2, "Topics Path")
        counter = 1
        for i in ontology_loaded_path_values:
            sh4.write(counter, 0, i)
            counter += 1
        counter = 1
        for i in phrases_loaded_path_values:
            sh4.write(counter, 1, i)
            counter += 1
        counter = 1
        for i in topics_loaded_path_values:
            sh4.write(counter, 2, i)
            counter += 1
        book_topic_info = xlwt.Workbook()
        sh5 = book_topic_info.add_sheet("sheet_5")
        sh5.write(0, 0, "origin topic")
        sh5.write(0, 1, "topic label")
        sh5.write(0, 2, "representative phrases")
        counter = 1
        for key, value in topic_labelling_info.items():
            for x in value:
                sh5.write(counter, 0, x.get_origin_topic())
                sh5.write(counter, 1, x.get_topic_label())
                sh5.write(counter, 2, str(x.get_representative_phrases()))
                counter += 1
        book_topic_list = xlwt.Workbook()
        sh6 = book_topic_list.add_sheet("sheet_6")
        sh6.write(0, 0, "topic list")
        counter = 1
        for i in input_topics:
            sh6.write(counter, 0, str(i))
            counter += 1
        book.save(output_name_phrases)
        book_concepts.save(output_name_concpets)
        book_axioms.save(output_name_axioms)
        book_info.save(output_name_info)
        book_topic_info.save(output_topic_info)
        book_topic_list.save(output_topic_list)
        messagebox.showinfo("info", "Output file has been saved!")
    else:
        messagebox.showerror("Error", "Please enter a valid name for output file!")


def save_as_owl():
    myFormats = [("OWL files", "*.owl")]
    filename = filedialog.asksaveasfilename(filetypes=myFormats)
    if filename:
        save_ontology_as_owl_new_2(filename)


def save_ontology_as_owl_new_2(name):
    name_main = name.rsplit('/', 1)[-1]
    if name and re.match("^[A-Za-z0-9_-]*$", name_main):
        output_name_2 = name + ".owl"
        file_name = output_name_2
        global ontology_help_owl
        x_temp = []
        if ontology_loaded_path_values:
            ontology_path = str(ontology_loaded_path_values[0].split('/')[-1])
            onto_path.append(".")
            onto = get_ontology(ontology_loaded_path_values[0]).load()
            t = onto.classes()
            x = list(onto.classes())
            for j in x:
                try:
                    x_temp.append(j.name)
                except:
                    x_temp.append(j)
        classes_in_main_ontology = []
        query = """
                   select ?class
                   where {?class a owl:Class}
                           """
        result = graph_ontology.query(query)
        for i in result:
            s = str(i)
            if "rdflib.term.URIRef" in s:
                j = re.findall("'(.*?)'", s)[0]
                x = j.rsplit('/', 1)[-1]
                y = str(x.rsplit('#')[-1])
                if y not in classes_in_main_ontology:
                    classes_in_main_ontology.append(y)
        for i in main_concept_names:
            if i not in x_temp:
                x_temp.append(i)
                index = main_concept_names.index(i)
                axioms = main_concepts[index].get_concept_axioms()
                if axioms != []:
                    for a in axioms:
                        with onto:
                            x = list(onto.classes())
                            b = str(a)
                            a_temp = x[x_temp.index(a)]
                            NewClass = types.new_class(i, (a_temp,))
                            h = a_temp.iri
                            s = a_temp.iri + "/" + i
                            NewClass.iri = a_temp.iri + "/" + i
                else:
                    with onto:
                        NewClass = types.new_class(i, (Thing,))
        onto.save(file=file_name, format="rdfxml")
        messagebox.showinfo("info", "Output file has been saved!")
    else:
        messagebox.showerror("Error", "Please enter a valid name for output file!")


def save_changes_to_existing_project_single_file():
    def save_as_project_frequentphrases(filename):
        if filename.endswith(".pkl"):
            filename = filename[:-4]
        name_main = filename.rsplit('/', 1)[-1]
        if filename and re.match("^[A-Za-z0-9_-]*$", name_main):
            global existing_project_flag
            existing_project_flag = 1
            global existing_project_path
            existing_project_path = filename
            output = name_main + '.pkl'
            dictionary = {}
            phrases_to_save = all_phrases
            concepts_to_save = main_concepts
            for i in main_concept_names:
                index = main_concept_names.index(i)
                x_mark = listbox_mark_concepts.itemcget(index, 'bg')
                concepts_to_save[index].set_concept_color_listmark(x_mark)
            axiom_color_to_save = []
            for i in axiom_color_edge:
                index = axiom_color_edge.index(i)
                axiom_color_to_save.append((i, axiom_color[index]))
            ontology_phrases_path_to_save = []
            for i in ontology_loaded_path_values:
                ontology_phrases_path_to_save.append(('ontology', i))
            for i in phrases_loaded_path_values:
                ontology_phrases_path_to_save.append(('phrases', i))
            for i in topics_loaded_path_values:
                ontology_phrases_path_to_save.append(('topics', i))
            existing_project_flag = 1
            dictionary["phrases"] = phrases_to_save
            dictionary["concepts"] = concepts_to_save
            dictionary["axiom_color"] = axiom_color_to_save
            dictionary["ontology_phrases_path"] = ontology_phrases_path_to_save
            dictionary["equivalent_concepts"] = equivalent_concepts_list
            dictionary["concept_name_style"] = concept_name_style_var.get()
            dictionary["topic_representative_info"] = topic_representative_info
            dictionary["Topics list"] = input_topics

            filename_check = filename + '.pkl'
            if os.path.isfile(filename_check) == False:
                filename_open = filename + '.pkl'
                os.path.join(filename, output)
                fp = open(filename_open, 'wb')
                pickle.dump(dictionary, fp)
                fp.close()

    global existing_project_flag
    global existing_project_path
    if existing_project_flag == 1 and existing_project_path != '':
        filename = existing_project_path + '.pkl'
        try:
            os.remove(filename)
        except OSError:
            pass
        if filename.endswith(".pkl"):
            filename = filename[:-4]
        name_main = filename.rsplit('/', 1)[-1]
        output = name_main + '.pkl'
        os.path.join(filename, output)
        save_as_project_frequentphrases(filename)
        m = "The changes has been saved to " + name_main
        messagebox.showinfo("info", m)
    else:
        info_window("You have not saved the project yet!", "Error", 3000)


def save_changes_to_existing_project_single_file():
    def save_as_project_frequentphrases(filename):
        if filename.endswith(".pkl"):
            filename = filename[:-4]
        name_main = filename.rsplit('/', 1)[-1]
        if filename and re.match("^[A-Za-z0-9_-]*$", name_main):
            global existing_project_flag
            existing_project_flag = 1
            global existing_project_path
            existing_project_path = filename
            output = name_main + '.pkl'
            dictionary = {}
            phrases_to_save = all_phrases
            concepts_to_save = main_concepts
            axiom_color_to_save = []
            for i in axiom_color_edge:
                index = axiom_color_edge.index(i)
                axiom_color_to_save.append((i, axiom_color[index]))
            ontology_phrases_path_to_save = []
            for i in ontology_loaded_path_values:
                ontology_phrases_path_to_save.append(('ontology', i))
            for i in phrases_loaded_path_values:
                ontology_phrases_path_to_save.append(('phrases', i))
            for i in topics_loaded_path_values:
                ontology_phrases_path_to_save.append(('topics', i))
            existing_project_flag = 1
            dictionary["FrequentPhrases_or_Topics"] = "FrequentPhrases"
            dictionary["phrases"] = phrases_to_save
            dictionary["concepts"] = concepts_to_save
            dictionary["axiom_color"] = axiom_color_to_save
            dictionary["ontology_phrases_path"] = ontology_phrases_path_to_save
            dictionary["equivalent_concepts"] = equivalent_concepts_list
            dictionary["concept_name_style"] = concept_name_style_var.get()
            dictionary["topic_labelling_info"] = topic_labelling_info
            dictionary["Topics list"] = input_topics
            filename_check = filename + '.pkl'
            if os.path.isfile(filename_check) == False:
                filename_open = filename + '.pkl'
                os.path.join(filename, output)
                fp = open(filename_open, 'wb')
                pickle.dump(dictionary, fp)
                fp.close()
    global existing_project_flag
    global existing_project_path
    if existing_project_flag == 1 and existing_project_path != '':
        filename = existing_project_path + '.pkl'
        try:
            os.remove(filename)
        except OSError:
            pass
        if filename.endswith(".pkl"):
            filename = filename[:-4]
        name_main = filename.rsplit('/', 1)[-1]
        output = name_main + '.pkl'
        os.path.join(filename, output)
        save_as_project_frequentphrases(filename)
        m = "The changes has been saved to " + name_main
        messagebox.showinfo("info", m)
    else:
        info_window("You have not saved the project yet!", "Error", 3000)


def save_new_project_using_dic():
    def save_as_new_project_frequentphrases(filename):
        name_main = filename.rsplit('/', 1)[-1]
        if filename and re.match("^[A-Za-z0-9_-]*$", name_main):
            global existing_project_flag
            existing_project_flag = 1
            global existing_project_path
            existing_project_path = filename
            output = name_main + '.pkl'
            dictionary = {}
            phrases_to_save = all_phrases
            concepts_to_save = main_concepts
            axiom_color_to_save = []
            for i in axiom_color_edge:
                index = axiom_color_edge.index(i)
                axiom_color_to_save.append((i, axiom_color[index]))
            ontology_phrases_path_to_save = []
            for i in ontology_loaded_path_values:
                ontology_phrases_path_to_save.append(('ontology', i))
            for i in phrases_loaded_path_values:
                ontology_phrases_path_to_save.append(('phrases', i))
            for i in topics_loaded_path_values:
                ontology_phrases_path_to_save.append(('topics', i))
            existing_project_flag = 1
            dictionary["phrases"] = phrases_to_save
            dictionary["concepts"] = concepts_to_save
            dictionary["axiom_color"] = axiom_color_to_save
            dictionary["ontology_phrases_path"] = ontology_phrases_path_to_save
            dictionary["equivalent_concepts"] = equivalent_concepts_list
            dictionary["concept_name_style"] = concept_name_style_var.get()
            dictionary["topic_labelling_info"] = topic_labelling_info
            dictionary["Topics list"] = input_topics
            filename_check = filename + '.pkl'
            if os.path.isfile(filename_check) == False:
                filename_open = filename + '.pkl'
                os.path.join(filename, output)
                fp = open(filename_open, 'wb')
                pickle.dump(dictionary, fp)
                fp.close()
                m = "Output file has been saved as: " + name_main
                messagebox.showinfo("info", m)
            else:
                result = messagebox.askquestion("Warning",
                                                "There is a file with the same name! \n Do you want to continue?",
                                                icon='warning')
                if result == 'yes':
                    os.remove(filename_check)
                    fp = open(output, 'wb')
                    pickle.dump(dictionary, fp)
                    fp.close()
                    m = "Output file has been saved as: " + name_main
                    messagebox.showinfo("info", m)
        else:
            messagebox.showerror("Error", "Please enter a valid project name!")

    myFormats = [("PICKLE files", "*.pkl")]
    filename = filedialog.asksaveasfilename(filetypes=myFormats)
    if filename:
        s = filename.rsplit('/')[-1]
        x = s.replace('.pkl', '')
        project_name = 'Project Name: ' + x + '     (' + filename + '.pkl' + ')'
        project_saved_path.config(text=project_name, font='Helvetica 11')
        save_as_new_project_frequentphrases(filename)


def restart():
    global p1
    p1.config(text='')
    global concept_name, concept_origin
    concept_name.config(text='')
    concept_origin.config(text='')
    global listbox1
    global listbox2
    listbox1.delete(0, END)
    listbox2.delete(0, END)
    listbox1_concept_names.delete(0, END)
    listbox2_concept_origin.delete(0, END)
    listbox1_concept_names_only.delete(0, END)
    listbox2_concept_origin_only.delete(0, END)
    listbox_mark_concepts.delete(0, END)
    listbox_mark_concepts_only.delete(0, END)
    input_phrases = []
    global phrases
    global all_phrases
    phrases.clear()
    all_phrases.clear()
    global main_relation_edge
    global listbox1_deleted
    global listbox1_deleted_index
    listbox1_deleted_index = -1
    listbox1_deleted = ''
    global listbox2_deleted
    global listbox2_deleted_index
    listbox2_deleted_index = -1
    listbox2_deleted = ''
    global listbox8_deleted
    global listbox8_deleted_index
    listbox8_deleted_index = -1
    listbox8_deleted = ''
    concept_name_style_var.set(0)
    global all_axioms
    all_axioms = []
    global x_position
    global y_position
    x_position = y_position = 0
    main_relation_edge = []
    global main_classes
    main_classes = []
    global relations_edge
    relations_edge = []
    global root
    global window_concept_axiom_view
    if window_concept_axiom_view:
        window_concept_axiom_view.destroy()
    global window_phrase_add_metadata_view
    if window_phrase_add_metadata_view:
        window_phrase_add_metadata_view.destroy()
    global window_concept_note_view
    if window_concept_note_view:
        window_concept_note_view.destroy()
    global window_phrase_note_view
    if window_phrase_note_view:
        window_phrase_note_view.destroy()
    global window_phrase_matching_view
    if window_phrase_matching_view:
        window_phrase_matching_view.destroy()
    if window_concept_only:
        window_concept_only.destroy()
    global window_concept_only_note_view
    if window_concept_only_note_view:
        window_concept_only_note_view.destroy()
    if window_TopicsPhrasesConcepts_note:
        window_TopicsPhrasesConcepts_note.destroy()
    if window_topic_representation:
        window_topic_representation.destroy()
    global window_topic_representation_focus_on_phrase
    if window_topic_representation_focus_on_phrase:
        window_topic_representation_focus_on_phrase.destroy()
    ontology_loaded_path.config(state="normal")
    phrases_loaded_path.config(state="normal")
    topics_loaded_path.config(state="normal")
    ontology_loaded_path.delete('1.0', END)
    phrases_loaded_path.delete('1.0', END)
    topics_loaded_path.delete('1.0', END)
    ontology_loaded_path_values.clear()
    phrases_loaded_path_values.clear()
    topics_loaded_path_values.clear()
    ontology_loaded_label.config(text="")
    phrases_loaded_label.config(text="")
    topics_loaded_label.config(text="")
    ontology_loaded_path.config(state="disabled")
    phrases_loaded_path.config(state="disabled")
    topics_loaded_path.config(state="disabled")
    global axiom_color_edge
    axiom_color_edge.clear()
    project_saved_path.config(text="")
    global load_super_sub_phrases_path
    load_super_sub_phrases_path = []
    global equivalent_concepts_list
    equivalent_concepts_list.clear()
    listbox1_topics_phrases.delete(0, END)
    listbox2_topics_phrases.delete(0, END)
    listbox_mark_topics_phrases.delete(0, END)
    topics_loaded_label.config(text="")
    topics_loaded_path.config(state="normal")
    topics_loaded_path.delete('1.0', END)
    topics_loaded_path.config(state="disabled")
    global topic_number
    global topics_with_phrase
    global input_topics
    input_topics = []
    topic_number = ['']
    topics_with_phrase = ['']
    topic_selection_2['values'] = topic_number
    topic_selection_2.set('')
    global topic_representative_info
    topic_representative_info = dict()
    try:
        notebook_main.forget(higher_view_topics_phrases_window)
        notebook_main.forget(higher_view_phrase_window)
        notebook_main.forget(higher_view_concept_only_window)
        notebook_main.forget(higher_view_concept_window)
    except:
        pass
    notebook_main.add(higher_view_phrase_window, text="Phrases \u279D Concepts")
    notebook_main.add(higher_view_topics_phrases_window, text="Topics \u279D Concepts")
    notebook_main.add(higher_view_concept_only_window, text="Concepts")
    notebook_main.add(higher_view_concept_window, text="Concepts \u279D Axioms")
    notebook_main.tab(1, state="disabled")
    notebook_main.tab(2, state="disabled")
    notebook_main.tab(3, state="disabled")
    notebook_main.tab(4, state="disabled")


def restart_new_ontology():
    global p1
    p1.config(text='')
    concept_origin.config(text='')
    listbox1_concept_names.delete(0, END)
    listbox2_concept_origin.delete(0, END)
    listbox_mark_concepts.delete(0, END)
    listbox1_concept_names_only.delete(0, END)
    listbox2_concept_origin_only.delete(0, END)
    listbox_mark_concepts_only.delete(0, END)
    global main_concept_names
    main_concept_names.clear()
    main_concepts.clear()
    global main_relation_edge
    global all_axioms
    all_axioms = []
    global x_position
    global y_position
    global previous_tab_id_concept
    global previous_tab_id_phrase_only
    global previous_tab_id_topic_phraseConcept
    global previous_tab_id
    global previous_tab_id_concept_only
    previous_tab_id_concept_only = 0
    previous_tab_id_concept = 0
    previous_tab_id_phrase_only = 0
    previous_tab_id_topic_phraseConcept = 0
    previous_tab_id = 0
    x_position = y_position = 0
    main_relation_edge = []
    global main_classes
    main_classes = []
    global relations_edge
    relations_edge = []
    global concepts
    global root


def new_project():
    restart()
    restart_new_ontology()
    global previous_tab_id
    global previous_tab_id
    previous_tab_id = 0
    global graph_ontology
    graph_ontology = rdflib.Graph()
    global ontology_help_owl
    global ontology_loaded_label
    global ontology_loaded_path
    ontology_loaded_path.config(state="normal")
    ontology_loaded_label.config(text="")
    ontology_loaded_path.delete('1.0', END)
    ontology_loaded_path.config(state="disabled")
    project_saved_path.config(text="")
    global existing_project_flag
    existing_project_flag = 0
    global existing_project_path
    existing_project_path = ''
    global phrases_loaded_label
    global phrases_loaded_path
    phrases_loaded_path.config(state="normal")
    phrases_loaded_label.config(text="")
    phrases_loaded_path.delete('1.0', END)
    phrases_loaded_path.config(state="disabled")
    window_mdo_info_view_set_up.destroy()
    global phrases
    global all_phrases
    global all_phrases_color
    phrases.clear()
    main_relation_edge.clear()
    relations_edge.clear()
    all_phrases.clear()
    listbox1.delete(0, END)
    listbox2.delete(0, END)
    notebook_main.select(load_necessary_files_window)


def open_a_working_project_single_file():
    project_path = filedialog.askopenfilename()
    if project_path:
        global previous_tab_id
        global previous_tab_id
        previous_tab_id = 0
        restart()
        new_project()
        try:
            filename = project_path
            s = filename.rsplit('/')[-1]
            x = s.replace('.pkl', '')
            project_name = 'Project Name: ' + x + '     (' + filename + ')'
            project_saved_path.config(text=project_name, font='Helvetica 11')
            input_file = open(filename, 'rb')
            dictionary = {}
            dictionary = pickle.load(input_file)
            try:
                notebook_main.forget(higher_view_phrase_window)
                notebook_main.forget(higher_view_topics_phrases_window)
                notebook_main.forget(higher_view_concept_only_window)
                notebook_main.forget(higher_view_concept_window)
            except:
                pass
            try:
                notebook_main.add(higher_view_phrase_window, text="Phrases \u279D Concepts")
                notebook_main.add(higher_view_topics_phrases_window, text="Topics \u279D Concepts")
                notebook_main.add(higher_view_concept_only_window, text="Concepts")
                notebook_main.add(higher_view_concept_window, text="Concepts \u279D Axioms")

                notebook_main.tab(1, state="normal")
                notebook_main.tab(2, state="normal")
                notebook_main.tab(3, state="normal")
                notebook_main.tab(4, state="normal")
            except:
                pass
            phrases_input_file = dictionary["phrases"]
            concepts_input_file = dictionary["concepts"]
            axiom_color_input_file = dictionary["axiom_color"]
            ontology_phrases_path_input_file = dictionary["ontology_phrases_path"]
            equivalent_concepts_input_file = dictionary["equivalent_concepts"]
            concept_name_style = dictionary["concept_name_style"]
            input_topics_list = dictionary["Topics list"]
            topic_labelling_info_list = dictionary['topic_labelling_info']
            concept_name_style_var.set(concept_name_style)
            flag = 1
            main_concepts.clear()
            main_concept_names.clear()
            for line in concepts_input_file:
                if flag == 1:
                    x = line
                    main_concept_names.append(x.get_concept_name())
                    main_concepts.append(x)
                    listbox1_concept_names.insert(END, x.get_concept_name())
                    listbox1_concept_names.itemconfig(END, fg=x.get_concept_color())
                    listbox1_concept_names_only.insert(END, x.get_concept_name())
                    listbox1_concept_names_only.itemconfig(END, fg=x.get_concept_color())
                    if (x.get_concept_color_listmark() == 'red'):
                        listbox1_concept_names.itemconfig(END, fg='red')
                        listbox1_concept_names_only.itemconfig(END, fg='red')
                else:
                    flag = 1
            flag = 1
            for line in phrases_input_file:
                if flag == 1:
                    x = line
                    phrases.append(x.get_phrase_name())
                    all_phrases.append(x)
                    listbox1.insert(END, x.get_phrase_name())
                    fg_color = x.get_phrase_color()
                    if fg_color and fg_color != " ":
                        listbox1.itemconfig(END, fg=fg_color)
                    if (x.get_phrase_listmark_color() == 'red'):
                        listbox1.itemconfig(END, fg='red')
                    fg_color = x.get_phrase_color()
                else:
                    flag = 1
            flag = 0
            axiom_color.clear()
            axiom_color_edge.clear()
            for line in axiom_color_input_file:
                if flag == 1:
                    axiom_color_edge.append(line[0])
                    relations_edge.append(line[0])
                    axiom_color.append(line[1])
                else:
                    flag = 1
            ontology_loaded_path.config(state="normal")
            phrases_loaded_path.config(state="normal")
            topics_loaded_path.config(state="normal")
            ontology_loaded_path.delete('1.0', END)
            phrases_loaded_path.delete('1.0', END)
            topics_loaded_path.delete('1.0', END)
            flag_ontology_path = 0
            flag_phrases_path = 0
            flag_topics_path = 0
            for line in ontology_phrases_path_input_file:
                if line[0] == 'ontology':
                    ontology_loaded_path.insert(END, line[1])
                    ontology_loaded_path.insert(END, '\n')
                    ontology_loaded_path_values.append(line[1])
                    flag_ontology_path = 1
                else:
                    if line[0] == 'phrases':
                        phrases_loaded_path.insert(END, line[1])
                        phrases_loaded_path.insert(END, '\n')
                        phrases_loaded_path_values.append(line[1])
                        flag_phrases_path = 1
                    else:
                        topics_loaded_path.insert(END, line[1])
                        topics_loaded_path.insert(END, '\n')
                        topics_loaded_path_values.append(line[1])
                        flag_topics_path = 1
            if flag_ontology_path == 1:
                ontology_loaded_label.config(text="The ontology has been loaded successfully!",
                                             font='Helvetica 11 bold')
            if flag_phrases_path == 1:
                phrases_loaded_label.config(text="The frequent phrases has been loaded successfully!",
                                            font='Helvetica 11 bold')
            if flag_topics_path == 1:
                topics_loaded_label.config(text="The Topics have been loaded successfully!", font='Helvetica 11 bold')
            ontology_loaded_path.config(state="disabled")
            phrases_loaded_path.config(state="disabled")
            topics_loaded_path.config(state="disabled")
            if ontology_loaded_path_values[0]:
                global ontology_help_owl
                ontology_help_owl = ontology_loaded_path_values[0]
            global existing_project_flag
            existing_project_flag = 1
            global existing_project_path
            existing_project_path = project_path
            if existing_project_path.endswith(".pkl"):
                existing_project_path = existing_project_path[:-4]

            equivalent_concepts_list.clear()
            for line in equivalent_concepts_input_file:
                equivalent_concepts_list.append(line)
            for line in input_topics_list:
                input_topics.append(line)
            global topic_representative_info
            global topic_number
            topic_number.clear()
            global topic_labelling_info
            topic_labelling_info = topic_labelling_info_list
            for path in topics_loaded_path_values:
                s = path.rsplit('/')[-1]
                x = s.replace('.txt', '')
                topic_number.append(x)
            topic_selection_2['values'] = topic_number
            try:
                topic_selection_2.current(0)
            except:
                pass
            listbox1_concept_names_only.selection_set(0)
            try:
                if window_concept_only:
                    window_concept_axiom_focus_view.destroy()
                if window_concept_only_note_view:
                    window_concept_only_note_view.destroy()
                curselection = listbox1_concept_names_only.curselection()[0]
                ph = listbox1_concept_names_only.get(curselection)
                if ph != '':
                    index = main_concept_names.index(ph)
                    cocenpt_only_tab1(ph)
                    concept_only_info(ph)
                    if previous_tab_id_concept_only == 0:
                        notebook_concepts_only.select(window_concept_only)
                    else:
                        notebook_concepts_only.select(window_concept_only_note_view)
            except:
                pass

            listbox1_concept_names.selection_set(0)
            try:
                if window_concept_axiom_focus_view:
                    window_concept_axiom_focus_view.destroy()
                if window_concept_note_view:
                    window_concept_note_view.destroy()
                curselection = listbox1_concept_names.curselection()[0]
                concept_name.config(text=listbox1_concept_names.get(curselection))
                ph = concept_name.cget("text")
                if ph != '':
                    index = main_concept_names.index(ph)
                    concept_origin.config(text=main_concepts[index].get_concept_origin())
                    concept_tab_axiom_view(ph)
                    concept_note(ph)
                    if previous_tab_id_concept == 0:
                        notebook_concepts.select(window_concept_axiom_view)
                    elif previous_tab_id_concept == 1:
                        notebook_concepts.select(window_concept_note_view)
            except:
                pass
            listbox1.selection_set(0)
            try:
                curselection = listbox1.curselection()[0]
                p1.config(text=listbox1.get(curselection))
                ph = p1.cget("text")
                if ph != '':
                    index = phrases.index(ph)
                    add_meta_data_tab(ph)
                    add_note_phrase(ph)
                    if previous_tab_id == 0:
                        notebook_phrases.select(window_phrase_add_metadata_view)
                    else:
                        notebook_phrases.select(window_phrase_note_view)
            except:
                pass
            try:
                topic_selection_2.current(0)
                j = topic_number.index(topic_selection_2.get())
                for item in input_topics[j]:
                    listbox1_topics_phrases.insert(END, item)
                listbox1_topics_phrases.selection_set(0)
                try:
                    curselection = listbox1_topics_phrases.curselection()[0]
                    ph = listbox1_topics_phrases.get(curselection)
                    if ph != '':
                        topic_representation_tab(ph)
                        add_focus_on_phrase_TopicsPhrasesConcepts(ph)
                        if previous_tab_id_topic_phraseConcept == 0:
                            notebook_topics_phrases.select(window_topic_representation)
                        if previous_tab_id_topic_phraseConcept == 1:
                            notebook_topics_phrases.select(window_topic_representation_focus_on_phrase)
                        if previous_tab_id_topic_phraseConcept == 2:
                            notebook_topics_phrases.select(window_TopicsPhrasesConcepts_note)
                except:
                    pass
            except:
                pass
        except:
            project_saved_path.config(text='', font='Helvetica 11')
            messagebox.showerror("Error", "The project cannot be loaded!")
            pass

def display_equivalent_concepts():
    global flag_display_equivalent_concepts
    global window_display_equivalent_concepts
    if flag_display_equivalent_concepts == 0:
        flag_display_equivalent_concepts = 1
        window_display_equivalent_concepts = Toplevel(root)
        window_display_equivalent_concepts.title("INFORMATION:   Equivalent Concepts")
        window_display_equivalent_concepts.geometry('')
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        window_display_equivalent_concepts.wm_iconphoto(False, photo)
        window_display_equivalent_concepts.configure(background='white')
        listbox_equivalent_concepts = Listbox(window_display_equivalent_concepts, borderwidth=0, highlightthickness=0, font='Helvetica 11')
        listbox_equivalent_concepts.pack(padx=10, pady=10)
        listbox_equivalent_concepts.config(width=0, height=0)
        counter = 0
        list_counter = 0
        if equivalent_concepts_list != []:
            for list in equivalent_concepts_list:
                list_counter += 1
                text = "List " + str(list_counter) + " : equivalmet concepts"
                listbox_equivalent_concepts.insert(END, text)
                listbox_equivalent_concepts.itemconfig(END, fg='black', bg='powderblue')
                for c in list:
                    listbox_equivalent_concepts.insert(END, c)
                    if counter == 0:
                        listbox_equivalent_concepts.itemconfig(END, fg='darkblue')
                    else:
                        listbox_equivalent_concepts.itemconfig(END, fg='darkred')
                listbox_equivalent_concepts.insert(END, '\n')
                if counter == 0:
                    counter = 1
                else:
                    counter = 0
        else:
            listbox_equivalent_concepts.insert(END, "There is no equivalent concepts to be displayed!")
        window_display_equivalent_concepts.focus()
    else:
        window_display_equivalent_concepts.destroy()
        flag_display_equivalent_concepts = 1
        window_display_equivalent_concepts = Toplevel(root)
        window_display_equivalent_concepts.title("INFORMATION:   Equivalent Concepts")
        window_display_equivalent_concepts.geometry('')
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        window_display_equivalent_concepts.wm_iconphoto(False, photo)
        window_display_equivalent_concepts.configure(background='white')
        listbox_equivalent_concepts = Listbox(window_display_equivalent_concepts, borderwidth=0, highlightthickness=0, font='Helvetica 11')
        listbox_equivalent_concepts.pack(padx=10, pady=10)
        listbox_equivalent_concepts.config(width=0, height=0)
        counter = 0
        list_counter = 0
        if equivalent_concepts_list != []:
            for list in equivalent_concepts_list:
                list_counter += 1
                text = "List " + str(list_counter) + " : equivalmet concepts"
                listbox_equivalent_concepts.insert(END, text)
                listbox_equivalent_concepts.itemconfig(END, fg='black', bg='powderblue')
                for c in list:
                    listbox_equivalent_concepts.insert(END, c)
                    if counter == 0:
                        listbox_equivalent_concepts.itemconfig(END, fg='darkblue')
                    else:
                        listbox_equivalent_concepts.itemconfig(END, fg='darkred')
                listbox_equivalent_concepts.insert(END, '\n')
                if counter == 0:
                    counter = 1
                else:
                    counter = 0
        else:
            listbox_equivalent_concepts.insert(END, "There is no equivalent concepts to be displayed!")
        window_display_equivalent_concepts.focus()

def display_topic_representative():
    def destroy_all_topic_representative_window(e):
        global flag_display_topic_representative
        flag_display_topic_representative = 0
    global window_display_topic_labelling
    global flag_display_topic_representative
    if flag_display_topic_representative == 0:
        flag_display_topic_representative = 1
        window_display_topic_labelling = Toplevel(root)
        window_display_topic_labelling.title("INFORMATION: Topic Represenatives list")
        window_display_topic_labelling.geometry("650x300+500+200")
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        window_display_topic_labelling.wm_iconphoto(False, photo)
        window_display_topic_labelling.configure(background='white')
        frame2 = Frame(window_display_topic_labelling)
        listbox_TR = Listbox(frame2, borderwidth=0, highlightthickness=0, font='Helvetica 11')
        scrollbary_listbox_TR = Scrollbar(frame2, command=scroll_view(listbox_TR))
        listbox_TR.bind("<MouseWheel>",lambda event: OnMouseWheel_function(e=event, listname=listbox_TR))
        listbox_TR.config(yscrollcommand=scrollbary_listbox_TR.set)
        scrollbary_listbox_TR.pack(side="right", fill=Y, expand=False)
        listbox_TR.pack(side="left", fill=BOTH, expand=True)
        frame2.pack(fill="both", expand=1)
        try:
            if topic_labelling_info.values() != False:
                flag_color = 0
                for i in topic_number:
                    for temp_node in topic_labelling_info[i]:
                        temp_node_topic_label = temp_node.get_topic_label()
                        temp_node_origin_topic = temp_node.get_origin_topic()
                        temp_node_selected_phrases = temp_node.get_representative_phrases()
                        last_index = listbox_TR.index(END)
                        text = "Origin topic--->" + str(temp_node_origin_topic)
                        listbox_TR.insert(END, text)
                        text = "Topic label--->"+ str(temp_node_topic_label)
                        listbox_TR.insert(END, text)
                        listbox_TR.insert(END, "Representative phrases--->")
                        for j in temp_node_selected_phrases:
                            listbox_TR.insert(END, j)
                        last_index_2 = listbox_TR.index(END)
                        while last_index < last_index_2:
                            if flag_color == 0:
                                listbox_TR.itemconfig(last_index, bg='powderblue')
                            else:
                                listbox_TR.itemconfig(last_index, bg='lightcyan')
                            last_index += 1
                        if flag_color == 0:
                            flag_color = 1
                        else:
                            flag_color = 0
        except:
            listbox_TR.insert(END, "There is no topic representative list to be displayed!")
        window_display_topic_labelling.focus()
        window_display_topic_labelling.bind("<Destroy>", destroy_all_topic_representative_window)
        listbox_TR.bind('<Double-Button-1>', lambda event: listbox_copy(listbox_TR, event))
    else:
        window_display_topic_labelling.destroy()
        flag_display_topic_representative = 1
        window_display_topic_labelling = Toplevel(root)
        window_display_topic_labelling.title("INFORMATION: Topic Represenatives list")
        window_display_topic_labelling.geometry("650x300+500+200")
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        window_display_topic_labelling.wm_iconphoto(False, photo)
        window_display_topic_labelling.configure(background='white')
        frame2 = Frame(window_display_topic_labelling)
        listbox_TR = Listbox(frame2, borderwidth=0, highlightthickness=0, font='Helvetica 11')
        scrollbary_listbox_TR = Scrollbar(frame2, command=scroll_view(listbox_TR))
        listbox_TR.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event, listname=listbox_TR))
        listbox_TR.config(yscrollcommand=scrollbary_listbox_TR.set)
        scrollbary_listbox_TR.pack(side="right", fill=Y, expand=False)
        listbox_TR.pack(side="left", fill=BOTH, expand=True)
        frame2.pack(fill="both", expand=1)
        try:
            if topic_labelling_info.values() != False:
                flag_color = 0
                for i in topic_number:
                    for temp_node in topic_labelling_info[i]:
                        temp_node_topic_label = temp_node.get_topic_label()
                        temp_node_origin_topic = temp_node.get_origin_topic()
                        temp_node_selected_phrases = temp_node.get_representative_phrases()
                        last_index = listbox_TR.index(END)
                        text = "Origin topic--->" + str(temp_node_origin_topic)
                        listbox_TR.insert(END, text)
                        text = "Topic label--->" + str(temp_node_topic_label)
                        listbox_TR.insert(END, text)
                        listbox_TR.insert(END, "Representative phrases--->")
                        for j in temp_node_selected_phrases:
                            listbox_TR.insert(END, j)
                        last_index_2 = listbox_TR.index(END)
                        while last_index < last_index_2:
                            if flag_color == 0:
                                listbox_TR.itemconfig(last_index, bg='powderblue')
                            else:
                                listbox_TR.itemconfig(last_index, bg='lightcyan')
                            last_index += 1
                        if flag_color == 0:
                            flag_color = 1
                        else:
                            flag_color = 0
        except:
            listbox_TR.insert(END, "There is no topic representative list to be displayed!")
        window_display_topic_labelling.focus()
        window_display_topic_labelling.bind("<Destroy>", destroy_all_topic_representative_window)
        listbox_TR.bind('<Double-Button-1>', lambda event: listbox_copy(listbox_TR, event))

def display_all_axioms():
    def destroy_all_axioms_window(e):
        global flag_display_all_axioms
        flag_display_all_axioms = 0
    global flag_display_all_axioms
    global window_display_all_axioms
    if flag_display_all_axioms == 0:
        flag_display_all_axioms = 1
        window_display_all_axioms = Toplevel(root)
        window_display_all_axioms.title("INFORMATION: Axioms of the Ontology")
        window_display_all_axioms.geometry("650x300+500+200")
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        window_display_all_axioms.wm_iconphoto(False, photo)
        window_display_all_axioms.configure(background='white')
        frame2 = Frame(window_display_all_axioms)
        listbox_all_axioms = Listbox(frame2, borderwidth=0, highlightthickness=0)
        scrollbary_listbox_all_axioms = Scrollbar(frame2, command=scroll_view(listbox_all_axioms))
        listbox_all_axioms.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event, listname=listbox_all_axioms))
        listbox_all_axioms.config(yscrollcommand=scrollbary_listbox_all_axioms.set)
        scrollbary_listbox_all_axioms.pack(side="right", fill=Y, expand=False)
        listbox_all_axioms.pack(side="left", fill=BOTH, expand=True)
        frame2.pack(fill="both", expand=1)
        bg_color_flag = 0
        if relations_edge != []:
            for edge in relations_edge:
                x = ' '.join(word[0].upper() + word[1:] for word in edge[0].split())
                y = ' '.join(word[0].upper() + word[1:] for word in edge[1].split())
                x1 = x.replace(" ", "")
                x2 = x1.replace("-", "")
                y1 = y.replace(" ", "")
                y2 = y1.replace("-", "")
                temp = x2 + '   is-a   ' + y2
                listbox_all_axioms.insert(END, temp)
                if bg_color_flag == 0:
                    listbox_all_axioms.itemconfig(END, bg='powderblue')
                    bg_color_flag = 1
                else:
                    listbox_all_axioms.itemconfig(END, bg='lightcyan')
                    bg_color_flag = 0
        else:
            listbox_all_axioms.insert(END, "There is no axiom to be displayed!")
        window_display_all_axioms.focus()
        window_display_all_axioms.bind("<Destroy>", destroy_all_axioms_window)
        listbox_all_axioms.bind('<Double-Button-1>', lambda event: listbox_copy(listbox_all_axioms, event))
    else:
        window_display_all_axioms.destroy()
        flag_display_all_axioms = 1
        window_display_all_axioms = Toplevel(root)
        window_display_all_axioms.title("INFORMATION: Axioms of the Ontology")
        window_display_all_axioms.geometry("650x300+500+200")
        ico = Image.open('p2o.png')
        photo = ImageTk.PhotoImage(ico)
        window_display_all_axioms.wm_iconphoto(False, photo)
        window_display_all_axioms.configure(background='white')
        frame2 = Frame(window_display_all_axioms)
        listbox_all_axioms = Listbox(frame2,borderwidth=0, highlightthickness=0)
        scrollbary_listbox_all_axioms = Scrollbar(frame2, command=scroll_view(listbox_all_axioms))
        listbox_all_axioms.bind("<MouseWheel>",lambda event: OnMouseWheel_function(e=event, listname=listbox_all_axioms))
        listbox_all_axioms.config(yscrollcommand=scrollbary_listbox_all_axioms.set)
        scrollbary_listbox_all_axioms.pack(side="right", fill=Y, expand=False)
        listbox_all_axioms.pack(side="left", fill=BOTH, expand=True)
        frame2.pack(fill="both", expand=1)
        bg_color_flag = 0
        if relations_edge != []:
            for edge in relations_edge:
                x = ' '.join(word[0].upper() + word[1:] for word in edge[0].split())
                y = ' '.join(word[0].upper() + word[1:] for word in edge[1].split())
                x1 = x.replace(" ", "")
                x2 = x1.replace("-", "")
                y1 = y.replace(" ", "")
                y2 = y1.replace("-", "")
                temp = x2 + '   is-a   ' + y2
                listbox_all_axioms.insert(END, temp)
                if bg_color_flag == 0:
                    listbox_all_axioms.itemconfig(END, bg='powderblue')
                    bg_color_flag = 1
                else:
                    listbox_all_axioms.itemconfig(END, bg='lightcyan')
                    bg_color_flag = 0
        else:
            listbox_all_axioms.insert(END, "There is no axiom to be displayed!")
        window_display_all_axioms.focus()
        window_display_all_axioms.bind("<Destroy>", destroy_all_axioms_window)
        listbox_all_axioms.bind('<Double-Button-1>', lambda event: listbox_copy(listbox_all_axioms, event))

def clear_searched_phrase():
    for item in phrases:
        i = phrases.index(item)
        listbox1.itemconfig(i, {'bg': 'white'})
    for item in main_concept_names:
        i = main_concept_names.index(item)
        listbox1_concept_names.itemconfig(i, {'bg': 'white'})

def clear_searched_concepts():
    for item in main_concept_names:
        i = main_concept_names.index(item)
        listbox1_concept_names.itemconfig(i, {'bg': 'white'})
        listbox1_concept_names_only.itemconfig(i, {'bg': 'white'})

def search_click_concepts(e):
    try:
        curselection = listbox_search.curselection()[0]
        search.delete(0, END)
        search.insert(0, listbox_search.get(curselection))
        clear_searched_concepts()
        s = listbox_search.get(curselection)
        i = main_concept_names.index(s)
        try:
            listbox1_concept_names.see(i)
            listbox1_concept_names.itemconfig(i, {'bg': 'lightBlue1'})
        except:
            pass
        global index_searched
        index_searched = i
        notebook_main.select(higher_view_concept_window)
    except:
        pass


def mdo_info():
    global main_classes_visualization
    main_classes_visualization.clear()
    for c in main_concept_names:
        main_classes_visualization.append(c)
    network_visualization()


def network_visualization():
    G = nx.DiGraph()
    for i in main_classes_visualization:
        G.add_node(i)
    for edge in relations_edge:
        if (edge[0] in main_classes_visualization) or (edge[1] in main_classes_visualization):
            i = axiom_color_edge.index(edge)
            x = axiom_color[i]
            G.add_edge(edge[0], edge[1], color=x)
    values = []
    for i in main_concept_names:
        index = main_concept_names.index(i)
        if main_concepts[index].get_concept_color() == 'black':
            values.append('r')
        else:
            values.append('b')
    colors = nx.get_edge_attributes(G, 'color').values()
    nodePos = nx.layout.fruchterman_reingold_layout(G)
    try:
        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.set_facecolor("blue")
        fig.set_facecolor("blue")
        nx.draw(G, nodePos, with_labels=True, edge_color=colors, node_color=values, arrows=True, node_size=8,
                font_size=9)
        network_visulaization_pyvis(G)
    except nx.NetworkXError:
        print("not found")


def network_visulaization_pyvis(G):
    nt = Network(width="1000px", height="700px", directed=True)
    temp_concepts = []
    for i in main_concept_names:
        t = i.replace(" ", "")
        temp_concepts.append(t)
    for node in G:
        index = main_concept_names.index(node)
        color = main_concepts[index].get_concept_color()
        if color == 'black':
            temp_color = 'red'
        else:
            temp_color = 'blue'
        nt.add_node(node, label=node, color=temp_color)
    for edge in axiom_color_edge:
        if (edge[0] in main_classes_visualization) or (edge[1] in main_classes_visualization):
            try:
                i = axiom_color_edge.index(edge)
                x = axiom_color[i]
                nt.add_edge(edge[0], edge[1], color=x)
            except:
                pass
    nt.show_buttons(filter_=['interaction', 'physics'])
    nt.show("nx.html", local=False)


def set_previous_tab_index_concepts_only(e):
    global previous_tab_id_concept_only
    try:
        previous_tab_id_concept_only = notebook_concepts_only.index(notebook_concepts_only.select())
    except:
        pass


def set_previous_tab_index_phrases(e):
    global previous_tab_id
    try:
        previous_tab_id = notebook_phrases.index(notebook_phrases.select())
    except:
        pass


def set_previous_tab_index_concepts(e):
    global previous_tab_id_concept
    try:
        previous_tab_id_concept = notebook_concepts.index(notebook_concepts.select())
    except:
        pass


def mark_phrase_done_button():
    p1.config(text=listbox1.get(ANCHOR))
    ph = p1.cget("text")
    if (ph != ''):
        i = phrases.index(ph)
        listbox1.itemconfig(i, fg='green')
        listbox2.itemconfig(i, fg='green')
        all_phrases[i].set_phrase_color('green')
        ph = phrases[i + 1]
        listbox1.selection_clear(i)
        global window_phrase_add_metadata_view
        if window_phrase_add_metadata_view:
            window_phrase_add_metadata_view.destroy()
        global window_phrase_matching_view
        if window_phrase_matching_view:
            window_phrase_matching_view.destroy()
        global window_phrase_note_view
        if window_phrase_note_view:
            window_phrase_note_view.destroy()
        if ph:
            try:
                index = phrases.index(ph)
                listbox1.activate(index)
                listbox1.selection_set(index)
                listbox1.select_anchor(index)
                p1.config(text=listbox1.get(index))
                add_meta_data_tab(ph)
                matching_tab(ph)
                add_note_phrase(ph)
                if previous_tab_id == 0:
                    notebook_phrases.select(window_phrase_add_metadata_view)
                else:
                    notebook_phrases.select(window_phrase_note_view)
                p1.config(text=listbox1.get(index))
            except:
                pass


def on_enter_label(e, message):
    toolTip.showtip(message)


def on_leave_label(e):
    toolTip.hidetip()


def yview_concept_view_only(*args):
    """ scroll both listboxes together """
    listbox1_concept_names_only.yview(*args)
    listbox2_concept_origin_only.yview(*args)
    listbox_mark_concepts_only.yview(*args)


def OnMouseWheel_concept_view_only(event):
    listbox1_concept_names_only.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox2_concept_origin_only.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox_mark_concepts_only.yview_scroll(-1 * int(event.delta / 120), "units")
    return "break"


def cocenpt_only_tab1(ph):
    global window_concept_only
    if window_concept_only:
        window_concept_only.destroy()
        window_concept_only = Frame(notebook_concepts_only, bg="white")
    Frame50 = Frame(window_concept_only, borderwidth=1, bg='white')
    Label(Frame50, text='Define a New Concept', bg='white', font='Helvetica 11 bold', fg='navy').grid(row=0,
                                                                                                      column=0)
    global textbox
    textbox = Text(Frame50, width=50, height=2, undo=True, borderwidth=2)
    textbox.grid(row=1, column=0, padx=5, sticky='w')
    Frame_note_temp = Frame(Frame50, borderwidth=0, bg='white')
    Label(Frame_note_temp, text='Comment', bg='white', font='Helvetica 11 bold', fg='navy').grid(row=0, column=0)
    textbox_note = Text(Frame_note_temp, width=50, height=7, undo=True, bg='azure')
    scrollbary_textbox_note = AutoScrollbar(Frame_note_temp, command=scroll_view(textbox_note))
    textbox_note.config(yscrollcommand=scrollbary_textbox_note.set)
    scrollbary_textbox_note.config(command=textbox_note.yview)
    textbox_note.grid(row=1, column=0)
    scrollbary_textbox_note.grid(row=1, column=1, sticky="ns")
    Frame_note_temp.grid(row=2, column=0, padx=5, pady=10)

    Button12 = Button(Frame50, text="Add to Concepts", width=15, fg='black', bg='lightBlue1', font=('comicsans', 12),
                      command=lambda: add_to_concepts_conceptonlytab((textbox.get("1.0", END)[:-1]), ph,
                                                                     (textbox_note.get('1.0', END)).strip()))
    Button12.grid(row=1, column=1, padx=10)
    Frame50.grid(row=3, column=0, padx=30, pady=20)
    notebook_concepts_only.add(window_concept_only, text="Define new concept")


def concept_only_info(ph):
    global window_concept_only_note_view
    if window_concept_only_note_view:
        window_concept_only_note_view.destroy()
        window_concept_only_note_view = Frame(notebook_concepts_only, bg="white")
    Frame20_only = Frame(window_concept_only_note_view, bg='white')
    Label(Frame20_only, text='Concept: ', bg='white', font='Helvetica 11 bold', fg='navy').grid(row=0, column=0,
                                                                                                sticky='w')
    Label(Frame20_only, text='Origin: ', bg='white', font='Helvetica 11 bold', fg='navy').grid(row=1, column=0,
                                                                                               sticky='w')
    concept_name_only = Label(Frame20_only, text='', bg='white', font='Helvetica 11')
    concept_name_only.grid(row=0, column=1, sticky='w')
    concept_origin_only = Label(Frame20_only, text='', bg='white', font='Helvetica 11')
    concept_origin_only.grid(row=1, column=1, sticky='w')
    Frame20_only.pack(side=TOP, anchor=W, padx=10, pady=10)
    curselection = listbox1_concept_names_only.curselection()[0]
    concept_name_only.config(text=listbox1_concept_names_only.get(curselection))
    ph = concept_name_only.cget("text")
    if ph != '':
        index = main_concept_names.index(ph)
        concept_origin_only.config(text=main_concepts[index].get_concept_origin())
    notebook_concepts_only.add(window_concept_only_note_view, text="Info on selected concept")


def add_to_concepts_conceptonlytab(text, ph, note):
    if text != "":
        global textbox
        temp_text = text
        temp_text_lower = text.lower()
        main_concept_names_lower = [c.lower() for c in main_concept_names]
        if temp_text not in main_concept_names and (temp_text_lower not in main_concept_names_lower):
            textbox.delete('1.0', END)
            temp_name = text
            if concept_name_style_var.get() == 1:
                temp_name = camelcase_concept_name(temp_name)
            main_concept_names.append(temp_name)
            x_concept = NodeType_concept(temp_name, [], [], 'darkred', 'darkred', "None (new concept)", note, '')
            main_concepts.append(x_concept)
            listbox1_concept_names.insert(END, temp_name)
            listbox2_concept_origin.insert(END, "")
            listbox_mark_concepts.insert(END, " ")
            listbox1_concept_names_only.insert(END, temp_name)
            listbox1_concept_names_only.see(END)
            i = listbox1_concept_names.get(0, END).index(temp_name)
            listbox1_concept_names.itemconfig(i, fg='darkred')
            listbox1_concept_names_only.itemconfig(i, fg='darkred')
            refresh_concept_only_tab(ph)
            text_temp = "The new concept: \"" + temp_name + "\" has been added to concepts list!"
            info_window(text_temp, "Info", 2000)
        else:
            messagebox.showerror("Error", "The extracted concept has already defined!")
        textbox.delete('1.0', END)


def refresh_concept_only_tab(ph):
    try:
        if ph != '':
            concept_origin.config(text=" ")
            global window_concept_only
            if window_concept_only:
                window_concept_only.destroy()
            global window_concept_only_note_view
            if window_concept_only_note_view:
                window_concept_only_note_view.destroy()
            cocenpt_only_tab1(ph)
            concept_only_info(ph)
            if previous_tab_id_concept_only == 0:
                notebook_concepts_only.select(window_concept_only)
            else:
                notebook_concepts_only.select(window_concept_only_note_view)
    except:
        pass


def click_on_concept_only(e):
    try:
        if window_concept_only:
            window_concept_axiom_focus_view.destroy()
        if window_concept_only_note_view:
            window_concept_only_note_view.destroy()
        curselection = listbox1_concept_names_only.curselection()[0]
        ph = listbox1_concept_names_only.get(curselection)
        if ph != '':
            index = main_concept_names.index(ph)
            cocenpt_only_tab1(ph)
            concept_only_info(ph)
            if previous_tab_id_concept_only == 0:
                notebook_concepts_only.select(window_concept_only)
            else:
                notebook_concepts_only.select(window_concept_only_note_view)
    except:
        pass

# =================Related to TOPICS========================
def save_phrase_note_TopicsPhrases(note, ph):
    index = phrases.index(ph)
    try:
        all_phrases[index].set_phrase_note(note)
        info_window("The note has been saved!", "Info", 2000)
    except:
        pass


def update_list_topic_phrases(e):
    global listbox1_topics_phrases
    global listbox2_topics_phrases
    global listbox_mark_topics_phrases
    global topic_label_previous_value
    topic_label_previous_value = ''
    global topic_comment_previous_value
    topic_comment_previous_value = ''
    listbox1_topics_phrases.delete(0, END)
    listbox2_topics_phrases.delete(0, END)
    listbox_mark_topics_phrases.delete(0, END)
    topic_selection_2.current(topic_number.index(topic_selection_2.get()))
    phrases_selected_for_topic_labeling.clear()
    try:
        j = topic_number.index(topic_selection_2.get())
        for item in input_topics[j]:
            listbox1_topics_phrases.insert(END, item)
            listbox2_topics_phrases.insert(END, " ")
            listbox_mark_topics_phrases.insert(END, " ")
            try:
                index_item = phrases.index(item)
                item_color = all_phrases[index_item].get_phrase_color()
                if item_color == 'green':
                    listbox1_topics_phrases.itemconfig(END, fg='green')
                index_item = phrases.index(item)
                bg_color = all_phrases[index_item].get_phrase_listbox_mark_color()

                if bg_color == 'red' or bg_color == 'darkred':
                    listbox_mark_topics_phrases.itemconfig(END, {'bg': 'red'})
                else:
                    listbox_mark_topics_phrases.itemconfig(END, {'bg': 'white'})
            except:
                pass
        global window_topic_representation
        if window_topic_representation:
            window_topic_representation.destroy()
        global window_TopicsPhrasesConcepts_note
        if window_TopicsPhrasesConcepts_note:
            window_TopicsPhrasesConcepts_note.destroy()
        global window_topic_representation_focus_on_phrase
        if window_topic_representation_focus_on_phrase:
            window_topic_representation_focus_on_phrase.destroy()
        try:
            listbox1_topics_phrases.selection_set(0)
            try:
                curselection = listbox1_topics_phrases.curselection()[0]
                ph = listbox1_topics_phrases.get(curselection)
                if ph != '':

                    topic_representation_tab(ph)
                    add_focus_on_phrase_TopicsPhrasesConcepts(ph)
                    if previous_tab_id_topic_phraseConcept == 0:
                        notebook_topics_phrases.select(window_topic_representation)
                    if previous_tab_id_topic_phraseConcept == 1:
                        notebook_topics_phrases.select(window_topic_representation_focus_on_phrase)
                    if previous_tab_id_topic_phraseConcept == 2:
                        notebook_topics_phrases.select(window_TopicsPhrasesConcepts_note)
            except:
                pass
        except:
            pass
    except:
        pass


def function_find_topics_contains_phrase(p, current_topic_index):
    result = []
    for item in input_topics:
        if p in item:
            index_temp = input_topics.index(item)
            result.append(topic_number[index_temp])
    return result


def click_on_phrase_TopicsPhrasesConceptTab_2(e=None):
    global single_or_double_click_topics
    if single_or_double_click_topics == 0:
        try:
            curselection = listbox1_topics_phrases.curselection()[0]
            ph = listbox1_topics_phrases.get(curselection)
            if ph != '':
                topic_representation_tab(ph)
                try:
                    [listbox_selected_phrases.insert(END, item) for item in phrases_selected_for_topic_labeling]
                except:
                    pass
                add_focus_on_phrase_TopicsPhrasesConcepts(ph)
                if previous_tab_id_topic_phraseConcept == 0:
                    notebook_topics_phrases.select(window_topic_representation)
                if previous_tab_id_topic_phraseConcept == 1:
                    notebook_topics_phrases.select(window_topic_representation_focus_on_phrase)
        except:
            pass


def click_on_phrase_TopicsPhrasesConceptTab(e=None):
    listbox1_topics_phrases.after(300,lambda :click_on_phrase_TopicsPhrasesConceptTab_2())


def topicslabels_include_a_phrase_function(e):
    topiclabel = topicslabels_include_a_phrase.get()
    topiclabel = topiclabel.strip()
    for i in topic_labelling_info:
        for temp in topic_labelling_info[i]:
            if temp.get_topic_label() == topiclabel:
                origin_topic = temp.get_origin_topic()
                try:
                    index = topic_number.index(origin_topic)
                    topic_selection_2.current(index)
                    global listbox1_topics_phrases
                    global listbox2_topics_phrases
                    listbox1_topics_phrases.delete(0, END)
                    listbox2_topics_phrases.delete(0, END)
                    topic_selection_2.current(topic_number.index(topic_selection_2.get()))
                    phrases_selected_for_topic_labeling.clear()
                    try:
                        j = topic_number.index(topic_selection_2.get())
                        for item in input_topics[j]:
                            listbox1_topics_phrases.insert(END, item)
                            listbox2_topics_phrases.insert(END, " ")
                            try:
                                index_item = phrases.index(item)
                                item_color = all_phrases[index_item].get_phrase_color()
                                if item_color == 'green':
                                    listbox1_topics_phrases.itemconfig(END, fg='green')
                                index_item = phrases.index(item)
                                bg_color = all_phrases[index_item].get_phrase_listbox_mark_color()
                                if bg_color == 'red' or bg_color == 'darkred':
                                    listbox_mark_topics_phrases.itemconfig(END, {'bg': 'red'})
                                else:
                                    listbox_mark_topics_phrases.itemconfig(END, {'bg': 'white'})
                            except:
                                pass
                        global window_topic_representation
                        if window_topic_representation:
                            window_topic_representation.destroy()
                        global window_topic_representation_focus_on_phrase
                        if window_topic_representation_focus_on_phrase:
                            window_topic_representation_focus_on_phrase.destroy()
                        try:
                            listbox1_topics_phrases.selection_set(0)
                            try:
                                curselection = listbox1_topics_phrases.curselection()[0]
                                ph = listbox1_topics_phrases.get(curselection)
                                if ph != '':
                                    topic_representation_tab(ph)
                                    add_focus_on_phrase_TopicsPhrasesConcepts()
                                    if previous_tab_id_topic_phraseConcept == 0:
                                        notebook_topics_phrases.select(window_topic_representation)
                                    if previous_tab_id_topic_phraseConcept == 1:
                                        notebook_topics_phrases.select(window_topic_representation_focus_on_phrase)
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass


def add_focus_on_phrase_TopicsPhrasesConcepts(ph):
    def OpenPhraseOtherTopcList_TopicsPhrasesConcepts(e):
        curselection = listbox1_topics_phrases.curselection()[0]
        ph = listbox1_topics_phrases.get(curselection)
        listbox1_topics_phrases.delete(0, END)
        listbox2_topics_phrases.delete(0, END)
        try:
            j = topic_number.index(topics_include_a_phrase_TopicsPhrasesConcepts.get())
            topic_n = j
            for item in input_topics[j]:
                listbox1_topics_phrases.insert(END, item)
                listbox2_topics_phrases.insert(END, " ")
            t = input_topics[j].index(ph)
            listbox1_topics_phrases.selection_clear(0, END)
            listbox1_topics_phrases.see(t)
            listbox1_topics_phrases.selection_set(t)
            topic_selection_2.current(topic_n)
            try:
                global topics_with_phrase
                if ph != '':
                    topics_phrase_in = function_find_topics_contains_phrase(ph, topic_selection_2.current())
                    for i in topics_phrase_in:
                        topics_with_phrase.append(i)
                    topic_representation_tab(ph)
                    add_focus_on_phrase_TopicsPhrasesConcepts(ph)
                    if previous_tab_id_topic_phraseConcept == 0:
                        notebook_topics_phrases.select(window_topic_representation)
                    if previous_tab_id_topic_phraseConcept == 1:
                        notebook_topics_phrases.select(window_topic_representation_focus_on_phrase)
            except:
                pass
        except:
            pass
    global window_topic_representation_focus_on_phrase
    if window_topic_representation_focus_on_phrase:
        window_topic_representation_focus_on_phrase.destroy()
        window_topic_representation_focus_on_phrase = Frame(notebook_topics_phrases, bg="white")
    Frame4_topics_phrases = Frame(window_topic_representation_focus_on_phrase, bg='white')
    Frame4_topics_phrases_temp = Frame(Frame4_topics_phrases, bg='white')
    Label(Frame4_topics_phrases_temp, text='Phrase: ', bg='white', font='Helvetica 12 bold', fg='navy').grid(row=0,
                                                                                                             column=0,
                                                                                                             sticky='w')
    p1_topics_phrases = Label(Frame4_topics_phrases_temp, text='', bg='white', font='Helvetica 12')
    p1_topics_phrases.grid(row=0, column=1, sticky='w')
    p1_topics_phrases.config(text=ph)
    Frame4_topics_phrases_temp.grid(row=0, column=0, sticky='w', pady=15)
    global topics_with_phrase
    topics_with_phrase = []
    Label(Frame4_topics_phrases, text='Topics that include the phrase: ', bg='white', font='Helvetica 11 bold',
          fg='navy').grid(row=2, column=0, sticky='w', pady=15)
    topics_include_a_phrase_TopicsPhrasesConcepts = tkinter.ttk.Combobox(Frame4_topics_phrases, state="readonly",
                                                                         value=topics_with_phrase, font='Helvetica 11')
    topics_include_a_phrase_TopicsPhrasesConcepts.bind("<<ComboboxSelected>>",
                                                       lambda e: OpenPhraseOtherTopcList_TopicsPhrasesConcepts(e))
    topics_include_a_phrase_TopicsPhrasesConcepts.grid(row=2, column=1, sticky='w', pady=15)
    global topiclabels_with_phrase
    topiclabels_with_phrase = []
    Label(Frame4_topics_phrases, text='Topic Labels related to the phrase:', bg='white', font='Helvetica 11 bold',
          fg='navy').grid(row=3, column=0, sticky='w', pady=15)
    topicslabels_include_a_phrase = tkinter.ttk.Combobox(Frame4_topics_phrases, state="readonly",
                                                         value=topiclabels_with_phrase)
    topicslabels_include_a_phrase.bind("<<ComboboxSelected>>", lambda e: topicslabels_include_a_phrase_function(e))
    topicslabels_include_a_phrase.grid(row=3, column=1, sticky='w', pady=15)
    Frame4_topics_phrases.pack(side=TOP, anchor=W, padx=10, pady=15)

    selection = topic_selection_2.current()
    topics_phrase_in = function_find_topics_contains_phrase(ph, selection)
    for i in topics_phrase_in:
        topics_with_phrase.append(i)
    topiclabels_with_phrase = function_find_topicslabels_contains_phrase(ph, selection)
    topics_include_a_phrase_TopicsPhrasesConcepts['values'] = topics_phrase_in
    topics_include_a_phrase_TopicsPhrasesConcepts.current(0)
    try:
        topicslabels_include_a_phrase['values'] = topiclabels_with_phrase
        topicslabels_include_a_phrase.current(0)
    except:
        pass
    notebook_topics_phrases.add(window_topic_representation_focus_on_phrase, text="Focus on selected phrase")


def add_note_TopicsPhrasesConcepts(ph):
    i = phrases.index(ph)
    global window_TopicsPhrasesConcepts_note
    if window_TopicsPhrasesConcepts_note:
        window_TopicsPhrasesConcepts_note.destroy()
        window_TopicsPhrasesConcepts_note = Frame(notebook_topics_phrases, bg="white")
    Frame_note = Frame(window_TopicsPhrasesConcepts_note, borderwidth=1, bg='white')
    Frame_note_temp = Frame(window_TopicsPhrasesConcepts_note, borderwidth=0, bg='white')
    textbox_note = Text(Frame_note_temp, width=100, height=25, undo=True, borderwidth=0)
    scrollbary_textbox_note = Scrollbar(Frame_note_temp, command=textbox_note.yview)
    textbox_note.config(yscrollcommand=scrollbary_textbox_note.set)
    textbox_note.pack(side="left", fill=Y, expand=False)
    scrollbary_textbox_note.pack(side="right", fill=Y, expand=False)
    Frame_note_temp.pack(fill='both', expand=True)
    b = Button(Frame_note, text="Save Note", width=15, fg='black', bg='lightBlue1', font=('comicsans', 12),
               command=lambda: save_phrase_note_TopicsPhrases((textbox_note.get("1.0", END)[:-1]), ph))
    b.pack(padx=1, pady=10)
    Frame_note.pack(fill='both', expand=True)
    textbox_note.delete('1.0', END)
    textbox_note.insert('1.0', all_phrases[i].get_phrase_note())
    text_temp = "Add note to selected phrase"
    notebook_topics_phrases.add(window_TopicsPhrasesConcepts_note, text=text_temp)


def topic_representation_tab(ph):
    def save_topic_representatives():
        topic_name = topic_selection_2.get()
        selected_phrases = listbox_selected_phrases.get(0, END)
        topic_label = textbox_topic_representative.get('1.0', 'end')
        topic_lable_comment = textbox_comment.get('1.0', 'end')
        t = re.sub('[^A-Za-z]+', ' ', topic_label)
        if selected_phrases != () and topic_label and topic_label != '\n':
            if (topic_labelling_info[topic_name] == []):
                listbox_topic_labels.delete(0, END)
            topic_label = topic_label.strip()
            topic_lable_comment = topic_lable_comment.strip()
            temp = NodeType_Topic_Labeling(topic_name, topic_label, selected_phrases, topic_lable_comment)
            topic_labelling_info[topic_name].append(temp)
            listbox_selected_phrases.delete(0, END)
            textbox_topic_representative.delete('1.0', END)
            textbox_comment.delete('1.0', END)
            listbox_topic_labels.insert(END, topic_label)
            info_window("The topic representative information has been saved!", "Info", 1500)
            global topicslabels_include_a_phrase
            topiclabels_with_phrase = function_find_topicslabels_contains_phrase(ph, topic_name)
            try:
                topicslabels_include_a_phrase['values'] = topiclabels_with_phrase
                topicslabels_include_a_phrase.current(0)
            except:
                pass
            for item in phrases_selected_for_topic_labeling:
                index_temp = listbox1_topics_phrases.get(0, END).index(item)
                listbox1_topics_phrases.itemconfig(index_temp, {'bg': 'white'})
            listbox1_topics_phrases.selection_clear(0, END)
            phrases_selected_for_topic_labeling.clear()
            global topic_label_previous_value
            topic_label_previous_value = ''
            global topic_comment_previous_value
            topic_comment_previous_value = ''
        else:
            info_window("The topic label or representative phrases are empty!", "Error", 3000)
    def click_on_selection_list(e):
        try:
            size = listbox_topic_labels.size()
            i = 0
            while i < size:
                if listbox_topic_labels.itemcget(i, "background") == 'paleturquoise':
                    listbox_topic_labels.itemconfig(i, {'bg': 'white'})
                i = i + 1
            representative_phrases_label.config(fg='white')
            comment_label.config(fg='white')
            textbox_comment_info.config(bg='white')
            textbox_comment_info.delete('1.0', END)
            topic_name = topic_selection_2.get()
            curselection = listbox_topic_labels.curselection()[0]
            listbox_topic_labels.selection_clear(0, END)
            listbox_topic_labels.itemconfig(curselection, {'bg': 'paleturquoise'})
            temp = curselection
            temp_node = topic_labelling_info[topic_name][int(temp)]
            temp_node_list_selected_phrases = temp_node.get_representative_phrases()
            listbox_representative_phrases.delete(0, END)
            if temp_node_list_selected_phrases:
                representative_phrases_label.config(fg='navy')
            for p in temp_node_list_selected_phrases:
                listbox_representative_phrases.insert(END, p)
                listbox_representative_phrases.itemconfig(END, {'bg': 'paleturquoise'})
            x = temp_node.get_comment()
            if temp_node.get_comment():
                textbox_comment_info.insert(END, temp_node.get_comment())
                comment_label.config(fg='navy')
                textbox_comment_info.config(bg='azure')
        except:
            pass
    def my_popup_add_topicRepresentative_to_concpets(e):
        size = listbox_topic_labels.size()
        i = 0
        selection = []
        while i < size:
            if listbox_topic_labels.itemcget(i, "background") == 'paleturquoise':
                selection.append(i)
                break
            i = i + 1
        if selection:
            item = selection[0]
            rootx = e.widget.winfo_rootx()
            rooty = e.widget.winfo_rooty()
            itemx, itemy, itemwidth, itemheight = e.widget.bbox(item)
            listbox_topic_labels_menu.tk_popup(rootx + e.widget.winfo_width() - 10, rooty + itemy + 10)
    def add_topiclabel_to_concepts():
        size = listbox_topic_labels.size()
        i = 0
        curselection = 0
        while i < size:
            if listbox_topic_labels.itemcget(i, "background") == 'paleturquoise':
                curselection = i
                break
            i = i + 1
        temp_concept = listbox_topic_labels.get(curselection)
        temp_text_lower = temp_concept.lower()
        main_concept_names_lower = [c.lower() for c in main_concept_names]
        if temp_concept not in main_concept_names and (temp_text_lower not in main_concept_names_lower):
            temp_name = temp_concept
            if concept_name_style_var.get() == 1:
                temp_name = camelcase_concept_name(temp_name)
            main_concept_names.append(temp_name)
            topic_name = topic_selection_2.get()
            temp_origin = 'Topic representative, ' + topic_name
            x_concept = NodeType_concept(temp_name, [], [], 'darkviolet', 'darkviolet', temp_origin, '', '')
            size = len(main_concepts)
            if size == 1:
                main_concepts[0] = x_concept
            else:
                main_concepts.append(x_concept)
            listbox1_concept_names_only.insert(END, temp_name)
            listbox2_concept_origin_only.insert(END, "")
            listbox_mark_concepts_only.insert(END, " ")
            listbox1_concept_names.insert(END, temp_name)
            listbox1_concept_names.see(END)
            listbox2_concept_origin.insert(END, "")
            listbox_mark_concepts.insert(END, " ")
            i = listbox1_concept_names.get(0, END).index(temp_name)
            listbox1_concept_names_only.itemconfig(i, fg='darkviolet')
            listbox1_concept_names.itemconfig(i, fg='darkviolet')
            notebook_main.tab(3, state="normal")
            notebook_main.tab(4, state="normal")
            info_window("The concept has been added to concepts list!", "Info", 1500)
        else:
            messagebox.showerror("Error", "The concept has already been defined!")
    def edit_topic_label():
        size = listbox_topic_labels.size()
        i = 0
        curselection = 0
        while i < size:
            if listbox_topic_labels.itemcget(i, "background") == 'paleturquoise':
                curselection = i
                break
            i = i + 1
        temp_topic_label = listbox_topic_labels.get(curselection)
        global topic_label_previous_value
        topic_label_previous_value = temp_topic_label
        textbox_topic_representative.delete("1.0", END)
        listbox_selected_phrases.delete(0, END)
        textbox_topic_representative.insert(END, temp_topic_label)
        global topic_comment_previous_value

        index = listbox_topic_labels.get(0, END).index(temp_topic_label)
        listbox_topic_labels.delete(index)

        topic_name = topic_selection_2.get()
        temp_representative_phrases = None
        temp_comment = None
        for temp in topic_labelling_info[topic_name]:
            if temp_topic_label == temp.get_topic_label():
                temp_representative_phrases = temp.get_representative_phrases()
                temp_comment = temp.get_comment()
                topic_comment_previous_value = temp_comment
                topic_labelling_info[topic_name].remove(temp)
                break
        for p in temp_representative_phrases:
            phrases_selected_for_topic_labeling.append(p)
            listbox_selected_phrases.insert(END, p)
            index_temp = listbox1_topics_phrases.get(0, END).index(p)
            listbox1_topics_phrases.itemconfig(index_temp, {'bg': 'lightcyan'})
            listbox1_topics_phrases.selection_clear(0, END)
        if temp_comment:
            textbox_comment.insert(END, temp_comment)
        representative_phrases_label.config(fg='white')
        comment_label.config(fg='white')
        textbox_comment_info.config(bg='white')
        textbox_comment_info.delete('1.0', END)
        listbox_representative_phrases.delete(0, END)
        listbox_selected_phrases.selection_clear(0, END)
    def save_topic_label_previous_value(e, text):
        global topic_label_previous_value
        topic_label_previous_value = text
    def save_comment_previous_value(e, text):
        global topic_comment_previous_value
        topic_comment_previous_value = text
    def on_leave_listbox_1(e):
        toolTip.hidetip()
    def on_motion_listbox(e, listname):
        index = listname.index("@%s,%s" % (e.x, e.y))
        if index >= 0:
            try:
                toolTip.hidetip()
                try:
                    toolTip.showtip(listname.get(index))
                except:
                    pass
            except:
                pass
    def select_all_representative_phrases():
        for item in listbox1_topics_phrases.get(0, END):
            if item not in phrases_selected_for_topic_labeling:
                phrases_selected_for_topic_labeling.append(item)
        for item in listbox1_topics_phrases.get(0, END):
            if item not in listbox_selected_phrases.get(0, END):
                listbox_selected_phrases.insert(END, item)
                index_value = listbox1_topics_phrases.get(0, "end").index(item)
                listbox1_topics_phrases.itemconfig(index_value, {'bg': 'lightcyan'})
    def clear_all_representative_phrases():
        phrases_selected_for_topic_labeling.clear()
        listbox_selected_phrases.delete(0, END)
        for item in listbox1_topics_phrases.get(0, END):
            #listbox_selected_phrases.insert(END, item)
            index_value = listbox1_topics_phrases.get(0, "end").index(item)
            listbox1_topics_phrases.itemconfig(index_value, {'bg': 'white'})
    global window_topic_representation
    if window_topic_representation:
        window_topic_representation.destroy()
        window_topic_representation = Frame(notebook_topics_phrases, bg="white")
    topic_name = topic_selection_2.get()
    if topic_name == '':
        topic_name = topic_number[0]
    F1 = Frame(window_topic_representation, bg='white')
    F1.pack(side="left", fill=Y, padx=1)
    F_topic_represantative_management = Frame(window_topic_representation, bg='white')
    F4 = Frame(F_topic_represantative_management, bg='white')
    Label(F4, text="Topic Label", bg='white', font='Helvetica 12 bold', fg='darkgreen').grid(row=0, column=0)
    textbox_topic_representative = Text(F4, width=35, height=2, undo=True, borderwidth=2, font='Helvetica 11 bold',
                                        highlightthickness=0)
    textbox_topic_representative.bind('<KeyRelease>', lambda e: save_topic_label_previous_value(e,
                                                                                                textbox_topic_representative.get(
                                                                                                    '1.0', END)))
    textbox_topic_representative.grid(row=1, column=0, padx=0)
    F4.grid(row=0, column=1, padx=5)
    F3 = Frame(F_topic_represantative_management, bg='white')
    Label(F3, text="Representative Phrases", bg='white', font='Helvetica 12 bold', fg='darkgreen').grid(row=0, column=0)
    global listbox_selected_phrases
    listbox_selected_phrases = Listbox(F3, width=40, height=5, font='Helvetica 11 bold', highlightthickness=0,borderwidth=2)
    listbox_selected_phrases.grid(row=1, column=0)
    scrollbary_listbox_selected_phrases = AutoScrollbar(F3, command=scroll_view(listbox_selected_phrases))
    scrollbary_listbox_selected_phrases.configure(command=listbox_selected_phrases.yview)
    listbox_selected_phrases.config(yscrollcommand=scrollbary_listbox_selected_phrases.set)
    scrollbary_listbox_selected_phrases.grid(row=1, column=1, sticky="ns")
    F3_2 = Frame(F3, bg='white')
    select_all_button = Button(F3_2,text="Add all phrases in topic list",width=20,fg='black',bg='paleturquoise',font=('comicsans',10),command=select_all_representative_phrases)
    clear_all_button = Button(F3_2,text="Clear all",width=9,fg='black',bg='paleturquoise',font=('comicsans', 10),command=clear_all_representative_phrases)
    select_all_button.grid(row=0, column=0, )
    clear_all_button.grid(row=0, column=1, padx=20)
    F3_2.grid(row=2, column=0, pady=10)
    F3.grid(row=0, column=0, padx=5)
    F_topic_represantative_management.pack(side=TOP, anchor=NW, pady=10)
    frame_comment = Frame(window_topic_representation, bg='white')
    Label(frame_comment, text="Comment for Topic Label", bg='white', font='Helvetica 12 bold', fg='darkgreen').grid(
        row=2, column=0)
    textbox_comment = Text(frame_comment, width=80, height=3, undo=True, borderwidth=1, font='Helvetica 11',
                           highlightthickness=0, bg="azure")
    textbox_comment.grid(row=3, column=0, padx=0)
    scrollbary_textbox_comment = AutoScrollbar(frame_comment, command=scroll_view(textbox_comment))
    scrollbary_textbox_comment.configure(command=textbox_comment.yview)
    textbox_comment.config(yscrollcommand=scrollbary_textbox_comment.set)
    scrollbary_textbox_comment.grid(row=3, column=1, sticky="ns")
    textbox_comment.bind('<KeyRelease>', lambda e: save_comment_previous_value(e,textbox_comment.get('1.0', END)))
    frame_comment.pack(side=TOP, anchor=NW, pady=10)
    F5 = Frame(window_topic_representation, bg='white')
    button_add_topic_representative = Button(F5, text="Add to Topic Labeling list", width=40, height=1, fg='black',
                                             bg='mediumaquamarine', font=('comicsans', 12),
                                             command=save_topic_representatives)
    button_add_topic_representative.grid(row=1, column=0)
    F5.pack(side=TOP, anchor=NW, pady=10, padx=112)
    F_topic_represantative_management_2 = Frame(window_topic_representation, bg='white')
    F6 = Frame(F_topic_represantative_management_2, bg='white')
    Label(F6, text="Topic Labels", bg='white', font='Helvetica 12 bold underline', fg='navy').grid(row=0, column=0)
    listbox_topic_labels = Listbox(F6, width=40, height=9, borderwidth=0, highlightthickness=0)
    listbox_topic_labels.bind("<<ListboxSelect>>", click_on_selection_list)
    listbox_topic_labels.bind("<Leave>", on_leave_listbox_1)
    listbox_topic_labels.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox_topic_labels))
    listbox_topic_labels_menu = Menu(F6, tearoff=False)
    listbox_topic_labels_menu.add_command(label="Create concept from Topic Label", command=add_topiclabel_to_concepts)
    listbox_topic_labels_menu.add_command(label="Edit", command=edit_topic_label)
    listbox_topic_labels.bind("<Button-3>", my_popup_add_topicRepresentative_to_concpets)
    listbox_topic_labels.grid(row=1, column=0)
    scrollbary_topic_labels = AutoScrollbar(F6, command=scroll_view(listbox_topic_labels))
    scrollbary_topic_labels.configure(command=listbox_topic_labels.yview)
    listbox_topic_labels.config(yscrollcommand=scrollbary_topic_labels.set)
    scrollbary_topic_labels.grid(row=1, column=1, sticky="ns")
    representative_phrases_label = Label(F6, text="Representative Phrases", bg='white',
                                         font='Helvetica 12 bold underline', fg='white')
    representative_phrases_label.grid(row=0, column=2)
    listbox_representative_phrases = Listbox(F6, width=35, height=9, borderwidth=0, highlightthickness=0)
    listbox_representative_phrases.grid(row=1, column=2)
    listbox_representative_phrases.bind('<Button-1>', lambda e: "break")
    scrollbary_representative_phrases = AutoScrollbar(F6, command=scroll_view(listbox_representative_phrases))
    scrollbary_representative_phrases.configure(command=listbox_representative_phrases.yview)
    listbox_representative_phrases.config(yscrollcommand=scrollbary_representative_phrases.set)
    scrollbary_representative_phrases.grid(row=1, column=3, sticky="ns")
    listbox_representative_phrases.bind("<Leave>", on_leave_listbox_1)
    listbox_representative_phrases.bind("<Motion>", lambda event: on_motion_listbox(e=event,
                                                                                    listname=listbox_representative_phrases))
    comment_label = Label(F6, text="Comment", bg='white', font='Helvetica 12 bold underline', fg='white')
    comment_label.grid(row=0, column=4)
    textbox_comment_info = Text(F6, width=35, height=9, borderwidth=0, highlightthickness=0)
    textbox_comment_info.grid(row=1, column=4)
    scrollbary_textbox_comment_info = AutoScrollbar(F6, command=scroll_view(textbox_comment_info))
    scrollbary_textbox_comment_info.configure(command=textbox_comment_info.yview)
    textbox_comment_info.config(yscrollcommand=scrollbary_textbox_comment_info.set)
    scrollbary_textbox_comment_info.grid(row=1, column=5, sticky="ns")
    F6.grid(row=0, column=0)
    F_topic_represantative_management_2.pack(side=TOP, anchor=NW)
    temp_nodes = topic_labelling_info[topic_name]
    listbox_selected_phrases.delete(0, END)
    textbox_topic_representative.delete('1.0', END)
    if temp_nodes:
        for i in temp_nodes:
            listbox_topic_labels.insert(END, i.get_topic_label())
    else:
        listbox_topic_labels.insert(END, 'There is no info to display!')
    if topic_label_previous_value != '':
        textbox_topic_representative.insert(END, topic_label_previous_value)
    if topic_comment_previous_value != '':
        textbox_comment.insert(END,topic_comment_previous_value)
    textbox_topic_representative.focus_set()
    notebook_topics_phrases.add(window_topic_representation, text="Topic labelling")


def set_previous_tab_index_topics_phrasesConcepts(e):
    global previous_tab_id_topic_phraseConcept
    try:
        previous_tab_id_topic_phraseConcept = notebook_topics_phrases.index(notebook_topics_phrases.select())
    except:
        pass

def export_concept_info_txt():
    myFormats = [("text Files", "*.txt")]
    filename = filedialog.asksaveasfilename(filetypes=myFormats)
    if filename:
        filename = filename + '.txt'
        mode = "w"
        with open(filename, mode) as output:  # file handle is auto-close
            for c in main_concepts:
                axioms = []
                name = c.get_concept_name()
                output.write("***********************************\n")
                output.write("Concept name:" + name)
                output.write("\n")
                r = c.get_concept_axioms()
                if r:
                    for item in r:
                        if "is-a" not in item:
                            temp = name + " is-a " + item
                            axioms.append(temp)
                        else:
                            axioms.append(item)
                r = c.get_super_concept_axioms()
                if r:
                    for item in r:
                        if "is-a" not in item:
                            temp = item + " is-a " + name
                            axioms.append(temp)
                        else:
                            axioms.append(item)
                if len(axioms) > 0:
                    output.write("Axioms:\n")
                j = 0
                while j < len(axioms):
                    output.write(str(axioms[j]) + "\n")
                    j += 1
                output.write("")
        output.close()
        messagebox.showinfo("info", "Output file has been saved!")
    else:
        messagebox.showerror("Error", "Please enter a valid name for output file!")

def export_topic_labelling_info_txt():
    myFormats = [("text Files", "*.txt")]
    filename = filedialog.asksaveasfilename(filetypes=myFormats)
    if filename:
        filename = filename + '.txt'
        mode = "w"
        with open(filename, mode) as output:  # file handle is auto-close
            if topic_labelling_info.values() != False:
                for i in topic_number:
                    for temp_node in topic_labelling_info[i]:
                        temp_node_topic_label = temp_node.get_topic_label()
                        temp_node_origin_topic = temp_node.get_origin_topic()
                        temp_node_selected_phrases = temp_node.get_representative_phrases()
                        output.write("***********************************\n")
                        text = "Origin topic--->" + str(temp_node_origin_topic)
                        output.write(text + '\n')
                        text = "Topic label--->"+ str(temp_node_topic_label)
                        output.write(text + '\n')
                        output.write("Representative phrases--->\n")
                        for j in temp_node_selected_phrases:
                            output.write(j+'\n')
        output.close()
        messagebox.showinfo("info", "Output file has been saved!")
    else:
        messagebox.showerror("Error", "Please enter a valid name for output file!")

def add_to_representative_phrases():
    try:
        curselection = listbox1_topics_phrases.curselection()
        value = listbox1_topics_phrases.get(curselection)
        if value not in listbox_selected_phrases.get(0, END):
            listbox1_topics_phrases.itemconfig(curselection, {'bg': 'lightcyan'})
            listbox_selected_phrases.insert(END, value)
            phrases_selected_for_topic_labeling.append(value)
    except:
        return None


def remove_from_representative_phrases():
    try:
        curselection = listbox1_topics_phrases.curselection()
        value = listbox1_topics_phrases.get(curselection)
        if value in listbox_selected_phrases.get(0, END):
            listbox1_topics_phrases.itemconfig(curselection, {'bg': 'white'})
            index_value = listbox_selected_phrases.get(0, "end").index(value)
            listbox_selected_phrases.delete(index_value)
            phrases_selected_for_topic_labeling.remove(value)
    except:
        return None


def my_popup_listbox1_topics_phrases_menu(e):
    currentselection = listbox1_topics_phrases.curselection()[0]
    selection = listbox1_topics_phrases.get(listbox1_topics_phrases.curselection()[0])
    if selection:
        x_position = e.widget.winfo_rootx()
        y_position = e.widget.winfo_rooty()
        itemx, itemy, itemwidth, itemheight = e.widget.bbox(currentselection)
        listbox1_topics_phrases_menu.tk_popup(x_position + e.widget.winfo_width() - 10, y_position + itemy + 10)


def add_or_remove_from_representative_phrases(e):
    global single_or_double_click_topics
    single_or_double_click_topics = 1
    try:

        curselection = listbox1_topics_phrases.curselection()
        value = listbox1_topics_phrases.get(curselection)
        if value not in listbox_selected_phrases.get(0, END):
            listbox1_topics_phrases.itemconfig(curselection, {'bg': 'lightcyan'})
            listbox_selected_phrases.insert(END, value)
            phrases_selected_for_topic_labeling.append(value)
            single_or_double_click_topics = 0
        else:
            listbox1_topics_phrases.itemconfig(curselection, {'bg': 'white'})
            index_value = listbox_selected_phrases.get(0, "end").index(value)
            listbox_selected_phrases.delete(index_value)
            phrases_selected_for_topic_labeling.remove(value)
            single_or_double_click_topics = 0


    except:
        pass


def mark_concept_only_menu():
    try:
        ph = listbox1_concept_names_only.get(ANCHOR)
        if ph != '':
            i = main_concept_names.index(ph)
            listbox1_concept_names.itemconfig(i, fg='red')
            listbox1_concept_names_only.itemconfig(i, fg='red')
            main_concept_names[i].set_concept_color_listmark('red')
    except:
        pass


def my_popup_listbox1_concept_only_view(e):
    currentselection = listbox1_concept_names_only.curselection()[0]
    selection = listbox1_concept_names_only.get(listbox1_concept_names_only.curselection()[0])
    if selection:
        x_position = e.widget.winfo_rootx()
        y_position = e.widget.winfo_rooty()
        itemx, itemy, itemwidth, itemheight = e.widget.bbox(currentselection)
        listbox_mark_concepts_only_menu.tk_popup(x_position + e.widget.winfo_width() - 10, y_position + itemy + 10)


def delete_concept_only_menu():
    try:
        ph = listbox1_concept_names_only.get(ANCHOR)
        if ph != '':
            i = main_concept_names.index(ph)
            if (('owl' not in main_concepts[i].get_concept_origin()) and (
                    main_concepts[i].get_concept_axioms() == []) and (
                    main_concepts[i].get_super_concept_axioms() == [])):
                listbox1_concept_names_only.delete(i)
                listbox1_concept_names.delete(i)
                main_concept_names.pop(i)
                main_concepts.pop(i)
                try:
                    for j in all_phrases:
                        if ph in j.get_ext_concepts():
                            t = j.get_ext_concepts()
                            t.remove(ph)
                            all_phrases[all_phrases.index(j)].set_ext_concepts(t)
                            break
                except:
                    pass
                info_window("The concept \"" + ph + "\" has been deleted successfully!", "Info", 2000)
            else:
                messagebox.showerror("Error",
                                     "The concept \"" + ph + "\" cannot be deleted from concepts! (In the current version of Phrase2Onto, you cannot delete concepts from main ontology or teh concepts that have any axioms.))")
    except:
        pass

def mark_concept_menu():
    try:
        concept_name.config(text=listbox1_concept_names.get(ANCHOR))
        ph = concept_name.cget("text")
        if ph != '':
            i = main_concept_names.index(ph)
            listbox1_concept_names.itemconfig(i, fg='red')
            listbox1_concept_names_only.itemconfig(i, fg='red')
            main_concept_names[i].set_concept_color_listmark('red')
    except:
        pass

def unmark_concept_menu():
    try:
        concept_name.config(text=listbox1_concept_names.get(ANCHOR))
        ph = concept_name.cget("text")
        if ph != '':
            i = main_concept_names.index(ph)
            color = main_concepts[i].get_concept_color()
            listbox1_concept_names.itemconfig(i, fg=color)
            listbox1_concept_names_only.itemconfig(i, fg=color)
            main_concept_names[i].set_concept_color_listmark('')
    except:
        pass


def delete_concept_menu():
    try:
        ph = listbox1_concept_names.get(ANCHOR)
        if ph != '':
            i = main_concept_names.index(ph)
            temp = main_concepts[i].get_concept_origin()
            if (('owl' not in main_concepts[i].get_concept_origin()) and (main_concepts[i].get_concept_axioms() == []) and (main_concepts[i].get_super_concept_axioms() == [])) :
                listbox1_concept_names_only.delete(i)
                listbox1_concept_names.delete(i)
                main_concept_names.pop(i)
                main_concepts.pop(i)
                try:
                    for j in all_phrases:
                        if ph in j.get_ext_concepts():
                            t = j.get_ext_concepts()
                            t.remove(ph)
                            all_phrases[all_phrases.index(j)].set_ext_concepts(t)
                            break
                except:
                    pass
                info_window("The concept \"" + ph + "\" has been deleted successfully!", "Info", 2000)
            else:
                messagebox.showerror("Error", "The concept \"" + ph + "\" cannot be deleted from concepts! (In the current version of Phrase2Onto, you cannot delete concepts from main ontology or teh concepts that have any axioms.))")
    except:
        pass


def unmark_concept_only_menu():
    try:
        ph = listbox1_concept_names_only.get(ANCHOR)
        if ph != '':
            i = main_concept_names.index(ph)
            color = main_concepts[i].get_concept_color()
            listbox1_concept_names.itemconfig(i, fg=color)
            listbox1_concept_names_only.itemconfig(i, fg=color)
            main_concept_names[i].set_concept_color_listmark('')
    except:
        pass

# *************************************************************
# *************************************************************
# *******************variables*********************************
global phrases
phrases = []
global all_phrases
all_phrases = [NodeType_phrase]
global topic_number
topic_number = ['']
global topic_representative_info
topic_representative_info = dict()
global root
root = Tk()
root.configure(background='white')
root.title('Phrase2Onto')
root.geometry("1100x630+100+1")
root.maxsize(width=1300, height=700)
s = ttk.Style()
s.configure('TNotebook.Tab', font=('URW Gothic L', '10', 'bold'))
global notebook_main
notebook_main = ttk.Notebook(root)
notebook_main.pack(expand=1, fill="both")
global graph_ontology
graph_ontology = rdflib.Graph()
ico = Image.open('p2o.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
global x_position
global y_position
x_position = y_position = 0
main_menu = Menu(root, tearoff=False)
root.config(menu=main_menu)
file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu=file_menu)
save_menu = Menu(file_menu, tearoff=False)
file_menu.add_command(label="New project", command=new_project)
file_menu.add_separator()
file_menu.add_command(label="Open project", command=open_a_working_project_single_file)
file_menu.add_separator()
file_menu.add_cascade(label="Save", menu=save_menu)
file_menu.add_separator()
save_menu.add_command(label="Save as new project", command=save_new_project_using_dic)
save_menu.add_separator()
save_menu.add_command(label="Save changes to current project", command=save_changes_to_existing_project_single_file)
save_menu.add_separator()
save_menu.add_command(label="Save as Excel", command=save_as_excel_FrequentPhrases)  # outpute_file
save_menu.add_separator()
save_menu.add_command(label="Save as OWL (just ontology)", command=save_as_owl)
file_menu.add_command(label="Exit", command=exit_program)
global index_searched
index_searched = -1
find_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Options", menu=find_menu)
find_menu.add_command(label="Find", command=find_window)
find_menu.add_separator()
find_menu.add_command(label="Display all axioms", command=display_all_axioms)
find_menu.add_separator()
find_menu.add_command(label="Display equivalent concepts", command=display_equivalent_concepts)
find_menu.add_separator()
find_menu.add_command(label="Display Topic Labelling Info", command=display_topic_representative)

find_menu.add_separator()
find_menu.add_command(label="Export concepts info to text file", command=export_concept_info_txt)
find_menu.add_separator()
find_menu.add_command(label="Export topic labelling to text file", command=export_topic_labelling_info_txt)

visualize_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Ontology Visualization", menu=visualize_menu)
visualize_menu.add_command(label="Display ontology visualization in browser", command=mdo_info)

global topic_label_previous_value
topic_label_previous_value = ''
global topic_comment_previous_value
topic_comment_previous_value = ''

global main_concept_names
main_concept_names = []
global main_concepts
main_concepts = [NodeType_concept]

global existing_project_flag
existing_project_flag = 0
global existing_project_path
existing_project_path = ''

global load_necessary_files_window
load_necessary_files_window = Frame(notebook_main, bg="white")
l1 = Label(load_necessary_files_window, text='1:', bg='white', font='Helvetica 12 bold')
l1.grid(row=0, column=0, padx=10, pady=20)
load_ontology_button = Button(load_necessary_files_window, text="Load Ontology", fg='black', bg='lightBlue1',
                              font=('comicsans', 11), command=load_ontology, width=20)
load_ontology_button.grid(row=0, column=2, padx=0, pady=20)

global ontology_loaded_label
ontology_loaded_label = Label(load_necessary_files_window, text='', bg='white', fg='navy')
ontology_loaded_label.grid(row=0, column=3, padx=10, pady=5, sticky='w')
global project_saved_path
project_saved_path = Label(load_necessary_files_window, text='', bg='white', fg='navy')
project_saved_path.grid(row=6, column=3, pady=5, sticky='w')
global ontology_loaded_path
ontology_loaded_path = Text(load_necessary_files_window, font=('comicsans', 9), borderwidth=0, height=5, wrap=WORD,
                            width=70)
ontology_loaded_path.config(state="disabled")
ontology_loaded_path.grid(row=1, column=3, padx=10, sticky='w')

global ontology_loaded_path_values
ontology_loaded_path_values = []
global phrases_loaded_path_values
phrases_loaded_path_values = []
global topics_loaded_path_values
topics_loaded_path_values = []
global topics_or_phrases_var
topics_or_phrases_var = IntVar()
topics_or_phrases_var.set(-1)
global flag_change_load_topics_frequentPhrases
flag_change_load_topics_frequentPhrases = -1

l2 = Label(load_necessary_files_window, text='2:', bg='white', font='Helvetica 12 bold')
l2.grid(row=2, column=0, padx=10, pady=40)

load_phrases_button = Button(load_necessary_files_window, text="Load Frequent Phrases", fg='black', bg='lightBlue1',
                             font=('comicsans', 11), command=load_phrases, width=20)
load_phrases_button.grid(row=2, column=2, padx=0, pady=40)
global phrases_loaded_label
phrases_loaded_label = Label(load_necessary_files_window, text='', bg='white', fg='navy')
phrases_loaded_label.grid(row=2, column=3, padx=10, pady=5, sticky='w')
global phrases_loaded_path
phrases_loaded_path = Text(load_necessary_files_window, font=('comicsans', 9), borderwidth=0, height=5, wrap=WORD,
                           width=90)
phrases_loaded_path.grid(row=3, column=3, padx=5, sticky='w')

l3 = Label(load_necessary_files_window, text='3:', bg='white', font='Helvetica 12 bold')
l3.grid(row=4, column=0, padx=10, pady=40)
load_topics_button = Button(load_necessary_files_window, text="Load Topics", fg='black', bg='lightBlue1',
                            font=('comicsans', 11), command=load_topics, width=20)
load_topics_button.grid(row=4, column=2, padx=0, pady=40)
global topics_loaded_label
topics_loaded_label = Label(load_necessary_files_window, text='', bg='white', fg='navy')
topics_loaded_label.grid(row=4, column=3, padx=10, pady=5, sticky='w')

global topics_loaded_path
topics_loaded_path = Text(load_necessary_files_window, font=('comicsans', 9), borderwidth=0, height=5, wrap=WORD,
                          width=90)
topics_loaded_path.grid(row=5, column=3, padx=5, sticky='w')

ontology_loaded_path.config(state="disabled")
phrases_loaded_path.config(state="disabled")
topics_loaded_path.config(state="disabled")

Frame_conceptN_style = Frame(load_necessary_files_window, borderwidth=1, bg='lightBlue1')  # whitesmoke
Label(Frame_conceptN_style, text='Select Concept Names Style', bg='white', font='Helvetica 11 bold',
      fg='navy').grid(row=0, column=1, sticky='W')
global concept_name_style_var
concept_name_style_var = IntVar()
concept_name_style_var.set(0)
b1 = Radiobutton(Frame_conceptN_style, text="No-Style", variable=concept_name_style_var, value=0,
                 bg='lightBlue1')
b1.grid(row=1, column=1, sticky='W')
b2 = Radiobutton(Frame_conceptN_style, text="CamelCase-Style", variable=concept_name_style_var, value=1,
                 bg='lightBlue1')
b2.grid(row=2, column=1, sticky='W')
Frame_conceptN_style.grid(row=1, column=5, padx=0, pady=5, sticky='w')

global notebook_set_up
notebook_set_up = ttk.Notebook(load_necessary_files_window)
notebook_main.add(load_necessary_files_window, text="Set-up")
load_phrases_button.bind("<Enter>", lambda e: on_enter_label(e, "Load TEXT file\\files of frequent phrases"))
load_phrases_button.bind("<Leave>", on_leave_label)
load_ontology_button.bind("<Enter>", lambda e: on_enter_label(e, "Load OWL file\\files of ontology"))
load_ontology_button.bind("<Leave>", on_leave_label)
load_topics_button.bind("<Enter>", lambda e: on_enter_label(e, "Load TEXT files of topics"))
load_topics_button.bind("<Leave>", on_leave_label)

global higher_view_concept_window
higher_view_concept_window = Frame(notebook_main, bg="white")

global input_phrases
input_phrases = []
global input_topics
input_topics = []

global equivalent_concepts_list
equivalent_concepts_list = []

global load_super_sub_phrases_path
load_super_sub_phrases_path = []
global load_super_sub_phrases_path_topics
load_super_sub_phrases_path_topics = []

global flag_find_window
global flag_topmine_window
flag_find_window = 0
global flag_find_window_phrases
flag_find_window_phrases = 0
global flag_find_window_concepts
flag_find_window_concepts = 0
global flag_find_window_axioms
flag_find_window_axioms = 0
flag_topmine_window = 0
global flag_display_all_axioms
flag_display_all_axioms = 0
global flag_display_topic_representative
flag_display_topic_representative = 0
global flag_display_equivalent_concepts
flag_display_equivalent_concepts = 0

global main_relation_edge
global listbox1_concept_deleted
global listbox1_concept_deleted_index
listbox1_concept_deleted_index = -1
listbox1_concept_deleted = ''
global listbox2_concept_deleted
global listbox2_concept_deleted_index
listbox2_concept_deleted_index = -1
listbox2_concept_deleted = ''

global listbox1_deleted
global listbox1_deleted_index
listbox1_deleted_index = -1
listbox1_deleted = ''
global listbox2_deleted
global listbox2_deleted_index
listbox2_deleted_index = -1
listbox2_deleted = ''
global listbox8_deleted
global listbox8_deleted_index
listbox8_deleted_index = -1
listbox8_deleted = ''
global all_axioms
global previous_tab_id
previous_tab_id = 0

global previous_tab_id_concept
previous_tab_id_concept = 0

all_axioms = []
main_relation_edge = []
global main_classes
main_classes = []
global main_classes_visualization
main_classes_visualization = []
global relations_edge
relations_edge = []
network_colors = []

global concepts
global ontology_help_owl
ontology_help_owl = ''
global refined_var
refinded_var = IntVar()
global state_add_concpet_var
state_add_concpet_var = IntVar()
global axiom_direction
axiom_direction = IntVar()
axiom_direction.set(-1)
all_phrases = []
all_phrases_color = []
stop_flag = False

global topic_labelling_info
topic_labelling_info = dict()
global previous_tab_id_topic_phraseConcept
previous_tab_id_topic_phraseConcept = 0

global higher_view_topics_phrases_window
higher_view_topics_phrases_window = Frame(notebook_main, bg="white")

global notebook_TopicsPhrases
notebook_TopicsPhrases = ttk.Notebook(higher_view_topics_phrases_window)

global phrases_selected_for_topic_labeling
phrases_selected_for_topic_labeling = []

Frame10_topics_phrases = Frame(higher_view_topics_phrases_window, bg='white')
Frame1_topics_phrases = Frame(Frame10_topics_phrases, bg='white')
Frame_temp_topics_phrases = Frame(Frame1_topics_phrases, bg='white')
Label(Frame_temp_topics_phrases, text='Select the Topic List:   ', bg='white', font='Helvetica 12 bold',
      fg='navy').pack(side="left")
topic_selection_2 = tkinter.ttk.Combobox(Frame_temp_topics_phrases, state="readonly", value=topic_number)
topic_selection_2.current(0)
topic_selection_2.bind("<<ComboboxSelected>>", lambda e: update_list_topic_phrases(e))
topic_selection_2.pack(side="left")
Frame_temp_topics_phrases.pack()
listbox_mark_topics_phrases = Listbox(Frame1_topics_phrases, width=8, highlightthickness=0, borderwidth=0.5)
listbox1_topics_phrases = Listbox(Frame1_topics_phrases, width=50, exportselection=False)
listbox2_topics_phrases = Listbox(Frame1_topics_phrases, width=10)
scrollbary_topics_phrases = Scrollbar(Frame1_topics_phrases, command=yview_main_topics_phrases())

listbox1_topics_phrases.bind("<MouseWheel>", OnMouseWheel_topics_phrases)
listbox2_topics_phrases.bind("<MouseWheel>", OnMouseWheel_topics_phrases)
listbox1_topics_phrases.config(yscrollcommand=scrollbary_topics_phrases.set)
listbox2_topics_phrases.config(yscrollcommand=scrollbary_topics_phrases.set)
scrollbary_topics_phrases.pack(side="right", fill=Y, expand=False)
global single_or_double_click_topics
single_or_double_click_topics = 0
listbox1_topics_phrases.bind("<Double-Button-1>", add_or_remove_from_representative_phrases)
listbox1_topics_phrases.bind("<<ListboxSelect>>", click_on_phrase_TopicsPhrasesConceptTab)
listbox1_topics_phrases.pack(side="left", fill=BOTH, expand=True)
listbox2_topics_phrases.pack_forget()
Frame1_topics_phrases.pack(side="left", fill=Y, padx=1)
Frame10_topics_phrases.pack(side="left", fill=Y, padx=5, pady=5)

for item in input_topics:
    for t in item:
        listbox1_topics_phrases.insert(END, item)
        listbox2_topics_phrases.insert(END, " ")
        listbox_mark_topics_phrases.insert(END, " ")

global listbox_selected_phrases
listbox1_topics_phrases_menu = Menu(Frame1_topics_phrases, tearoff=False)
listbox1_topics_phrases_menu.add_command(label="Add to Representative Phrases", command=add_to_representative_phrases)
listbox1_topics_phrases_menu.add_command(label="Remove from Representative Phrases",command=remove_from_representative_phrases)
listbox1_topics_phrases.bind("<Button-3>", my_popup_listbox1_topics_phrases_menu)

global notebook_topics_phrases
notebook_topics_phrases = ttk.Notebook(higher_view_topics_phrases_window)
notebook_topics_phrases.pack(side=LEFT, fill=BOTH, expand=1, pady=20)
notebook_topics_phrases.bind('<<NotebookTabChanged>>', set_previous_tab_index_topics_phrasesConcepts)
global window_TopicsPhrasesConcepts_note
window_TopicsPhrasesConcepts_note = Frame(notebook_topics_phrases, width=950, height=450, bg="white")
global window_topic_representation
window_topic_representation = Frame(notebook_topics_phrases, width=950, height=450, bg="white")

global window_topic_representation_focus_on_phrase
window_topic_representation_focus_on_phrase = Frame(notebook_topics_phrases, width=950, height=450, bg="white")
# =========higher_view_phrases_only_window=================
# ============higher_view_phrase_window==================
global higher_view_phrase_window
higher_view_phrase_window = Frame(notebook_main, bg="white")
Frame10 = Frame(higher_view_phrase_window, bg='white')
Frame1 = Frame(Frame10, bg='white')
Frame_temp = Frame(Frame1, bg='white')
Label(Frame_temp, text='Phrases List      ', bg='white', font='Helvetica 12 bold', fg='navy').pack(side="left")
Frame_temp.pack()
listbox1 = Listbox(Frame1, width=50, exportselection=False)
listbox2 = Listbox(Frame1, width=10)
scrollbary = Scrollbar(Frame1, command=yview_main)
listbox1.bind("<MouseWheel>", OnMouseWheel)
listbox2.bind("<MouseWheel>", OnMouseWheel)
listbox1.config(yscrollcommand=scrollbary.set)
listbox2.config(yscrollcommand=scrollbary.set)
scrollbary.pack(side="right", fill=Y, expand=False)
listbox1.pack(side="left", fill=BOTH, expand=True)
listbox2.pack_forget()
Frame1.pack(side="left", fill=Y, padx=1)
Frame10.pack(side="left", fill=Y, padx=5, pady=5)
for item in phrases:
    i = phrases.index(item)
    listbox1.insert(END, item)
    listbox2.insert(END, all_phrases[i].get_validation_label())
listbox1.bind("<<ListboxSelect>>", click_on_phrase)
Frame4 = Frame(higher_view_phrase_window, bg='white')
Label(Frame4, text='Phrase: ', bg='white', font='Helvetica 10 bold', fg='navy').grid(row=0, column=0, sticky='w')
Label(Frame4, text='Label: ', bg='white', font='Helvetica 10 bold', fg='white').grid(row=1, column=0, sticky='w')
p1 = Label(Frame4, text='', bg='white')
p1.grid(row=0, column=1, sticky='w')
Button2 = Button(Frame4, text="Mark phrase as DONE", width=20, fg='black', bg='paleturquoise', font=('comicsans', 10),
                 command=mark_phrase_done_button).grid(row=0, column=2, sticky='e', padx=50)
Frame4.pack(side=TOP, anchor=W, padx=10, pady=1)
listbox1_menu = Menu(Frame1, tearoff=False)
listbox1_menu.add_command(label="Flag this phrase", command=mark_phrase_menu)
listbox1_menu.add_command(label="Unflag this phrase", command=unmark_phrase_menu)
listbox1_menu.add_command(label="Mark as Done", command=mark_phrase_done)
listbox1_menu.add_command(label="UnMark as Done", command=unmark_phrase_done)
listbox1.bind("<Button-3>", my_popup_3)
global notebook_phrases
notebook_phrases = ttk.Notebook(higher_view_phrase_window)
notebook_phrases.pack(side=LEFT, fill=BOTH, expand=1)
notebook_phrases.bind('<<NotebookTabChanged>>', set_previous_tab_index_phrases)

global window_phrase_add_metadata_view
window_phrase_add_metadata_view = Frame(notebook_phrases, width=950, height=450, bg="white")
global window_phrase_matching_view
window_phrase_matching_view = Frame(notebook_phrases, width=950, height=450, bg="white")
global window_phrase_note_view
window_phrase_note_view = Frame(notebook_phrases, width=950, height=450, bg="white")
global window_mdo_info_view_set_up
window_mdo_info_view_set_up = Frame(notebook_set_up, width=900, height=450, bg="white")

global axiom_color_edge
axiom_color_edge = []
global axiom_color
axiom_color = []

global higher_view_concept_only_window
higher_view_concept_only_window = Frame(notebook_main, bg="white")

Frame1_concept_view_only = Frame(higher_view_concept_only_window, bg='white')
Frame_temp_only = Frame(Frame1_concept_view_only, bg='white')
Label(Frame_temp_only, text='Concepts list', bg='white', font='Helvetica 12 bold', fg='navy').pack(side="left")
Frame_temp_only.pack()

global listbox1_concept_names_only
global listbox2_concept_origin_only
global listbox_mark_concepts_only

listbox_mark_concepts_only = Listbox(Frame1_concept_view_only, width=3)
listbox1_concept_names_only = Listbox(Frame1_concept_view_only, width=50, exportselection=False)
listbox2_concept_origin_only = Listbox(Frame1_concept_view_only, width=10)

scrollbary_only = Scrollbar(Frame1_concept_view_only, command=yview_concept_view_only)
listbox1_concept_names_only.bind("<MouseWheel>", OnMouseWheel_concept_view_only)
listbox2_concept_origin_only.bind("<MouseWheel>", OnMouseWheel_concept_view_only)
listbox1_concept_names_only.config(yscrollcommand=scrollbary_only.set)
listbox2_concept_origin_only.config(yscrollcommand=scrollbary_only.set)
listbox_mark_concepts_only.config(yscrollcommand=scrollbary_only.set)


listbox_mark_concepts_only_menu = Menu(Frame1_concept_view_only, tearoff=False)
listbox_mark_concepts_only_menu.add_command(label="Flag this concept", command=mark_concept_only_menu)
listbox_mark_concepts_only_menu.add_command(label="Unflag this concept", command=unmark_concept_only_menu)
listbox_mark_concepts_only_menu.add_command(label="Delete this concept (limited usage)", command=delete_concept_only_menu)
listbox1_concept_names_only.bind("<Button-3>", my_popup_listbox1_concept_only_view)
scrollbary_only.pack(side="right", fill=Y, expand=False)
listbox1_concept_names_only.pack(side="left", fill=BOTH, expand=True)
listbox2_concept_origin_only.pack_forget()
listbox1_concept_names_only.bind("<<ListboxSelect>>", click_on_concept_only)
Frame1_concept_view_only.pack(side="left", fill=Y, padx=5, pady=5)

global notebook_concepts_only
notebook_concepts_only = ttk.Notebook(higher_view_concept_only_window)
notebook_concepts_only.pack(side=LEFT, fill=BOTH, expand=1, pady=20)
global previous_tab_id_concept_only
previous_tab_id_concept_only = 0
notebook_concepts_only.bind('<<NotebookTabChanged>>', set_previous_tab_index_concepts_only)
global window_concept_only
window_concept_only = Frame(notebook_concepts_only, width=950, height=450, bg="white")
global window_concept_only_note_view
window_concept_only_note_view = Frame(notebook_concepts_only, width=950, height=450, bg="white")
Frame1_concept_view = Frame(higher_view_concept_window, bg='white')
Frame_temp = Frame(Frame1_concept_view, bg='white')
Label(Frame_temp, text='Concepts list', bg='white', font='Helvetica 12 bold', fg='navy').pack(side="left")
Frame_temp.pack()

global listbox1_concept_names
global listbox2_concept_origin
global listbox_mark_concepts

listbox_mark_concepts = Listbox(Frame1_concept_view, width=3)
listbox1_concept_names = Listbox(Frame1_concept_view, width=50, exportselection=False)
listbox2_concept_origin = Listbox(Frame1_concept_view, width=10)

scrollbary = Scrollbar(Frame1_concept_view, command=yview_concept_view)
listbox1_concept_names.bind("<MouseWheel>", OnMouseWheel_concept_view)
listbox1_concept_names.config(yscrollcommand=scrollbary.set)
listbox2_concept_origin.bind("<MouseWheel>", OnMouseWheel_concept_view)
listbox2_concept_origin.config(yscrollcommand=scrollbary.set)
listbox_mark_concepts.config(yscrollcommand=scrollbary.set)
listbox1_concept_names.bind('<Double-Button-1>', lambda event: listbox_copy(listbox1_concept_names, event))

scrollbary.pack(side="right", fill=Y, expand=False)
listbox1_concept_names.pack(side="left", fill=BOTH, expand=True)
listbox2_concept_origin.pack_forget()
listbox1_concept_names.bind("<<ListboxSelect>>", click_on_concept)
listbox_mark_concepts.bind("<ButtonRelease-1>", lambda event: mark_concept(event))
Frame1_concept_view.pack(side="left", fill=Y, padx=5, pady=5)
Frame20 = Frame(higher_view_concept_window, bg='white')
Label(Frame20, text='Concept: ', bg='white', font='Helvetica 10 bold', fg='navy').grid(row=0, column=0, sticky='w')
Label(Frame20, text='Origin: ', bg='white', font='Helvetica 10 bold', fg='navy').grid(row=1, column=0, sticky='w')

global concept_name
concept_name = Label(Frame20, text='', bg='white')
concept_name.grid(row=0, column=1, sticky='w')
concept_origin = Label(Frame20, text='', bg='white')
concept_origin.grid(row=1, column=1, sticky='w')
Frame20.pack(side=TOP, anchor=W, padx=10, pady=10)

global notebook_concepts
notebook_concepts = ttk.Notebook(higher_view_concept_window)
notebook_concepts.pack(side=LEFT, fill=BOTH, expand=1)
notebook_concepts.bind('<<NotebookTabChanged>>', set_previous_tab_index_concepts)

global window_concept_axiom_view
window_concept_axiom_view = Frame(notebook_concepts, bg="white")
global window_concept_note_view
window_concept_note_view = Frame(notebook_concepts, bg="white")
global window_concept_axiom_focus_view
window_concept_axiom_focus_view = Frame(notebook_concepts, bg="white")



listbox_mark_concepts_menu = Menu(Frame1_concept_view, tearoff=False)
listbox_mark_concepts_menu.add_command(label="Flag this concept", command=mark_concept_menu)
listbox_mark_concepts_menu.add_command(label="Unflag this concept", command=unmark_concept_menu)
listbox_mark_concepts_menu.add_command(label="Mark as Done", command=mark_concept_done)
listbox_mark_concepts_menu.add_command(label="UnMark as Done", command=unmark_concept_done)
listbox_mark_concepts_menu.add_command(label="Delete this concept (limited usage)", command=delete_concept_menu)
listbox1_concept_names.bind("<Button-3>", my_popup_listbox1_concept_view)
listbox1_concept_names.bind('<FocusOut>', lambda e: clear_searched_concepts)

notebook_main.add(higher_view_phrase_window, text="Phrases \u279D Concepts")
notebook_main.add(higher_view_topics_phrases_window, text="Topics \u279D Concepts")
notebook_main.add(higher_view_concept_only_window, text="Concepts")
notebook_main.add(higher_view_concept_window, text="Concepts \u279D Axioms")

notebook_main.tab(1, state="disabled")
notebook_main.tab(2, state="disabled")
notebook_main.tab(3, state="disabled")
notebook_main.tab(4, state="disabled")

global element_display_popup
element_display_popup = -1
global phrases_list
phrases_list = []
global sub_super_phrsaes_list
sub_super_phrsaes_list = {}

global find_var
find_var = IntVar()
find_var.set(-1)
global findwindow
global window_display_all_axioms
global window_display_equivalent_concepts
global window_display_topic_labelling

root.bind('<Control-f>', find_window)
toolTip = ToolTip(root)
root.mainloop()
# **********************The End********************************
# *************************************************************
# *************************************************************