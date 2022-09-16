#!/usr/bin/env python3
import tkinter
from builtins import int
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from fuzzywuzzy import fuzz
from stemming.porter2 import stem
from tkinter import messagebox
import xlwt
import networkx as nx
from rdflib import URIRef
from rdflib.namespace import RDFS
import rdflib
from pyvis.network import Network
from owlready2 import *
# owlready2.JAVA_EXE = "C:\\path\\to\\java.exe"
owlready2.JAVA_EXE = "C:/path/to/java.exe"
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
import pickle
from tkinter import font


class NodeType_concepts:
    def __init__(self, concept_name, concept_axioms, super_concept_axioms, concept_color, concept_origin, concept_note, concept_color_list):
        self.concept_name = concept_name
        self.concept_axioms = concept_axioms
        self.concept_color = concept_color
        self.concept_origin = concept_origin
        self.super_concept_axioms = super_concept_axioms
        self.concept_note = concept_note
        self.concept_color_list = concept_color_list

    def set_concpet_name(self, name):
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

    def set_concept_color_list(self, color):
        self.concept_color_list = color

    def get_concpet_name(self):
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

    def get_concept_color_list(self):
        return self.concept_color_list


class NodeType_phrase:
    def __init__(self, phrase_name, phrase_refinedf, ext_concepts, phrase_color, phrase_label, phrase_note,
                 phrase_relatedc):
        self.phrase_name = phrase_name
        self.phrase_refinedf = phrase_refinedf
        self.ext_concepts = ext_concepts
        self.phrase_color = phrase_color
        self.phrase_label = phrase_label
        self.phrase_note = phrase_note
        self.phrase_relatedc = phrase_relatedc

    def set_phrase_name(self, name):
        self.phrase_name = name

    def set_phrase_refinedf(self, r):
        self.phrase_refinedf = r

    def set_ext_concepts(self, ext):
        self.ext_concepts = ext

    def set_phrase_color(self, c):
        self.phrase_color = c

    def set_phrase_label(self, l):
        self.phrase_label = l

    def set_phrase_related_concepts(self, c):
        self.phrase_relatedc = c

    def get_phrase_name(self):
        return self.phrase_name

    def get_phrase_refinedf(self):
        return self.phrase_refinedf

    def get_ext_concepts(self):
        return self.ext_concepts

    def get_phrase_color(self):
        return self.phrase_color

    def get_phrase_label(self):
        return self.phrase_label

    def set_phrase_note(self, c):
        self.phrase_note = c

    def get_phrase_note(self):
        return self.phrase_note

    def get_phrase_related_concepts(self):
        return self.phrase_relatedc


class NodeType:
    def __init__(self, metadata, refinedf, ext_concepts, phrase_color, note, phrase_relatedc):
        self.metadata_main = metadata
        self.refinedf_main = refinedf
        self.extracted_concepts = ext_concepts
        self.phrase_color = phrase_color
        self.note = note
        self.phrase_relatedc = phrase_relatedc

    def set_metadata(self, m):
        self.metadata_main = m

    def set_refinedf(self, r):
        self.refinedf_main = r

    def get_metadata(self):
        return self.metadata_main

    def get_refinedf(self):
        return self.refinedf_main

    def set_ext_concepts(self, e):
        self.extracted_concepts = e

    def get_ext_concepts(self):
        return self.extracted_concepts

    def set_phrase_color(self, c):
        self.phrase_color = c

    def get_phrase_color(self):
        return self.phrase_color

    def set_phrase_note(self, c):
        self.note = c

    def get_phrase_note(self):
        return self.note

    def set_phrase_relatedc(self, c):
        self.phrase_relatedc = c

    def get_phrase_relatedc(self):
        return self.phrase_relatedc


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
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


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
        ico = Image.open('logo_5.png')
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
        global listbox_search
        listbox_search = Listbox(findwindow, width=50, borderwidth=0, highlightthickness=0)
        listbox_search.pack(pady=10)
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
        # findwindow.resizable(0, 0)
        ico = Image.open('logo_5.png')
        photo = ImageTk.PhotoImage(ico)
        findwindow.wm_iconphoto(False, photo)
        frame1 = Frame(findwindow)
        global find_var
        find_var.set(find_var.get())
        b_phrase = Radiobutton(frame1, text="Find in Phrases", variable=find_var, value=0,command=lambda: find_phrases(), bg='white')
        b_phrase.grid(row=1, column=1)
        b_concept = Radiobutton(frame1, text="Find in Concepts", variable=find_var, value=1,command=lambda: find_concepts(), bg='white')
        b_concept.grid(row=1, column=2)
        b_axiom = Radiobutton(frame1, text="Find in Axioms", variable=find_var, value=2,command=lambda: find_axioms(), bg='white')
        b_axiom.grid(row=1, column=3)
        frame1.pack(pady=20)
        global search
        search = Entry(findwindow, font=("Helvetica", 11), borderwidth=0, highlightthickness=0)
        search.pack(pady=10)
        search.focus()
        global listbox_search
        listbox_search = Listbox(findwindow, width=50, borderwidth=0, highlightthickness=0)
        listbox_search.pack(pady=10)
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
                for item in super_cocepts:
                    if typed.lower() in item.lower():
                        i = super_cocepts.index(item)
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
        ico = Image.open('logo_5.png')
        photo = ImageTk.PhotoImage(ico)
        findwindow.wm_iconphoto(False, photo)

        frame1 = Frame(findwindow)
        global find_var
        find_var.set(find_var.get())
        b_phrase = Radiobutton(frame1, text="Find in Phrases", variable=find_var, value=0,command=lambda: find_phrases(), bg='white')
        b_phrase.grid(row=1, column=1)
        b_concept = Radiobutton(frame1, text="Find in Concepts", variable=find_var, value=1,command=lambda: find_concepts(), bg='white')
        b_concept.grid(row=1, column=2)
        b_axiom = Radiobutton(frame1, text="Find in Axioms", variable=find_var, value=2,command=lambda: find_axioms(), bg='white')
        b_axiom.grid(row=1, column=3)
        frame1.pack(pady=20)
        global search
        search = Entry(findwindow, font=("Helvetica", 11), borderwidth=0, highlightthickness=0)
        search.pack(pady=10)
        search.focus()
        search.config(width=0)
        global listbox_search
        listbox_search = Listbox(findwindow, borderwidth=0, highlightthickness=0)
        listbox_search.pack(pady=10)
        listbox_search.config(width=0, height=0)

        # save all defined axioms of ontology
        complete_relations_edge = []
        sub_concepts = []
        super_cocepts = []
        for r in relations_edge:
            sub_concepts.append(r[0])
            super_cocepts.append(r[1])
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
        findwindow.geometry("500x300+500+200")
        findwindow.configure(background='white')
        ico = Image.open('logo_5.png')
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


def load_ontology():
    owl_files = filedialog.askopenfilenames(title="Select OWL files to load", filetypes=(("OWL Files", "*.owl"),))
    root.update()
    paths = root.tk.splitlist(owl_files)
    read_owl(paths)


def restart_new_ontology():
    global p1, p2
    p1.config(text='')
    p2.config(text='')
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
    x_position = y_position = 0
    main_relation_edge = []
    global main_classes
    main_classes = []
    global relations_edge
    relations_edge = []
    global all_phrases
    global concepts
    global root
    all_phrases.clear()


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
        count = 0
        for path in paths:
            path = str(path)
            print(path)
            origin_path = " "
            origin_path = path.split('/')[-1]
            g = rdflib.Graph()
            g.parse(path, format='xml')
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
                            x = NodeType_concepts(y, [], [], 'black', origin_path, ' ', 'black')
                            size = len(main_concepts)
                            if size > 0:
                                main_concepts[0] = x
                            else:
                                main_concepts.append(x)
                            count += 1
                        else:
                            main_concept_names.append(y)
                            x = NodeType_concepts(y, [], [], 'black', origin_path, ' ', 'black')
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
        ontology_loaded_label.config(text="The ontology has been loaded successfully.", font='Helvetica 11 bold')

        length = len(main_concepts)
        for i in range(0, length):
            name = main_concepts[i].get_concpet_name()
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
            concept_origin.config(text=listbox2_concept_origin.get(index))
            concept_tab_axiom_view(ph)
            concept_note(ph)
            if previous_tab_id_concept == 0:
                notebook_concepts.select(window_concept_axiom_view)
            elif previous_tab_id_concept == 1:
                notebook_concepts.select(window_concept_note_view)
    except:
        pass


def concept_note(ph):
    i = main_concept_names.index(ph)
    global window_concept_note_view
    if window_concept_note_view:
        window_concept_note_view.destroy()
        window_concept_note_view = Frame(notebook_concepts, bg="white")  # width=950, height=450,
    Frame_note = Frame(window_concept_note_view, borderwidth=1, bg='white')
    textbox_note = Text(Frame_note, width=100, height=25, undo=True, borderwidth=0)  # , width=30, height=2,
    textbox_note.pack(fill='both', expand=True)
    b = Button(Frame_note, text="Save changes", width=15, fg='black', bg='lightBlue1', font=('comicsans', 12),command=lambda: save_concept_note((textbox_note.get("1.0", END)[:-1]), ph))
    b.pack(padx=1, pady=10)
    Frame_note.pack(fill='both', expand=True)
    notebook_concepts.add(window_concept_note_view, text="Note")
    textbox_note.delete('1.0', END)
    textbox_note.insert('1.0', main_concepts[i].get_concept_note())


def save_concept_note(note, ph):
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
    listbox_mark_concepts_menu.tk_popup(e.x_root, e.y_root)
    global x_position
    global y_position
    x_position = e.x_root
    y_position = e.y_root


def info_window_2(message, title, time, xposition, yposition):
    window = Toplevel(root)
    window.title(title)
    s = "+" + str(xposition) + "+" + str(yposition)
    window.geometry(s)
    window.configure(background='white')
    window.resizable(0, 0)
    ico = Image.open('logo_5.png')
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
        main_concepts[i].set_concept_color('green')
        listbox1_concept_names.itemconfig(i, fg='green')
        listbox2_concept_origin.itemconfig(i, fg='green')


def unmark_concept_done():
    concept_name.config(text=listbox1_concept_names.get(ANCHOR))
    ph = concept_name.cget("text")
    if (ph != ''):
        i = main_concept_names.index(ph)
        previous_color = main_concepts[i].get_concept_color_list()
        main_concepts[i].set_concept_color(previous_color)
        listbox1_concept_names.itemconfig(i, fg=previous_color)
        listbox2_concept_origin.itemconfig(i, fg=previous_color)


def yview_main(*args):
    """ scroll both listboxes together """
    listbox1.yview(*args)
    listbox2.yview(*args)
    listbox_mark.yview(*args)


def scroll_view(listbox, *args):
    listbox.yview(*args)


def OnMouseWheel(event):
    listbox1.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox2.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox_mark.yview_scroll(-1 * int(event.delta / 120), "units")
    return "break"


def click_on_phrase(e):
    try:
        curselection = listbox1.curselection()[0]
        p1.config(text=listbox1.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            index = phrases.index(ph)
            p2.config(text=listbox2.get(index))
            add_meta_data_tab(ph)
            add_note_phrase(ph)
            if previous_tab_id == 0:
                notebook_phrases.select(window_phrase_add_metadata_view)
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
    Frame_note = Frame(window_phrase_note_view, borderwidth=1, bg='white')
    textbox_note = Text(Frame_note, width=100, height=25, undo=True, borderwidth=0)
    textbox_note.pack(fill='both', expand=True, anchor=W)
    b = Button(Frame_note, text="Save changes", width=15, fg='black', bg='lightBlue1', font=('comicsans', 12),
               command=lambda: save_phrase_note((textbox_note.get("1.0", END)[:-1]), ph))
    b.pack(padx=1, pady=10)
    Frame_note.pack(fill='both', expand=True)
    notebook_phrases.add(window_phrase_note_view, text="Note")
    textbox_note.insert('1.0', FP_metadata_2[i].get_phrase_note())


def save_phrase_note(note, ph):
    index = phrases.index(ph)
    global FP_metadata
    global FP_metadata_2
    x = FP_metadata_2[index]
    y = FP_metadata[index]
    x.set_phrase_note(note)
    y.set_phrase_note(note)
    FP_metadata_2[index] = x
    FP_metadata[index] = y
    info_window("The note has been saved!", "Info", 2000)


def add_to_concepts_new(text, ph, var):
    if text != "":
        temp_name = text
        main_concept_names.append(temp_name)
        index = main_concept_names.index(temp_name)
        x_concept = NodeType_concepts(temp_name, [], [], 'blue', ph, ' ', 'blue')
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


def add_to_concepts(text, ph, var):
    temp = text.strip()
    temp = camelcase_concept_name(temp)
    text = camelcase_concept_name(text)
    if text != "" and temp != "":
        if var == 0:
            p1.config(text=ph)
            i = phrases.index(ph)
            ext_concepts = []
            ext_concepts = FP_metadata_2[i].get_ext_concepts()
            if ext_concepts == '':
                ext_concepts = []
            temp_text = text
            if temp_text not in main_concept_names and temp_text not in ext_concepts:
                listbox_concepts_metadata.insert(END, temp_text)
                textbox2.delete('1.0', END)
                ext_concepts.append(temp_text)
                FP_metadata_2[i].set_ext_concepts(ext_concepts)
                FP_metadata[i].set_ext_concepts(ext_concepts)
                if FP_validation[i] == ('' or ' '):
                    FP_validation[i] = 'ADD'
                else:
                    temp = FP_validation[i].replace('ADD-m', '')
                    if "ADD" not in temp:
                        if "ADD-m" in FP_validation[i]:
                            FP_validation[i] = "ADD , " + FP_validation[i]
                listbox2.delete(i)
                listbox2.insert(i, FP_validation[i])
                exist_m_related_concept.append(" ")
                temp_name = text
                main_concept_names.append(temp_name)
                index = main_concept_names.index(temp_name)
                x_concept = NodeType_concepts(temp_name, [], [], 'blue', '', ' ', 'blue')
                main_concepts.append(x_concept)

                listbox1_concept_names.insert(END, temp_name)
                listbox2_concept_origin.insert(END, "")
                listbox_mark_concepts.insert(END, " ")
                i = listbox1_concept_names.get(0, END).index(temp_name)
                listbox1_concept_names.itemconfig(i, fg='blue')
                listbox2_concept_origin.itemconfig(i, fg='blue')

                listbox1_concept_names_only.insert(END, temp_name)
                listbox2_concept_origin_only.insert(END, "")
                listbox_mark_concepts_only.insert(END, " ")
                i = listbox1_concept_names_only.get(0, END).index(temp_name)
                listbox1_concept_names_only.itemconfig(i, fg='blue')
                listbox2_concept_origin_only.itemconfig(i, fg='blue')

                refresh_meta_data_tabs_2()
            else:
                messagebox.showerror("Error", "The concept \"" + ph + "\" already exists in concepts!")

        elif var == 1:
            global state_add_concpet_var
            state_add_concpet_var.set(1)
            p1.config(text=listbox1.get(ANCHOR))
            ph = p1.cget("text")
            i = phrases.index(ph)
            ext_concepts = []
            ext_concepts = FP_metadata_2[i].get_ext_concepts()
            if ext_concepts == '':
                ext_concepts = []
            temp_text = text
            if temp_text not in main_concept_names and temp_text not in ext_concepts:
                listbox_concepts_metadata.insert(END, temp_text)
                textbox2.delete('1.0', END)
                ext_concepts.append(temp_text)
                FP_metadata_2[i].set_ext_concepts(ext_concepts)
                FP_metadata[i].set_ext_concepts(ext_concepts)
                if "ADD-m" not in FP_validation[i]:
                    if "ADD" not in FP_validation[i]:
                        temp_label = "ADD-m"
                    else:
                        temp_label = FP_validation[i] + " , " + "ADD-m"
                    FP_validation[i] = temp_label
                    listbox2.delete(i)
                    listbox2.insert(i, temp_label)
                temp_name = text
                main_concept_names.append(temp_name)
                index = main_concept_names.index(temp_name)
                x_concept = NodeType_concepts(temp_name, [], [], 'purple', ph, ' ', 'purple')
                main_concepts.append(x_concept)

                listbox1_concept_names.insert(END, temp_name)
                listbox2_concept_origin.insert(END, ph)
                listbox_mark_concepts.insert(END, " ")
                i = listbox1_concept_names.get(0, END).index(temp_name)
                listbox1_concept_names.itemconfig(i, fg='purple')
                listbox2_concept_origin.itemconfig(i, fg='purple')

                listbox1_concept_names_only.insert(END, temp_name)
                listbox2_concept_origin_only.insert(END, ph)
                listbox_mark_concepts_only.insert(END, " ")
                i = listbox1_concept_names_only.get(0, END).index(temp_name)
                listbox1_concept_names_only.itemconfig(i, fg='purple')
                listbox2_concept_origin_only.itemconfig(i, fg='purple')

                refresh_meta_data_tabs_2()
            else:
                temp_name = text
                messagebox.showerror("Error", "The concept \"" + temp_name + "\" already exists in concepts!")
    else:
        textbox2.delete('1.0', END)


def refresh_meta_data_tabs():
    try:
        curselection = listbox1_concept_names.curselection()[0]
        p1.config(text=listbox1_concept_names.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            index = main_concept_names.index(ph)
            p2.config(text=listbox2_concept_origin.get(index))
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


def refresh_meta_data_tabs_2():
    try:
        curselection = listbox1.curselection()[0]
        p1.config(text=listbox1.get(curselection))
        ph = p1.cget("text")
        if ph != '':
            index = phrases.index(ph)
            p2.config(text=listbox2.get(index))
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
    ico = Image.open('logo_5.png')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)
    my_label = Label(window, text=message, bg='white', font='Helvetica 9 bold')
    my_label.pack()
    if time != -1:
        window.after(time, window.destroy)


def my_popup_2(e):
    menu_subsuper.tk_popup(e.x_root, e.y_root)


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


def camelcase_concept_name(name):
    name = str(name)
    name_1 = name.title()
    name_1 = name_1.strip()
    name_2 = name_1.replace(" ", "")
    return name_2


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
        if (FP_validation[index] in value_list) :
            if related_concept in main_concept_names:
                # global assigned_concepts
                assigned_concepts.config(fg='navy')
                FP_validation[index] = "EXIST or EXIST-m"
                listbox2.delete(index)
                listbox2.insert(index, FP_validation[index])
                index = phrases.index(phrase)
                p2.config(text=listbox2.get(index))
                if (related_concept not in FP_metadata_2[index].get_phrase_relatedc()):
                    exist_m_related_concept[index] = related_concept
                    listbox_related_concepts.insert(END, related_concept)
                    listbox_related_concepts.itemconfig(END, bg='lightcyan')
                    related_concepts_list = []
                    related_concepts_list = FP_metadata_2[index].get_phrase_relatedc()
                    if related_concepts_list == '' or related_concepts_list == " ":
                        related_concepts_list = []
                    related_concepts_list.append(related_concept)
                    FP_metadata_2[index].set_phrase_relatedc(related_concepts_list)
                    search_3.delete(0, END)
            else:
                info_window("There is not such concept! Please enter the correct concept name.", "Error", 3000)
                search_3.delete(0, END)
        else:
            # info_window("You cannot define related concept while label is not empty or not EXIST or EXIST-m", "Error",3000)
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

    def use_new_phrase_name():
        textbox2.delete("1.0", END)

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
    #'''
    def OnKeyPress_textbox2(e):
        global state_add_concpet_var
        if state_add_concpet_var.get() != 1 and state_add_concpet_var.get() != 0:
            state_add_concpet_var.set(1)
            refined_button1 = Radiobutton(Frame12, text="Use the phrase itself", variable=state_add_concpet_var, value=0,
                                          command=use_of_phrase_ityself, bg='whitesmoke')
            refined_button1.grid(row=0, column=1, sticky='W')
            refined_button2 = Radiobutton(Frame12, text="Define new form of the phrase", variable=state_add_concpet_var,
                                          value=1, command=use_of_other_form_of_phrase, bg='whitesmoke')
            refined_button2.grid(row=1, column=1, sticky='W')

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
    r = FP_metadata_2[i].get_ext_concepts()
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
    listbox_search_3 = Listbox(Frame14, width=40, height=5, borderwidth=0, highlightthickness=0, bg='whitesmoke')
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
    assigned_concepts = Label(Frame14, text='Assigned Concepts to Phrase', bg='whitesmoke', font='Helvetica 9 bold',
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

    rc = FP_metadata_2[i].get_phrase_relatedc()
    if rc and rc != '' and rc != " ":
        assigned_concepts.config(fg='black')
        for item in rc:
            listbox_related_concepts.insert(END, item)
            listbox_related_concepts.itemconfig(END, bg='lightcyan')

    listbox_related_concepts.bind("<<ListboxSelect>>",lambda e: click_on_listbox_concepts_metadata(e, listbox_related_concepts))

    i = phrases.index(ph)
    if exist_m_related_concept[i] != " " and exist_m_related_concept[i] != '':
        search_3.insert(0, exist_m_related_concept[i])
    Frame14.grid(row=1, column=0, sticky='w', padx=15, pady=10)
    window_phrase_add_metadata_view.pack()
    notebook_phrases.add(window_phrase_add_metadata_view, text="Define Concepts from Phrase")


def close_tab(window):
    window.destroy()


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
            listbox_mark.see(index)
            p2.config(text=listbox2.get(index))
            add_meta_data_tab(ph)
            add_note_phrase(ph)
            notebook_main.select(higher_view_phrase_window)
            if previous_tab_id == 0:
                notebook_phrases.select(window_phrase_add_metadata_view)
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
                        result_p_label.append(FP_validation[i])
                    temp = phrase_stemming(x)
                    if temp == stem_ph:
                        stem_result_p.append(x)
                        i = phrases_2.index(x)
                        stem_result_p_label.append(FP_validation[i])
                    else:
                        if (substring(temp, stem_ph) == 1):
                            stem_result_p.append(x)
                            i = phrases_2.index(x)
                            stem_result_p_label.append(FP_validation[i])
        else:
            messagebox.showerror("Error", "Please select a phrase for matching!")
            return False
        if len(stem_result_p) > 0:
            for i in stem_result_p:
                listbox4.insert(END, i)

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

    def load_phrases_for_super_sub_phrases(window, phrase, listbox6):
        phrases_files = root.filename = filedialog.askopenfilenames(
            title="Select Phrases files to load and extract Super and Sub phrases",
            filetypes=(("text Files", "*.txt"),))
        paths = root.tk.splitlist(phrases_files)
        if paths:
            listbox6.delete(0, END)
            load_super_sub_phrases_path.clear()
            global phrases_list
            phrases_list = []
            for path in paths:
                load_super_sub_phrases_path.append(path)
                input_file_2 = open(path, "r")
                lines_2 = input_file_2.readlines()
                for j in lines_2:
                    phrases_list.append(re.sub('[^A-Za-z]+', ' ', j))
            ph_stem = phrase_stemming(phrase)
            global sub_super_phrsaes_list
            sub_super_phrsaes_list = {}
            i = phrases.index(phrase)
            results = [i for i in phrases_list if ph_stem in phrase_stemming(i) and ph_stem != phrase_stemming(i)]
            sub_super_phrsaes_list[i] = results
            listbox6.insert(END, *results)
            Button_yes.config(bg='turquoise')
            global sub_super_p_button_color_yes
            sub_super_p_button_color_yes = 'turquoise'

            Button_no.config(bg='lightBlue1')
            global sub_super_p_button_color_no
            sub_super_p_button_color_no = 'lightBlue1'
        # else:
        #    messagebox.showerror("Error", "Please select a file to be loaded!")
        # window.lift()

    def unload_phrases_for_super_sub_phrases():
        Button_yes.config(bg='lightBlue1')
        global sub_super_p_button_color_yes
        sub_super_p_button_color_yes = 'lightBlue1'
        Button_no.config(bg='turquoise')
        global load_super_sub_phrases_path
        load_super_sub_phrases_path = []
        listbox6.delete(0, END)
        global sub_super_p_button_color_no
        sub_super_p_button_color_no = 'turquoise'

    def context_menu(listbox6, window):
        p = ''
        p = listbox6.get(ANCHOR)
        ph = p
        if (ph != ''):
            item = ph
            flag = 0
            for phr in phrases:
                if item == phr:
                    flag = 1
                    break
            global window_phrase_add_metadata_view
            if flag == 0:
                response = messagebox.askquestion('Add to Phrases',
                                                  'Are you sure to add "' + item + '" to the phrases?\n',
                                                  parent=window_phrase_matching_view)
                if response == 'yes':
                    ph_str = str(ph)
                    item = ph_str.strip()
                    phrases.append(item)
                    listbox1.insert(END, item)
                    listbox1_phrase_only.insert(END, item)
                    FP_validation.append(" ")
                    exist_m_related_concept.append(" ")
                    x = NodeType(" ", " ", [], " ", " ", " ")
                    list_nodetype = []
                    list_ext_concepts = []
                    x_2 = NodeType(list_nodetype, " ", list_ext_concepts, "black", " ", " ")
                    FP_metadata.append(x)
                    FP_metadata_2.append(x_2)
                    FP_metadata_md.append(" ")
                    FP_metadata_refined.append(" ")
                    listbox2.insert(END, " ")
                    listbox_mark.insert(END, " ")
                    listbox2_phrase_only.insert(END, " ")
                    listbox_mark_phrase_only.insert(END, " ")
                    s = '"' + item + '" ' + "is added to phrases!"
                    info_window(s, "Info", 3000)
            else:
                s = item + " " + "already exists in phrases!"
                info_window(s, "Error", -1)

    global notebook_phrases


    global window_phrase_matching_view
    if window_phrase_matching_view:
        window_phrase_matching_view.destroy()
        window_phrase_matching_view = Frame(notebook_phrases_only, bg="white")  # width=950, height=450

    Frame3 = Frame(window_phrase_matching_view, bg='whitesmoke')
    Label(Frame3, text='Matched Phrases', bg='whitesmoke', font='Helvetica 9 bold', fg='navy').grid(row=0, column=0,
                                                                                                    padx=5, sticky='w')
    Label(Frame3, text='', bg='whitesmoke').grid(row=0, column=2)
    Label(Frame3, text='Matched Concepts', bg='whitesmoke', font='Helvetica 9 bold', fg='navy').grid(row=0, column=3,
                                                                                                     padx=5, sticky='w')
    listbox4 = Listbox(Frame3, width=40, height=5, bg='whitesmoke', borderwidth=0, highlightthickness=0)
    listbox4.grid(row=1, column=0)
    listbox4_3 = Listbox(Frame3, width=1, height=5, bg="silver")
    listbox4_3.grid(row=1, column=1)
    listbox5 = Listbox(Frame3, width=40, height=5, bg='whitesmoke', borderwidth=0, highlightthickness=0)
    listbox5.grid(row=1, column=3)

    listbox4.bind("<<ListboxSelect>>", lambda e: click_on_phrase_listbox(e, listbox4))
    listbox5.bind("<<ListboxSelect>>", lambda e: click_on_concept_listbox(e, listbox5))

    scrollbary_listbox4 = AutoScrollbar(Frame3, command=scroll_view(listbox4))
    scrollbary_listbox4.configure(command=listbox4.yview)
    listbox4.config(yscrollcommand=scrollbary_listbox4.set)
    scrollbary_listbox4.grid(row=1, column=1, sticky="ns")

    scrollbary_listbox5 = AutoScrollbar(Frame3, command=scroll_view(listbox5))
    scrollbary_listbox5.configure(command=listbox5.yview)
    listbox5.config(yscrollcommand=scrollbary_listbox5.set)
    scrollbary_listbox5.grid(row=1, column=3, sticky="ns")

    Frame6 = Frame(Frame3, bg='whitesmoke')
    Button2 = Button(Frame6, text="Matching", width=20, fg='black', bg='lightBlue1', font=('comicsans', 10),
                     command=matching)
    Button2.pack(padx=10, pady=5, anchor=W)
    Button3 = Button(Frame6, text="Clear Matching lists", width=20, fg='black', bg='lightBlue1', font=('comicsans', 10),
                     command=clear_all)
    Button3.pack(padx=10, pady=5, anchor=W)
    Frame6.grid(row=1, column=4, padx=10, pady=10)
    Frame3.grid(row=0, column=0, padx=10, pady=10)

    Frame6 = Frame(window_phrase_matching_view, bg='white')
    Label(Frame6, text='Sub and Super Phrases', bg='white', font='Helvetica 11 bold', fg='navy').grid(row=0, column=1)
    global listbox6
    listbox6 = Listbox(Frame6, width=80, height=9, borderwidth=0, highlightthickness=0)
    listbox6.grid(row=1, column=1)
    listbox6.config(bg='whitesmoke')

    scrollbary_2 = AutoScrollbar(Frame6, command=lambda event: OnMouseWheel_function(e=event, listname=listbox6))
    listbox6.config(yscrollcommand=scrollbary_2.set)
    scrollbary_2.grid(row=1, column=2, sticky="ns")

    Label(Frame6, text='Load other phrases file\\files to extract super and sub phrases', bg='white').grid(row=2,
                                                                                                           column=1,
                                                                                                           pady=5)
    Frame_mini = Frame(Frame6, bg='white', borderwidth=0, highlightthickness=0)
    Button_yes = Button(Frame_mini, text="Load", width=6, fg='black', bg=sub_super_p_button_color_yes,
                        font=('comicsans', 9),
                        command=lambda: load_phrases_for_super_sub_phrases(window_phrase_add_metadata_view, ph,
                                                                           listbox6))
    Button_yes.grid(row=0, column=0, padx=5)
    Button_no = Button(Frame_mini, text="Unload", width=6, fg='black', bg=sub_super_p_button_color_no,
                       font=('comicsans', 9), command=unload_phrases_for_super_sub_phrases)
    Button_no.grid(row=0, column=1, padx=5)
    Frame_mini.grid(row=3, column=1, pady=5)
    Frame6.grid(row=1, column=0, sticky='w', padx=10, pady=20)

    global menu_subsuper
    menu_subsuper = Menu(Frame6, tearoff=False)
    menu_subsuper.add_command(label="Add to phrases",
                              command=lambda: context_menu(listbox6, window_phrase_add_metadata_view))
    listbox6.bind("<Button-3>", my_popup_2)
    if load_super_sub_phrases_path:
        listbox6.delete(0, END)
        i = phrases.index(ph)
        try:
            results = sub_super_phrsaes_list[i]
            listbox6.insert(END, *results)
        except:
            ph_stem = phrase_stemming(ph)
            results = [i for i in phrases_list if ph_stem in phrase_stemming(i) and ph_stem != phrase_stemming(i)]
            sub_super_phrsaes_list[i] = results
            listbox6.insert(END, *results)
    notebook_phrases_only.add(window_phrase_matching_view, text="Focus on Phrase")


def clear_all_searched_phrases(e):
    global flag_find_window_phrases
    flag_find_window_phrases = 0
    for item in phrases:
        i = phrases.index(item)
        try:
            listbox1.itemconfig(i, {'bg': 'white'})

        except:
            return None


def clear_all_searched_axioms(e):
    global flag_find_window_axioms
    flag_find_window_axioms = 0


def clear_all_searched_concepts(e):
    global flag_find_window_concepts
    flag_find_window_concepts = 0
    for item in main_concept_names:
        i = main_concept_names.index(item)
        try:
            listbox1_concept_names.itemconfig(i, {'bg': 'white'})
            listbox2_concept_origin.itemconfig(i, {'bg': 'white'})
            listbox_mark_concepts.itemconfig(i, {'bg': 'white'})
        except:
            return None


def listbox_undo(e):
    global listbox1_deleted_index
    global listbox1_deleted
    global listbox2_deleted
    if listbox1_deleted_index != -1:
        listbox1.insert(listbox1_deleted_index, listbox1_deleted)
        listbox2.insert(listbox1_deleted_index, listbox2_deleted)
        listbox_mark.insert(listbox1_deleted_index, ' ')
        listbox1_deleted_index = -1
        listbox1_deleted = ''
        listbox2_deleted = ''


def listbox_concept_undo(e):
    global listbox1_concept_deleted_index
    global listbox1_concept_deleted
    global listbox2_concept_deleted
    if listbox1_concept_deleted_index != -1:
        listbox1_concept_names.insert(listbox1_concept_deleted_index, listbox1_concept_deleted)
        listbox2_concept_origin.insert(listbox1_concept_deleted_index, listbox2_concept_deleted)
        listbox_mark_concepts.insert(listbox1_concept_deleted_index, ' ')
        listbox1_concept_deleted_index = -1
        listbox1_concept_deleted = ''
        listbox2_concept_deleted = ''


def mark_phrase(e):
    try:
        curselection = listbox_mark.curselection()
        index = curselection[0]
        bg_color = listbox_mark.itemcget(index, "background")

        if bg_color == 'red':
            listbox_mark.itemconfig(index, {'bg': 'white'})
            listbox_mark.selection_clear(0, END)
            listbox_mark_phrase_only.itemconfig(index, {'bg': 'white'})
            listbox_mark_phrase_only.selection_clear(0, END)
        else:
            listbox_mark.itemconfig(index, {'bg': 'red'})
            listbox_mark.selection_clear(0, END)
            listbox_mark_phrase_only.itemconfig(index, {'bg': 'darkred'})
            listbox_mark_phrase_only.selection_clear(0, END)
    except:
        return None


def unmark_phrase(e):
    try:
        curselection = listbox_mark.curselection()
        index = curselection[0]
        listbox_mark.itemconfig(index, {'bg': 'white'})
    except:
        return None


def context_menu_2():
    global listbox1_deleted
    global listbox1_deleted_index
    global listbox2_deleted
    p1.config(text=listbox1.get(ANCHOR))
    ph = p1.cget("text")
    if ph != '':
        i = phrases.index(ph)
        response = messagebox.askquestion('Delete Item', 'Are you sure to delete?\n' + ph, parent=root)
        if response == 'yes':
            listbox1.delete(i)
            listbox2_deleted = listbox2.get(i)
            listbox2.delete(i)
            listbox1_deleted = ph
            listbox1_deleted_index = i
            for p in phrases:
                index = phrases.index(p)
                c = FP_metadata_2[index].get_ext_concepts()
                if ph in c:
                    c.remove(ph)
    else:
        info_window_2("Select a phrase to be deleted!", "Error", 2000, x_position, y_position)


def mark_phrase_done():
    p1.config(text=listbox1.get(ANCHOR))
    ph = p1.cget("text")
    if ph != '':
        i = phrases.index(ph)
        listbox1.itemconfig(i, fg='green')
        listbox2.itemconfig(i, fg='green')
        FP_metadata_2[i].set_phrase_color('green')


def unmark_phrase_done():
    p1.config(text=listbox1.get(ANCHOR))
    ph = p1.cget("text")
    if (ph != ''):
        i = phrases.index(ph)
        listbox1.itemconfig(i, fg='black')
        listbox2.itemconfig(i, fg='black')
        FP_metadata_2[i].set_phrase_color('black')


def my_popup_3(e):
    listbox1_menu.tk_popup(e.x_root, e.y_root)
    global x_position
    global y_position
    x_position = e.x_root
    y_position = e.y_root


def load_phrases():
    phrases_files = filedialog.askopenfilenames(title="Select Phrases files to load",filetypes=(("text Files", "*.txt"),))
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
    global all_phrases_color
    phrases.clear()
    FP_validation.clear()
    exist_m_related_concept.clear()
    FP_metadata.clear()
    FP_metadata_2.clear()
    FP_metadata_md.clear()
    FP_metadata_refined.clear()
    all_phrases.clear()
    listbox1.delete(0, END)
    listbox2.delete(0, END)
    listbox_mark.delete(0, END)
    listbox1_phrase_only.delete(0, END)
    listbox2_phrase_only.delete(0, END)
    listbox_mark_phrase_only.delete(0, END)

    for item in data:
        item = item.strip()
        FP_validation.append(" ")
        exist_m_related_concept.append(" ")
        x = NodeType(" ", " ", " ", " ", " ", " ")
        Node_list = []
        list_ext_concpets = []
        x_2 = NodeType(Node_list, " ", list_ext_concpets, " ", " ", " ")
        FP_metadata.append(x)
        FP_metadata_2.append(x_2)
        FP_metadata_md.append(" ")
        FP_metadata_refined.append(" ")
        all_phrases_color.append('black')
        phrases.append(item)
        all_phrases.append(item)

    for item in data:
        item = item.strip()
        i = phrases.index(item)
        listbox1.insert(END, item)
        listbox2.insert(END, FP_validation[i])
        listbox_mark.insert(END, " ")
        listbox1_phrase_only.insert(END, item)
        listbox2_phrase_only.insert(END, FP_validation[i])
        listbox_mark_phrase_only.insert(END, " ")

    phrases_loaded_label.config(text="The frequent phrases has been loaded successfully.", font='Helvetica 11 bold')
    phrases_loaded_path.config(state="disabled")
    root.mainloop()


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
                result_concepts, result_realtions, relations = find_relations_super_2(main_phrase, x2_2,
                                                                                      result_relations,
                                                                                      result_concepts, relations)
                listbox_axiom_view_super_axioms.delete(0, END)
                for r in relations:
                    listbox_axiom_view_super_axioms.insert(END, r)
                result_relations_sub = []
                result_concepts_sub = []
                relations_sub = []
                result_concepts_sub, result_realtions_sub, relations_sub = find_relations_sub_2(main_phrase, x1_1,
                                                                                                result_relations_sub,
                                                                                                result_concepts_sub,
                                                                                                relations_sub)
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

    def enable_direction2():
        search_3.configure(state='normal')
        search_2.delete(0, END)
        search_2.configure(state='disable')

    axioms = []
    global window_concept_axiom_view
    if window_concept_axiom_view:
        window_concept_axiom_view.destroy()
        window_concept_axiom_view = Frame(notebook_concepts, bg="white")  # width=950, height=490,

    global window_concept_note_view
    if window_concept_note_view:
        window_concept_note_view.destroy()
        window_concept_note_view = Frame(notebook_concepts, bg="white")  # width=950, height=490,

    Frame12 = Frame(window_concept_axiom_view, borderwidth=1, bg='white')

    Frame11 = Frame(Frame12, borderwidth=1, bg='white')
    global axiom_direction
    b1 = Radiobutton(Frame11, text=" ", variable=axiom_direction, value=0, command=enable_direction1, bg="white")
    b1.grid(row=1, column=1, sticky='W')
    b2 = Radiobutton(Frame11, text=" ", variable=axiom_direction, value=1, command=enable_direction2, bg="white")
    b2.grid(row=2, column=1, pady=30, sticky='W')

    Label(Frame11, text=ph, bg='white', font='Helvetica 9 bold', relief='groove', width=30).grid(row=1,
                                                                                                 column=2)
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
    Label(Frame11, text=ph, bg='white', font='Helvetica 9 bold', relief='groove', width=30).grid(row=2, column=4,
                                                                                                 pady=5)
    Button10 = Button(Frame11, text="Add to axioms", width=15, fg='black', bg='lightBlue1', font=('comicsans', 10),
                      command=lambda: add_relation(ph, variable.get(), search_2.get(), search_3.get(),
                                                   axiom_direction.get(), window_concept_axiom_view))
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
    listbox_search_2 = Listbox(Frame14, width=50, height=10)
    listbox_search_2.grid(row=1, column=1)
    update_2(main_concept_names)
    listbox_search_2.bind("<<ListboxSelect>>", fillout_2)
    search_2.bind("<KeyRelease>", check_2)
    search_3.bind("<KeyRelease>", check_3)
    Frame14.grid(row=0, column=1)
    Frame12.grid(row=0, column=0, sticky='e', padx=5, pady=5)
    Frame3 = Frame(window_concept_axiom_view, borderwidth=0, bg='white')
    Label(Frame3,text='Axioms defined for the concept',bg='white',font='Helvetica 9 bold',fg='navy').grid(row=0,column=1)
    global listbox_axiom_view
    listbox_axiom_view = Listbox(Frame3, width=45, height=10)
    scrollbary_axiom_focus = Scrollbar(Frame3, orient=VERTICAL)
    listbox_axiom_view.config(yscrollcommand=scrollbary_axiom_focus.set)
    scrollbary_axiom_focus.config(command=listbox_axiom_view.yview)
    scrollbary_axiom_focus.grid(row=1, column=2, sticky="ns")
    listbox_axiom_view.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event, listname=listbox_axiom_view))
    listbox_axiom_view.grid(row=1, column=1, padx=1)
    listbox_axiom_view.bind('<Double-Button-1>', lambda event: listbox_copy(listbox_axiom_view, event))
    def on_enter_listbox(e, listname):
        index = listname.index("@%s,%s" % (e.x, e.y))
        if index >= 0:
            if (e.y < listname.bbox(0)[1]) or (
                    e.y > listname.bbox(END)[1] + listname.bbox(END)[3]):  # if not between it
                return None
            else:
                toolTip.showtip(listname.get(index))
                global element_display_popup
                element_display_popup = index

    def on_leave_listbox_1(e):
        toolTip.hidetip()
        global element_display_popup
        element_display_popup = -1

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
            if index != element_display_popup:
                toolTip.hidetip()
                element_display_popup = index
                if (e.y < listname.bbox(0)[1]) or (
                        e.y > listname.bbox(END)[1] + listname.bbox(END)[3]):  # if not between it
                    return None
                else:
                    toolTip.showtip(listname.get(index))

    element_display_popup = -1
    listbox_axiom_view.bind("<Enter>", lambda event: on_enter_listbox(e=event, listname=listbox_axiom_view))
    listbox_axiom_view.bind("<Leave>", on_leave_listbox_1)
    listbox_axiom_view.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox_axiom_view))

    Label(Frame3, text='Axioms related to super-concepts of the concept', bg='white', font='Helvetica 9 bold',fg='navy').grid(row=0,column=3)
    listbox_axiom_view_super_axioms = Listbox(Frame3, width=45, height=10)
    scrollbary_axiom_focus_super = Scrollbar(Frame3, orient=VERTICAL)
    listbox_axiom_view_super_axioms.config(yscrollcommand=scrollbary_axiom_focus_super.set)
    scrollbary_axiom_focus_super.config(command=listbox_axiom_view_super_axioms.yview)
    scrollbary_axiom_focus_super.grid(row=1, column=4, sticky="ns")
    listbox_axiom_view_super_axioms.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event,
                                                                                             listname=listbox_axiom_view_super_axioms))
    listbox_axiom_view_super_axioms.grid(row=1, column=3, pady=1)
    listbox_axiom_view_super_axioms.bind('<Double-Button-1>',
                                         lambda event: listbox_copy(listbox_axiom_view_super_axioms, event))

    Label(Frame3, text='Axioms related to sub-concepts of the concept', bg='white', font='Helvetica 9 bold',
          fg='navy').grid(row=0,
                          column=5)
    listbox_axiom_view_sub_axioms = Listbox(Frame3, width=45, height=10)
    scrollbary_axiom_focus_sub = Scrollbar(Frame3, orient=VERTICAL)
    listbox_axiom_view_sub_axioms.config(yscrollcommand=scrollbary_axiom_focus_sub.set)
    scrollbary_axiom_focus_sub.config(command=listbox_axiom_view_sub_axioms.yview)
    scrollbary_axiom_focus_sub.grid(row=1, column=6, sticky="ns")
    listbox_axiom_view_sub_axioms.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event,
                                                                                           listname=listbox_axiom_view_sub_axioms))
    listbox_axiom_view_sub_axioms.grid(row=1, column=5, padx=1)
    listbox_axiom_view_sub_axioms.bind('<Double-Button-1>',
                                       lambda event: listbox_copy(listbox_axiom_view_sub_axioms, event))
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

    listbox_axiom_view_super_axioms.bind("<Enter>", lambda event: on_enter_listbox(e=event, listname=listbox_axiom_view_super_axioms))
    listbox_axiom_view_super_axioms.bind("<Leave>", on_leave_listbox_2)
    listbox_axiom_view_super_axioms.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox_axiom_view_super_axioms))
    listbox_axiom_view_sub_axioms.bind("<Enter>", lambda event: on_enter_listbox(e=event, listname=listbox_axiom_view_sub_axioms))
    listbox_axiom_view_sub_axioms.bind("<Leave>", on_leave_listbox_3)
    listbox_axiom_view_sub_axioms.bind("<Motion>", lambda event: on_motion_listbox(e=event, listname=listbox_axiom_view_sub_axioms))
    window_concept_axiom_view.lift()
    window_concept_axiom_view.pack()
    notebook_concepts.add(window_concept_axiom_view, text="Define axioms")
    notebook_concepts.add(window_concept_note_view, text="Note")
    notebook_concepts.select(window_concept_axiom_view)


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
            index = main_concept_names.index(item)
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
            index = main_concept_names.index(item)
            if typed.lower() in item.lower():
                data.append(item)
    update_2(data)


def update_2(data):
    listbox_search_2.delete(0, END)
    listbox_search_2.insert(END, *data)


def find_relations_super_cycle_2(destination, sub_concept, super_concept, result_relations, result_concepts, relations):
    # check if super_concept is a sub_concept
    for r in relations_edge:
        c1 = r[0]
        c2 = r[1]
        if super_concept == c1:
            if c1 not in result_concepts:
                result_concepts.append(c2)
            if r not in result_relations:
                t = c1 + '  is-a  ' + c2
                relations.append(t)
                result_relations.append(r)
            if c2 != destination:
                find_relations_super_cycle_2(destination, c1, c2, result_relations, result_concepts, relations)
            else:
                if c2 == destination:
                    return True
                else:
                    return False


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


def find_cycle_2(destination, super, result_relations, result_concepts, relations, signs):
    for r in relations_edge:
        index = relations_edge.index(r)
        if signs[index] != 1:
            c1 = r[0]
            c2 = r[1]
            signs[index] = 1
            if r not in result_relations:
                if super == c1:
                    result_relations.append(r)
                    result_concepts.append(c1)
                    if destination == c2:
                        return True

                    else:
                        return find_cycle_2(destination, c2, result_relations, result_concepts, relations, signs)
    return False


def add_relation(ph, relations, phrase1, phrase2, direction, window):
    global selected_concept
    selected_concept = ''

    def destroy_equivalent_window(question_w, main_window, e):
        question_w.destroy()
        main_window.destroy()

    def select_concpet_to_keep(sub, super, main_window, result_relation_list):
        # Which concept name do the user want to keep, sub or super?
        question_window = Toplevel(root)
        question_window.title("Equivalent concept names")
        question_window.geometry("500x200+450+200")
        question_window.configure(background='white')
        ico = Image.open('logo_5.png')
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
        #for c in equivalent_concepts:
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
        ico = Image.open('logo_5.png')
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
                    command=lambda: select_concpet_to_keep(sub, super, window, result_relation_list))
        b2.grid(row=5, column=1, pady=5)
        window.lift()

    flag = False
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
                    result_relations = []
                    result_concepts = []
                    relations_set = []
                    flag = False
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
                        s = []
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


def add_to_concepts_exist(text):
    if text != "":
        index = listbox1.get(0, END).index(text)
        if listbox2_concept_origin.get(index) == '':
            listbox2_concept_origin.delete(index)
            listbox2_concept_origin.insert(index, '?')


def save_metadata_relation(textbox1):
    p1.config(text=listbox1_concept_names.get(ANCHOR))
    ph = p1.cget("text")
    if (ph != ''):
        index = main_concept_names.index(ph)
        list_relations = []
        list_ext_concepts = []
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


def output_file():
    # phrases
    book = xlwt.Workbook()
    sh = book.add_sheet("sheet_1")
    sh.write(0, 0, "Phrase")
    sh.write(0, 1, "Label")
    sh.write(0, 2, "Refined Form")
    sh.write(0, 3, "Meta data")
    sh.write(0, 4, "Extracted Concepts")
    counter = 1
    for i in phrases:
        index = phrases.index(i)
        sh.write(counter, 0, i)
        sh.write(counter, 1, FP_validation[index])
        sh.write(counter, 2, FP_metadata[index].get_refinedf())
        sh.write(counter, 3, FP_metadata[index].get_metadata())
        sh.write(counter, 4, FP_metadata[index].get_ext_concepts())
        counter += 1
    # concepts
    book_concepts = xlwt.Workbook()
    sh = book_concepts.add_sheet("sheet_2")
    sh.write(0, 0, "Concept")
    sh.write(0, 1, "Axioms")
    sh.write(0, 2, "Color")
    sh.write(0, 3, "Origin")
    counter = 1
    for i in main_concept_names:
        index = main_concept_names.index(i)
        sh.write(counter, 0, main_concepts[index].get_concpet_name())
        sh.write(counter, 1, main_concepts[index].get_concept_axioms())
        sh.write(counter, 2, main_concepts[index].get_concept_color())
        sh.write(counter, 3, main_concepts[index].get_concept_origin())
        counter += 1
    get_filename_excel(book, book_concepts)


def get_filename_excel(book, book_concepts):
    myFormats = [("Excel files", "*.xls")]
    filename = filedialog.asksaveasfilename(filetypes=myFormats)
    if filename:
        save_2(filename, book, book_concepts)


def save_2(name, book, book_concepts):
    name_main = name.rsplit('/', 1)[-1]
    if name and re.match("^[A-Za-z0-9_-]*$", name_main):
        output_name_phrases = name + "_phrases.xls"
        output_name_concpets = name + "_concepts.xls"
        book.save(output_name_phrases)
        book_concepts.save(output_name_concpets)
        messagebox.showinfo("info", "Output file has been saved!")
    else:
        messagebox.showerror("Error", "Please enter a valid name for output file!")


def save_as_owl():
    myFormats = [("OWL files", "*.owl")]
    filename = filedialog.asksaveasfilename(filetypes=myFormats)
    if filename:
        save_ontology_as_owl(filename)


def save_ontology_as_owl(name):
    name_main = name.rsplit('/', 1)[-1]
    if name and re.match("^[A-Za-z0-9_-]*$", name_main):
        output_name_2 = name + ".owl"
        file_name = output_name_2
        global ontology_help_owl
        if ontology_help_owl != '':
            onto = get_ontology(ontology_help_owl)
            for i in main_concept_names:
                class_names = onto.classes()
                if i not in class_names:
                    with onto:
                        NewClass = types.new_class(i, (Thing,))
                rela_2 = []
                index = main_concept_names.index(i)
                axioms = main_concepts[index].get_concept_axioms()
                for item in axioms:
                    rela_2.append(item)
                if len(rela_2) > 0:
                    NewClass.is_a.remove(owl.Thing)
                for x in rela_2:
                    if x not in onto.classes():
                        with onto:
                            NewClass2 = types.new_class(str(x), (Thing,))
                        NewClass.is_a.append(NewClass2)
                    else:
                        NewClass.is_a.append(x)
        onto.save(file=file_name, format="rdfxml")
        messagebox.showinfo("info", "Output file has been saved!")
    else:
        messagebox.showerror("Error", "Please enter a valid name for output file!")


def save_changes_to_existing_project_single_file():
    global existing_project_flag
    global existing_project_path
    if existing_project_flag == 1 and existing_project_path != '':
        #filename = os.path.expanduser('~') + existing_project_path
        filename = existing_project_path
        try:
            os.remove(filename)
        except OSError:
            pass
        name_main = filename.rsplit('/', 1)[-1]
        output = name_main + '.pkl'
        dictionary = {}
        phrases_to_save = [NodeType_phrase]
        for i in phrases:
            index = phrases.index(i)
            x = NodeType_phrase(i, FP_metadata_2[index].get_refinedf(), FP_metadata_2[index].get_ext_concepts(),
                                FP_metadata_2[index].get_phrase_color(), FP_validation[index],
                                FP_metadata_2[index].get_phrase_note(), FP_metadata_2[index].get_phrase_relatedc())
            x_mark = listbox_mark.itemcget(index, 'bg')
            phrases_to_save.append((x, x_mark))
        concepts_to_save = [NodeType_concepts]
        for i in main_concept_names:
            index = main_concept_names.index(i)
            c = main_concepts[index].get_concept_color_list()
            x = NodeType_concepts(i, main_concepts[index].get_concept_axioms(),
                                  main_concepts[index].get_super_concept_axioms(),
                                  main_concepts[index].get_concept_color(),
                                  main_concepts[index].get_concept_origin(),
                                  main_concepts[index].get_concept_note(), main_concepts[index].get_concept_color_list())
            x_mark = listbox_mark_concepts.itemcget(index, 'bg')
            concepts_to_save.append((x, x_mark))
        axiom_color_to_save = []
        for i in axiom_color_edge:
            index = axiom_color_edge.index(i)
            axiom_color_to_save.append((i, axiom_color[index]))
        ontology_phrases_path_to_save = []
        for i in ontology_loaded_path_values:
            ontology_phrases_path_to_save.append(('ontology', i))
        for i in phrases_loaded_path_values:
            ontology_phrases_path_to_save.append(('phrases', i))
        related_concept_exist_m_to_save = []
        for i in exist_m_related_concept:
            related_concept_exist_m_to_save.append(i)
        existing_project_flag = 1
        dictionary["phrases"] = phrases_to_save
        dictionary["concepts"] = concepts_to_save
        dictionary["axiom_color"] = axiom_color_to_save
        dictionary["ontology_phrases_path"] = ontology_phrases_path_to_save
        dictionary["related_concept_exist_m"] = related_concept_exist_m_to_save
        dictionary["equivalent_concepts"] = equivalent_concepts_list
        dictionary["concept_name_style"] = concept_name_style_var.get()
        filename_open = filename + '.pkl'
        os.path.join(filename, output)
        fp = open(filename_open, 'wb')
        pickle.dump(dictionary, fp)
        fp.close()
        m = "The changes has been saved to " + name_main
        messagebox.showinfo("info", m)
    else:
        info_window("You have not saved the project yet!", "Error", 3000)


def save_new_project_using_dic():
    def save_as_new_project(filename):
        name_main = filename.rsplit('/', 1)[-1]
        if filename and re.match("^[A-Za-z0-9_-]*$", name_main):
            global existing_project_flag
            existing_project_flag = 1
            global existing_project_path
            existing_project_path = filename
            output = name_main + '.pkl'
            dictionary = {}
            phrases_to_save = [NodeType_phrase]
            for i in phrases:
                index = phrases.index(i)
                x = NodeType_phrase(i, FP_metadata_2[index].get_refinedf(), FP_metadata_2[index].get_ext_concepts(),
                                    FP_metadata_2[index].get_phrase_color(), FP_validation[index],
                                    FP_metadata_2[index].get_phrase_note(), FP_metadata_2[index].get_phrase_relatedc())
                x_mark = listbox_mark.itemcget(index, 'bg')
                phrases_to_save.append((x, x_mark))
            concepts_to_save = [NodeType_concepts]
            for i in main_concept_names:
                index = main_concept_names.index(i)
                x = NodeType_concepts(i, main_concepts[index].get_concept_axioms(),
                                      main_concepts[index].get_super_concept_axioms(),
                                      main_concepts[index].get_concept_color(),
                                      main_concepts[index].get_concept_origin(),
                                      main_concepts[index].get_concept_note(), main_concepts[index].get_concept_color_list())
                x_mark = listbox_mark_concepts.itemcget(index, 'bg')
                concepts_to_save.append((x, x_mark))
            axiom_color_to_save = []
            for i in axiom_color_edge:
                index = axiom_color_edge.index(i)
                axiom_color_to_save.append((i, axiom_color[index]))
            ontology_phrases_path_to_save = []
            for i in ontology_loaded_path_values:
                ontology_phrases_path_to_save.append(('ontology', i))
            for i in phrases_loaded_path_values:
                ontology_phrases_path_to_save.append(('phrases', i))
            related_concept_exist_m_to_save = []
            for i in exist_m_related_concept:
                related_concept_exist_m_to_save.append(i)
            existing_project_flag = 1
            dictionary["phrases"] = phrases_to_save
            dictionary["concepts"] = concepts_to_save
            dictionary["axiom_color"] = axiom_color_to_save
            dictionary["ontology_phrases_path"] = ontology_phrases_path_to_save
            dictionary["related_concept_exist_m"] = related_concept_exist_m_to_save
            dictionary["equivalent_concepts"] = equivalent_concepts_list
            dictionary["concept_name_style"] = concept_name_style_var.get()
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
        save_as_new_project(filename)


def new_project():
    restart()
    restart_new_ontology()
    global previous_tab_id
    global previous_tab_id
    previous_tab_id = 0
    previous_tab_id_concept = 0
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
    FP_validation.clear()
    exist_m_related_concept.clear()
    FP_metadata.clear()
    FP_metadata_2.clear()
    FP_metadata_md.clear()
    FP_metadata_refined.clear()
    main_relation_edge.clear()
    relations_edge.clear()
    all_phrases.clear()
    listbox1.delete(0, END)
    listbox2.delete(0, END)
    listbox_mark.delete(0, END)
    notebook_main.select(load_necessary_files_window)


def open_a_working_project_single_file():
    project_path = filedialog.askopenfilename()
    if project_path:
        global previous_tab_id
        global previous_tab_id
        previous_tab_id = 0
        previous_tab_id_concept = 0
        restart()
        try:
            filename = project_path
            s = filename.rsplit('/')[-1]
            x = s.replace('.pkl', '')
            project_name = 'Project Name: ' + x + '     (' + filename + ')'
            project_saved_path.config(text=project_name, font='Helvetica 11')
            input_file = open(filename, 'rb')
            dictionary = {}
            dictionary = pickle.load(input_file)
            phrases_input_file = dictionary["phrases"]
            concepts_input_file = dictionary["concepts"]
            axiom_color_input_file = dictionary["axiom_color"]
            ontology_phrases_path_input_file = dictionary["ontology_phrases_path"]
            related_concept_exist_m_input_file = dictionary["related_concept_exist_m"]
            equivalent_concepts_input_file = dictionary["equivalent_concepts"]
            concept_name_style = dictionary["concept_name_style"]
            concept_name_style_var.set(concept_name_style)
            x = NodeType_concepts('', [], [], '', '', '', '')
            flag = 0
            main_concepts.clear()
            main_concept_names.clear()
            for line in concepts_input_file:
                if flag == 1:
                    x = line[0]
                    main_concept_names.append(x.get_concpet_name())
                    main_concepts.append(x)
                    listbox1_concept_names.insert(END, x.get_concpet_name())
                    listbox1_concept_names.itemconfig(END, fg=x.get_concept_color())
                    listbox1_concept_names_only.insert(END, x.get_concpet_name())
                    listbox1_concept_names_only.itemconfig(END, fg=x.get_concept_color())
                    if x.get_concept_origin() != "main":
                        listbox2_concept_origin.insert(END, x.get_concept_origin())
                        listbox2_concept_origin.itemconfig(END, fg=x.get_concept_color())
                        listbox2_concept_origin_only.insert(END, x.get_concept_origin())
                        listbox2_concept_origin_only.itemconfig(END, fg=x.get_concept_color())
                    else:
                        listbox2_concept_origin.insert(END, " ")
                        listbox2_concept_origin_only.insert(END, " ")
                    listbox_mark_concepts.insert(END, " ")
                    listbox_mark_concepts.itemconfig(END, bg=line[1])
                    listbox_mark_concepts_only.insert(END, " ")
                    if line[1] == 'red':
                        listbox_mark_concepts_only.itemconfig(END, bg='darkred')
                    else:
                        listbox_mark_concepts_only.itemconfig(END, bg=line[1])
                else:
                    flag = 1
            x = NodeType_phrase('', '', '', '', '', '', '')
            flag = 0
            for line in phrases_input_file:
                if flag == 1:
                    x = line[0]
                    phrases.append(x.get_phrase_name())
                    s = x.get_phrase_related_concepts()
                    t = NodeType(' ', x.get_phrase_refinedf(), x.get_ext_concepts(), x.get_phrase_color(),
                                 x.get_phrase_note(), x.get_phrase_related_concepts())
                    FP_metadata_2.append(t)
                    FP_metadata.append(t)
                    FP_validation.append(x.get_phrase_label())

                    listbox1.insert(END, x.get_phrase_name())
                    listbox2.insert(END, x.get_phrase_label())
                    fg_color = x.get_phrase_color()
                    if fg_color and fg_color != " ":
                        listbox1.itemconfig(END, fg=fg_color)
                        listbox2.itemconfig(END, fg=fg_color)
                    listbox_mark.insert(END, ' ')
                    listbox_mark.itemconfig(END, bg=line[1])
                    listbox1_phrase_only.insert(END, x.get_phrase_name())
                    listbox2_phrase_only.insert(END, x.get_phrase_label())
                    fg_color = x.get_phrase_color()
                    if fg_color and fg_color != " ":
                        listbox1_phrase_only.itemconfig(END, fg=fg_color)
                        listbox2_phrase_only.itemconfig(END, fg=fg_color)
                    listbox_mark_phrase_only.insert(END, ' ')
                    if line[1] == 'red':
                        listbox_mark_phrase_only.itemconfig(END, bg='darkred')
                    else:
                        listbox_mark_phrase_only.itemconfig(END, bg=line[1])
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
            ontology_loaded_path.delete('1.0', END)
            phrases_loaded_path.delete('1.0', END)
            flag_ontology_path = 0
            flag_phrases_path = 0
            for line in ontology_phrases_path_input_file:
                if line[0] == 'ontology':
                    ontology_loaded_path.insert(END, line[1])
                    ontology_loaded_path.insert(END, '\n')
                    ontology_loaded_path_values.append(line[1])
                    flag_ontology_path = 1
                else:
                    phrases_loaded_path.insert(END, line[1])
                    phrases_loaded_path.insert(END, '\n')
                    phrases_loaded_path_values.append(line[1])
                    flag_phrases_path = 1
            if flag_ontology_path == 1:
                ontology_loaded_label.config(text="The ontology has been loaded successfully.",
                                             font='Helvetica 11 bold')
            if flag_phrases_path == 1:
                phrases_loaded_label.config(text="Frequent phrases has been loaded successfully.",
                                            font='Helvetica 11 bold')
            ontology_loaded_path.config(state="disabled")
            phrases_loaded_path.config(state="disabled")
            if ontology_loaded_path_values[0]:
                global ontology_help_owl
                ontology_help_owl = ontology_loaded_path_values[0]
            global existing_project_flag
            existing_project_flag = 1
            global existing_project_path
            existing_project_path = project_path
            if existing_project_path.endswith(".pkl"):
                existing_project_path = existing_project_path[:-4]
            exist_m_related_concept.clear()
            for line in related_concept_exist_m_input_file:
                exist_m_related_concept.append(line)
            equivalent_concepts_list.clear()
            for line in equivalent_concepts_input_file:
                equivalent_concepts_list.append(line)
        except:
            messagebox.showerror("Error", "The project cannot be loaded!")
            pass


def restart():
    global p1, p2
    p1.config(text='')
    p2.config(text='')
    global concept_name, concept_origin
    concept_name.config(text='')
    concept_origin.config(text='')
    global listbox1
    global listbox2
    global listbox_mark
    listbox1.delete(0, END)
    listbox2.delete(0, END)
    listbox1_concept_names.delete(0, END)
    listbox2_concept_origin.delete(0, END)
    listbox1_concept_names_only.delete(0, END)
    listbox2_concept_origin_only.delete(0, END)
    listbox_mark_concepts.delete(0, END)
    listbox_mark_concepts_only.delete(0, END)
    listbox_mark.delete(0, END)
    p1_phrase_only.config(text='')
    p2_phrase_only.config(text='')
    global listbox1_phrase_only
    global listbox2_phrase_only
    global listbox_mark_phrase_only
    listbox1_phrase_only.delete(0, END)
    listbox2_phrase_only.delete(0, END)
    listbox_mark_phrase_only.delete(0, END)
    global input_phrases
    input_phrases = []
    global phrases
    global FP_validation
    global FP_metadata
    global FP_metadata_2
    global FP_metadata_md
    global FP_metadata_refined
    global exist_m_related_concept
    phrases.clear()
    FP_validation.clear()
    exist_m_related_concept.clear()
    FP_metadata.clear()
    FP_metadata_2.clear()
    FP_metadata_md = []
    FP_metadata_refined = []
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
    global all_phrases
    global concepts
    global root
    all_phrases.clear()
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
    global window_phrase_note_view_only
    if window_phrase_note_view_only:
        window_phrase_note_view_only.destroy()
    global window_phrase_matching_view
    if window_phrase_matching_view:
        window_phrase_matching_view.destroy()
    if window_concept_only:
        window_concept_only.destroy()
    global window_concept_only_note_view
    if window_concept_only_note_view:
        window_concept_only_note_view.destroy()
    ontology_loaded_path.config(state="normal")
    phrases_loaded_path.config(state="normal")
    ontology_loaded_path.delete('1.0', END)
    phrases_loaded_path.delete('1.0', END)
    ontology_loaded_path_values.clear()
    phrases_loaded_path_values.clear()
    ontology_loaded_label.config(text="")
    phrases_loaded_label.config(text="")
    ontology_loaded_path.config(state="disabled")
    phrases_loaded_path.config(state="disabled")
    global axiom_color_edge
    axiom_color_edge.clear()
    project_saved_path.config(text="")

    global load_super_sub_phrases_path
    load_super_sub_phrases_path = []
    global sub_super_p_button_color_yes
    sub_super_p_button_color_yes = 'lightBlue1'
    global sub_super_p_button_color_no
    sub_super_p_button_color_no = 'lightBlue1'
    global equivalent_concepts_list
    equivalent_concepts_list.clear()


def display_equivalent_concepts():
    window = Toplevel(root)
    window.title("INFORMATION:   Equivalent Concepts")
    window.geometry("500x300+450+100")
    ico = Image.open('logo_5.png')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)
    window.configure(background='white')
    listbox_equivalent_concepts = Listbox(window, borderwidth=0, highlightthickness=0)
    listbox_equivalent_concepts.pack(padx=10, pady=10)
    listbox_equivalent_concepts.config(width=0, height=0)
    counter = 0
    list_counter = 0
    if equivalent_concepts_list != []:
        for list in equivalent_concepts_list:
            temp = []
            list_counter += 1
            text = "List "+ str(list_counter)+ " : equivalmet concepts"
            listbox_equivalent_concepts.insert(END,text)
            listbox_equivalent_concepts.itemconfig(END, fg='black', bg = 'powderblue')
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
    window.focus()


def display_all_axioms():
    def destroy_all_axioms_window(e):
        global flag_display_all_axioms
        flag_display_all_axioms = 0
    global flag_display_all_axioms
    if flag_display_all_axioms == 0:
        flag_display_all_axioms = 1
    window = Toplevel(root)
    window.title("INFORMATION: Axioms of the Ontology")
    window.geometry("500x300+450+100")
    # window.resizable(0, 0)
    ico = Image.open('logo_5.png')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)
    window.configure(background='white')
    listbox_all_axioms = Listbox(window, borderwidth=0, highlightthickness=0)
    listbox_all_axioms.pack(padx=10, pady=10)
    listbox_all_axioms.config(width=0, height=0)
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
    window.focus()
    window.bind("<Destroy>", destroy_all_axioms_window)
    listbox_all_axioms.bind('<Double-Button-1>', lambda event: listbox_copy(listbox_all_axioms, event))


def listbox_copy(listbox, event):
    root.clipboard_clear()
    selected = listbox.get(ANCHOR)
    root.clipboard_append(selected)


def update(data):
    listbox_search.delete(0, END)
    for item in data:
        listbox_search.insert(END, item)


def fillout(e):
    search.delete(0, END)
    search.insert(0, listbox_search.get(ACTIVE))


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


def search_click_phrases(e):
    try:
        curselection = listbox_search.curselection()[0]
        search.delete(0, END)
        search.insert(0, listbox_search.get(curselection))
        clear_seached_phrase()
        s = listbox_search.get(curselection)
        i = phrases.index(s)
        listbox1.see(i)
        listbox1.itemconfig(i, {'bg': 'lightBlue1'})
        global index_searched
        index_searched = i
        notebook_main.select(higher_view_phrase_window)
    except:
        pass


def search_click_concepts(e):
    try:
        curselection = listbox_search.curselection()[0]
        search.delete(0, END)
        search.insert(0, listbox_search.get(curselection))
        clear_seached_concepts()
        s = listbox_search.get(curselection)
        i = main_concept_names.index(s)
        listbox1_concept_names.see(i)
        listbox1_concept_names.itemconfig(i, {'bg': 'lightBlue1'})
        listbox2_concept_origin.itemconfig(i, {'bg': 'lightBlue1'})
        global index_searched
        index_searched = i
        notebook_main.select(higher_view_concept_window)
    except:
        pass


def clear_seached_phrase():
    for item in phrases:
        i = phrases.index(item)
        listbox1.itemconfig(i, {'bg': 'white'})
    for item in main_concept_names:
        i = main_concept_names.index(item)
        listbox1_concept_names.itemconfig(i, {'bg': 'white'})


def clear_seached_concepts():
    for item in main_concept_names:
        i = main_concept_names.index(item)
        listbox1_concept_names.itemconfig(i, {'bg': 'white'})
        listbox2_concept_origin.itemconfig(i, {'bg': 'white'})


def OnMouseWheel_function(e, listname):
    listname.yview_scroll(-1 * int(e.delta / 120), "units")
    return "break"


def mdo_info():
    global main_classes_visualization
    main_classes_visualization.clear()
    for c in main_concept_names:
        main_classes_visualization.append(c)
    network_visualization()


def network_visualization():
    G = nx.DiGraph()
    #relations_edge = []
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

def set_previous_tab_index_concepts_only(e):
    global previous_tab_id_concept_only
    try:
        previous_tab_id_concept_only = notebook_concepts_only.index(notebook_concepts_only.select())
    except:
        pass


def network_visulaization_pyvis(G):
    nt = Network(width="1000px", height="700px", directed=True)
    temp_concepts = []
    for i in main_classes:
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
    nt.show("nx.html")


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


def focus_on_concept_axioms():
    def click_on_concept_axiom_focus(e):
        clear_seached_concepts()
        s = listbox_axiom_focus.get(ACTIVE)
        i = main_concept_names.index(s)
        listbox1_concept_names.see(i)
        listbox1_concept_names.itemconfig(i, {'bg': 'lightBlue1'})
        listbox2_concept_origin.itemconfig(i, {'bg': 'lightBlue1'})
        notebook_main.select(higher_view_concept_window)

    try:
        p1.config(text=listbox1_concept_names.get(ANCHOR))
        ph = p1.cget("text")
        if ph != '':
            index = main_concept_names.index(ph)
            p2.config(text=listbox2_concept_origin.get(index))
            global window_concept_axiom_focus_view
            if window_concept_axiom_focus_view:
                window_concept_axiom_focus_view.destroy()
                window_concept_axiom_focus_view = Frame(notebook_concepts, width=950, height=490, bg="white")

            Frame3 = Frame(window_concept_axiom_focus_view, borderwidth=0, bg='white')
            Label(Frame3, text=ph, bg='white', font='Helvetica 9 bold', relief='groove', wraplength=170).grid(row=2,
                                                                                                              column=1)
            Label(Frame3, text="is-a", bg='white', font='Helvetica 9 bold', relief='groove', wraplength=200).grid(row=2,
                                                                                                                  column=2,
                                                                                                                  padx=5)

            listbox_axiom_focus = Listbox(Frame3, width=30, height=5)
            scrollbary_axiom_focus = Scrollbar(Frame3, orient=VERTICAL)
            listbox_axiom_focus.config(yscrollcommand=scrollbary_axiom_focus.set)
            scrollbary_axiom_focus.config(command=listbox_axiom_focus.yview)
            scrollbary_axiom_focus.grid(row=2, column=4, sticky="ns")
            listbox_axiom_focus.bind("<MouseWheel>",
                                     lambda event: OnMouseWheel_function(e=event, listname=listbox_axiom_focus))
            listbox_axiom_focus.grid(row=2, column=3, padx=1)

            Label(Frame3, text='Super axioms', bg='white', font='Helvetica 9 bold').grid(row=0, column=5)
            listbox_axiom_focus_super = Listbox(Frame3, width=70, height=9)
            scrollbary_axiom_focus_super = Scrollbar(Frame3, orient=VERTICAL)
            listbox_axiom_focus_super.config(yscrollcommand=scrollbary_axiom_focus_super.set)
            scrollbary_axiom_focus_super.config(command=listbox_axiom_focus_super.yview)
            scrollbary_axiom_focus_super.grid(row=1, column=6, sticky="ns")
            listbox_axiom_focus_super.bind("<MouseWheel>", lambda event: OnMouseWheel_function(e=event,
                                                                                               listname=listbox_axiom_focus_super))
            listbox_axiom_focus_super.grid(row=1, column=5, pady=3)

            Label(Frame3, text='Sub axioms', bg='white', font='Helvetica 9 bold').grid(row=3, column=5)
            listbox_axiom_focus_sub = Listbox(Frame3, width=70, height=9)
            scrollbary_axiom_focus_sub = Scrollbar(Frame3, orient=VERTICAL)
            listbox_axiom_focus_sub.config(yscrollcommand=scrollbary_axiom_focus_sub.set)
            scrollbary_axiom_focus_sub.config(command=listbox_axiom_focus_sub.yview)
            scrollbary_axiom_focus_sub.grid(row=4, column=6, sticky="ns")
            listbox_axiom_focus_sub.bind("<MouseWheel>",
                                         lambda event: OnMouseWheel_function(e=event, listname=listbox_axiom_focus_sub))
            listbox_axiom_focus_sub.grid(row=4, column=5)

            Frame3.place(x=10, y=10)

            i = main_concept_names.index(ph)
            r = main_concepts[i].get_concept_axioms()
            if r:
                for item in r:
                    if "is-a" not in item:
                        listbox_axiom_focus.insert(END, item)
                    else:
                        j = item.split("is-a", 1)[1]
                        j = j.replace(" ", "")
                        listbox_axiom_focus.insert(END, j)

            listbox_axiom_focus.bind("<Double-Button-1>", click_on_concept_axiom_focus)
            listbox_axiom_focus.bind('<FocusOut>', lambda e: clear_seached_concepts())

            for item in listbox_axiom_focus.get(0, END):
                result_relations = []
                result_concepts = []
                relations = []
                result_concepts, result_relations, relations = find_relations_super(item, result_relations,
                                                                                    result_concepts, relations)
                listbox_axiom_focus_super.delete(0, END)
                count = 0
                for r in relations:
                    listbox_axiom_focus_super.insert(END, r)
                    if count == 0:
                        listbox_axiom_focus_super.itemconfig(END, {'bg': 'lavender'})
                        count = 1
                    else:
                        count = 0

                result_relations_sub = []
                result_concepts_sub = []
                relations_sub = []
                result_concepts_sub, result_relations_sub, relations_sub = find_relations_sub(ph, result_relations_sub,
                                                                                              result_concepts_sub,
                                                                                              relations_sub)
                listbox_axiom_focus_sub.delete(0, END)
                count = 0
                for r in relations_sub:
                    listbox_axiom_focus_sub.insert(END, r)
                    if count == 0:
                        listbox_axiom_focus_sub.itemconfig(END, {'bg': 'lavender'})
                        count = 1
                    else:
                        count = 0
            listbox_axiom_focus_sub.bind('<FocusOut>', lambda e: listbox_axiom_focus_sub.selection_clear(0, END))
            listbox_axiom_focus_super.bind('<FocusOut>', lambda e: listbox_axiom_focus_super.selection_clear(0, END))
            listbox_axiom_focus.bind('<FocusOut>', lambda e: listbox_axiom_focus.selection_clear(0, END))
            '''
            Button7 = Button(window_concept_axiom_focus_view, text="Close Tab", width=10, fg='black', bg='lightBlue1',
                             font=('comicsans', 10), command=lambda: close_tab(window_concept_axiom_focus_view))
            Button7.place(x=10, y=420)
            '''
            notebook_concepts.add(window_concept_axiom_focus_view, text="Focus on axioms")
            notebook_concepts.select(window_concept_axiom_focus_view)
    except:
        pass


def font_change(event):
    '''
    if event.width in range(300, 1100):
        my_font.configure(size=8)
    elif event.width in range(1101, 425):
        my_font.configure(size=20)
    elif event.width > 600:
        my_font.configure(size=30)
    fontsize.configure(size=font_size)
    '''
    # '''
    # print(event.widget, event)  # See what is happening
    # Base size
    # 1100x630
    normal_width = 1100  # 200
    normal_height = 630  # 100
    # Screen
    screen_width = event.width
    screen_height = event.height
    if event.widget != root:
        return None  # Jump out of the function if the widget firing configure isn't root
    # Get percentage of screen size from Base size
    percentage_width = screen_width / (normal_width / 100)
    percentage_height = screen_height / (normal_height / 100)
    minimum_size = 10
    # Make a scaling factor
    scale_factor = ((percentage_width + percentage_height) / 2) / 100
    # Set the fontsize based on scale_factor,
    # if the fontsize is less than minimum_size
    # it is set to the minimum size
    # font_size is the variable to store actual size
    if scale_factor > minimum_size / 18:
        font_size = int(10 * scale_factor)
    else:
        font_size = minimum_size
    fontsize.configure(size=font_size)


def mark_phrase_done_button():
    p1.config(text=listbox1.get(ANCHOR))
    ph = p1.cget("text")
    if (ph != ''):
        i = phrases.index(ph)
        listbox1.itemconfig(i, fg='green')
        listbox2.itemconfig(i, fg='green')
        FP_metadata_2[i].set_phrase_color('green')
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
                p2.config(text=listbox2.get(index))
                add_meta_data_tab(ph)
                matching_tab(ph)
                add_note_phrase(ph)
                if previous_tab_id == 0:
                    notebook_phrases.select(window_phrase_add_metadata_view)
                else:
                    notebook_phrases.select(window_phrase_note_view)
                p1.config(text=listbox1.get(index))
                p2.config(text=listbox2.get(index))
            except:
                pass


def on_enter_label(e, message):
    toolTip.showtip(message)


def on_leave_label(e):
    toolTip.hidetip()


def yview_main_phrase_only(*args):
    """ scroll both listboxes together """
    listbox1_phrase_only.yview(*args)
    listbox2_phrase_only.yview(*args)
    listbox_mark_phrase_only.yview(*args)


def OnMouseWheel_phrase_only(event):
    listbox1_phrase_only.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox2_phrase_only.yview_scroll(-1 * int(event.delta / 120), "units")
    listbox_mark_phrase_only.yview_scroll(-1 * int(event.delta / 120), "units")
    return "break"


def mark_phrase_only_tab(e):
    try:
        curselection = listbox_mark_phrase_only.curselection()
        index = curselection[0]
        bg_color = listbox_mark_phrase_only.itemcget(index, "background")


        if bg_color == 'darkred':
            listbox_mark_phrase_only.itemconfig(index, {'bg': 'white'})
            listbox_mark_phrase_only.selection_clear(0, END)
            listbox_mark.itemconfig(index, {'bg': 'white'})
            listbox_mark.selection_clear(0, END)
        else:
            listbox_mark_phrase_only.itemconfig(index, {'bg': 'darkred'})
            listbox_mark_phrase_only.selection_clear(0, END)
            listbox_mark.itemconfig(index, {'bg': 'red'})
            listbox_mark.selection_clear(0, END)
    except:
        return None


def add_note_phrase_only(ph):
    class AutoScrollbar(Scrollbar):
        # a scrollbar that hides itself if it's not needed.  only
        # works if you use the grid geometry manager.
        def set(self, lo, hi):
            if float(lo) <= 0.0 and float(hi) >= 1.0:
                # grid_remove is currently missing from Tkinter!
                self.pack_forget()
            else:
                if self.cget("orient") == HORIZONTAL:
                    self.pack(fill=X)
                else:
                    self.pack(fill=Y)
            Scrollbar.set(self, lo, hi)

        def grid(self, **kw):
            raise TclError  # , "cannot use grid with this widget"

        def place(self, **kw):
            raise TclError  # , "cannot use place with this widget"

    i = phrases.index(ph)
    global window_phrase_note_view_only
    if window_phrase_note_view_only:
        window_phrase_note_view_only.destroy()
        window_phrase_note_view_only = Frame(notebook_phrases_only, bg="white")  # , width=950, height=450
    Frame_note = Frame(window_phrase_note_view_only, borderwidth=1, bg='white')
    textbox_note = Text(Frame_note, width=100, height=25, undo=True, borderwidth=0)
    textbox_note.pack(fill=Y, expand=True, anchor=W)  # fill='both', side="left", fill=BOTH, expand=True
    b = Button(Frame_note, text="Save changes", width=15, fg='black', bg='lightBlue1', font=('comicsans', 12),
               command=lambda: save_phrase_note((textbox_note.get("1.0", END)[:-1]), ph))
    b.pack(padx=1, pady=10)
    Frame_note.pack(fill='both', expand=True)
    notebook_phrases_only.add(window_phrase_note_view_only, text="Note")
    textbox_note.delete('1.0', END)
    textbox_note.insert('1.0', FP_metadata_2[i].get_phrase_note())


def click_on_phrase_only(e):
    try:
        curselection = listbox1_phrase_only.curselection()[0]
        p1_phrase_only.config(text=listbox1_phrase_only.get(curselection))
        ph = p1_phrase_only.cget("text")
        if ph != '':
            index = phrases.index(ph)
            p2_phrase_only.config(text=listbox2_phrase_only.get(index))
            matching_tab(ph)
            add_note_phrase_only(ph)
            global previous_tab_id_phrase_only
            if previous_tab_id_phrase_only == 0:
                notebook_phrases_only.select(window_phrase_matching_view)
            else:
                notebook_phrases_only.select(window_phrase_note_view_only)
    except:
        pass


def set_previous_tab_index_phrases_only(e):
    global previous_tab_id_phrase_only
    try:
        previous_tab_id_phrase_only = notebook_phrases_only.index(notebook_phrases_only.select())
    except:
        pass


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


def mark_concept_only(e):
    try:
        curselection = listbox_mark_concepts_only.curselection()
        index = curselection[0]
        bg_color = listbox_mark_concepts_only.itemcget(index, "background")
        if bg_color == 'darkred':
            listbox_mark_concepts_only.itemconfig(index, {'bg': 'white'})
            listbox_mark_concepts_only.selection_clear(0, END)
            listbox_mark_concepts.itemconfig(index, {'bg': 'white'})
            listbox_mark_concepts.selection_clear(0, END)
        else:
            listbox_mark_concepts_only.itemconfig(index, {'bg': 'darkred'})
            listbox_mark_concepts_only.selection_clear(0, END)
            listbox_mark_concepts.itemconfig(index, {'bg': 'red'})
            listbox_mark_concepts.selection_clear(0, END)
    except:
        return None


def click_on_concept_only(e):
    def refresh_concept_only_tab(ph):
        try:
            if ph != '':
                index = main_concept_names.index(ph)
                concept_origin.config(text=" ")
                global window_concept_only
                if window_concept_only:
                    window_concept_only.destroy()
                global window_concept_only_note_view
                if window_concept_only_note_view:
                    window_concept_only_note_view.destroy()
                cocenpt_only_tab1(ph)
                concept_only_note(ph)

                if previous_tab_id_concept_only == 0:
                    notebook_concepts_only.select(window_concept_only)
                else:
                    notebook_concepts_only.select(window_concept_only_note_view)
        except:
            pass

    def add_to_concepts_conceptonlytab(text, ph):
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
                index = main_concept_names.index(temp_name)
                x_concept = NodeType_concepts(temp_name, [], [], 'darkred', ph, ' ', 'darkred')
                main_concepts.append(x_concept)
                listbox1_concept_names.insert(END, temp_name)
                listbox2_concept_origin.insert(END, "")
                listbox_mark_concepts.insert(END, " ")
                listbox1_concept_names_only.insert(END, temp_name)
                listbox1_concept_names_only.see(END)
                listbox2_concept_origin_only.insert(END, "")
                listbox_mark_concepts_only.insert(END, " ")
                i = listbox1_concept_names.get(0, END).index(temp_name)
                listbox1_concept_names.itemconfig(i, fg='darkred')
                listbox2_concept_origin.itemconfig(i, fg='darkred')
                listbox1_concept_names_only.itemconfig(i, fg='darkred')
                listbox2_concept_origin_only.itemconfig(i, fg='darkred')
                refresh_concept_only_tab(ph)
            else:
                messagebox.showerror("Error", "The extracted concept has already defined!")
            textbox.delete('1.0', END)

    def cocenpt_only_tab1(ph):
        global window_concept_only
        if window_concept_only:
            window_concept_only.destroy()
            window_concept_only = Frame(notebook_concepts_only, bg="white")  # width=950, height=490,

        Frame50 = Frame(window_concept_only, borderwidth=1, bg='whitesmoke')
        Label(Frame50, text='Define a New Concept', bg='whitesmoke', font='Helvetica 10 bold', fg='black').grid(row=0,
                                                                                                                column=0)
        global textbox
        textbox = Text(Frame50, width=35, height=2, undo=True, borderwidth=2)
        textbox.grid(row=1, column=0, padx=5)  # sticky='w',
        Button12 = Button(Frame50, text="Add to Concepts", width=12, fg='black', bg='lightBlue1',
                          font=('comicsans', 11),
                          command=lambda: add_to_concepts_conceptonlytab((textbox.get("1.0", END)[:-1]), ph))
        Button12.grid(row=1, column=1, padx=10)
        Frame50.grid(row=0, column=0, sticky='e', padx=20, pady=20)

        notebook_concepts_only.add(window_concept_only, text="Focus on Concepts")

    def concept_only_note(ph):
        i = main_concept_names.index(ph)
        global window_concept_only_note_view
        if window_concept_only_note_view:
            window_concept_only_note_view.destroy()
            window_concept_only_note_view = Frame(notebook_concepts_only, bg="white")
        Frame_note = Frame(window_concept_only_note_view, borderwidth=1, bg='white')
        textbox_note = Text(Frame_note, width=100, height=25, undo=True, borderwidth=0)  # , width=30, height=2,
        textbox_note.pack(fill='both', expand=True)
        b = Button(Frame_note, text="Save changes", width=15, fg='black', bg='lightBlue1', font=('comicsans', 12),
                   command=lambda: save_concept_note((textbox_note.get("1.0", END)[:-1]), ph))
        b.pack(padx=1, pady=10)
        Frame_note.pack(fill='both', expand=True)
        notebook_concepts_only.add(window_concept_only_note_view, text="Note")
        textbox_note.delete('1.0', END)
        textbox_note.insert('1.0', main_concepts[i].get_concept_note())

    try:
        if window_concept_only:
            window_concept_axiom_focus_view.destroy()
        if window_concept_only_note_view:
            window_concept_only_note_view.destroy()
        curselection = listbox1_concept_names_only.curselection()[0]
        concept_name_only.config(text=listbox1_concept_names_only.get(curselection))
        ph = concept_name_only.cget("text")
        if ph != '':
            index = main_concept_names.index(ph)
            concept_origin_only.config(text=listbox2_concept_origin_only.get(index))
            cocenpt_only_tab1(ph)
            concept_only_note(ph)
            if previous_tab_id_concept_only == 0:
                notebook_concepts_only.select(window_concept_only)
            else:
                notebook_concepts_only.select(window_concept_only_note_view)
    except:
        pass


global root
root = Tk()
root.configure(background='white')
root.title('Ontology Extension System')
root.geometry("1100x630+100+1")

ico = Image.open('logo_5.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

global x_position
global y_position
x_position = y_position = 0

main_menu = Menu(root, tearoff=False)
root.config(menu=main_menu)

global fontsize
fontsize = font.Font(size=10)

root.bind('<Configure>', font_change)

file_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="File", menu=file_menu)
save_menu = Menu(file_menu, tearoff=False)
file_menu.add_command(label="New project", command=new_project)
file_menu.add_separator()
file_menu.add_command(label="Open project", command=open_a_working_project_single_file)
file_menu.add_separator()
file_menu.add_cascade(label="Save", menu=save_menu)
file_menu.add_separator()
save_menu.add_command(label="Save as a new project", command=save_new_project_using_dic)
save_menu.add_separator()
save_menu.add_command(label="Save changes to current project", command=save_changes_to_existing_project_single_file)
save_menu.add_separator()
save_menu.add_command(label="Save as Excel", command=output_file)
save_menu.add_separator()
save_menu.add_command(label="Save as OWL", command=save_as_owl)
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

visualize_menu = Menu(main_menu, tearoff=False)
main_menu.add_cascade(label="Ontology Visualization", menu=visualize_menu)
visualize_menu.add_command(label="Display ontology visualization in browser", command=mdo_info)

global main_concept_names
main_concept_names = []
global main_concepts
main_concepts = [NodeType_concepts]

global existing_project_flag
existing_project_flag = 0
global existing_project_path
existing_project_path = ''

global notebook_main
notebook_main = ttk.Notebook(root)
notebook_main.pack(expand=1, fill="both")

global load_necessary_files_window
load_necessary_files_window = Frame(notebook_main, bg="white")
l1 = Label(load_necessary_files_window, text='1:', bg='white', font='Helvetica 12 bold')
l1.grid(row=0, column=0, padx=10, pady=20)
load_ontology_button = Button(load_necessary_files_window, text="Load Ontology", fg='black', bg='lightBlue1',
                              font=('comicsans', 11), command=load_ontology)
load_ontology_button.grid(row=0, column=1, padx=10, pady=20)

global ontology_loaded_label
ontology_loaded_label = Label(load_necessary_files_window, text='', bg='white', fg='navy')
ontology_loaded_label.grid(row=0, column=2, padx=10, pady=5, sticky='w')
global project_saved_path
project_saved_path = Label(load_necessary_files_window, text='', bg='white', fg='navy')
project_saved_path.grid(row=4, column=2, pady=10, sticky='w')
global ontology_loaded_path
ontology_loaded_path = Text(load_necessary_files_window, font=('comicsans', 9), borderwidth=0, height=5, wrap=WORD,
                            width=70)
ontology_loaded_path.config(state="disabled")
ontology_loaded_path.grid(row=1, column=2, padx=10, sticky='w')

global ontology_loaded_path_values
ontology_loaded_path_values = []
global phrases_loaded_path_values
phrases_loaded_path_values = []

l2 = Label(load_necessary_files_window, text='2:', bg='white', font='Helvetica 12 bold')
l2.grid(row=2, column=0, padx=10, pady=40)
load_phrases_button = Button(load_necessary_files_window, text="Load Frequent Phrases", fg='black', bg='lightBlue1',
                             font=('comicsans', 11), command=load_phrases)
load_phrases_button.grid(row=2, column=1, padx=10, pady=40)
global phrases_loaded_label
phrases_loaded_label = Label(load_necessary_files_window, text='', bg='white', fg='navy')
phrases_loaded_label.grid(row=2, column=2, padx=10, pady=5, sticky='w')
global phrases_loaded_path
phrases_loaded_path = Text(load_necessary_files_window, font=('comicsans', 9), borderwidth=0, height=5, wrap=WORD,
                           width=90)
phrases_loaded_path.grid(row=3, column=2, padx=10, sticky='w')

Frame_conceptN_style = Frame(load_necessary_files_window, borderwidth=1, bg='whitesmoke')
Label(Frame_conceptN_style, text='Select the style for Concept Names:', bg='white', font='Helvetica 11 bold', fg='navy').grid(row=0, column=1, sticky='W')
global concept_name_style_var
concept_name_style_var = IntVar()
concept_name_style_var.set(0)
b1 = Radiobutton(Frame_conceptN_style, text="No-Style", variable=concept_name_style_var, value=0, bg='whitesmoke')#,command=concept_name_no_syle
b1.grid(row=1, column=1, sticky='W')
b2 = Radiobutton(Frame_conceptN_style, text="CamelCase-Style", variable=concept_name_style_var,value=1, bg='whitesmoke')#, command=concept_name_mdo_style
b2.grid(row=2, column=1, sticky='W')
#concept_name_style_var.set(0)
Frame_conceptN_style.grid(row=5, column=1, padx=10, pady=5, sticky='w')

global notebook_set_up
notebook_set_up = ttk.Notebook(load_necessary_files_window)
notebook_main.add(load_necessary_files_window, text="Set-up")

load_phrases_button.bind("<Enter>", lambda e: on_enter_label(e,
                                                             "Load TEXT file\\files of frequent phrases"))
load_phrases_button.bind("<Leave>", on_leave_label)
load_ontology_button.bind("<Enter>", lambda e: on_enter_label(e, "Load OWL file\\files of ontology"))
load_ontology_button.bind("<Leave>", on_leave_label)

global higher_view_concept_window
higher_view_concept_window = Frame(notebook_main, bg="white")

global higher_view_phrase_window
higher_view_phrase_window = Frame(notebook_main, bg="white")

global input_phrases
input_phrases = []
global phrases
global FP_validation
global exist_m_related_concept
global FP_metadata
global FP_metadata_2
global FP_metadata_md
global FP_metadata_refined

global equivalent_concepts_list
equivalent_concepts_list = []

global load_super_sub_phrases_path
load_super_sub_phrases_path = []
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

global notes_phrases
notes_phrases = []
global notes_concepts
notes_concepts = []
phrases = []
FP_validation = []
exist_m_related_concept = []
FP_metadata = [NodeType]
FP_metadata_2 = [NodeType]
FP_metadata_md = []
FP_metadata_refined = []
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
global all_phrases
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

global higher_view_phrases_only_window
higher_view_phrases_only_window = Frame(notebook_main, bg="white")

Frame10_phrase_only = Frame(higher_view_phrases_only_window, bg='white')
Frame1_phrase_only = Frame(Frame10_phrase_only, bg='white')
Frame_temp_phrase_only = Frame(Frame1_phrase_only, bg='white')
Label(Frame_temp_phrase_only, text='     Phrases', bg='white', font='Helvetica 12 bold', fg='navy').pack(side="left")
Frame_temp_phrase_only.pack()
listbox_mark_phrase_only = Listbox(Frame1_phrase_only, width=3)
listbox1_phrase_only = Listbox(Frame1_phrase_only, width=50, exportselection=False)
listbox2_phrase_only = Listbox(Frame1_phrase_only, width=10)
scrollbary_phrase_only = Scrollbar(Frame1_phrase_only, command=yview_main_phrase_only)

listbox1_phrase_only.bind("<MouseWheel>", OnMouseWheel_phrase_only)
listbox2_phrase_only.bind("<MouseWheel>", OnMouseWheel_phrase_only)
listbox1_phrase_only.config(yscrollcommand=scrollbary_phrase_only.set)
listbox2_phrase_only.config(yscrollcommand=scrollbary_phrase_only.set)
listbox_mark_phrase_only.config(yscrollcommand=scrollbary_phrase_only.set)

scrollbary_phrase_only.pack(side="right", fill=Y, expand=False)
listbox_mark_phrase_only.pack(side="left", fill=BOTH, expand=True)
listbox1_phrase_only.pack(side="left", fill=BOTH, expand=True)
listbox2_phrase_only.pack_forget()
Frame1_phrase_only.pack(side="left", fill=Y, padx=1)
Frame10_phrase_only.pack(side="left", fill=Y, padx=5, pady=5)

for item in phrases:
    i = phrases.index(item)
    listbox1_phrase_only.insert(END, item)
    listbox2_phrase_only.insert(END, FP_validation[i])
    listbox_mark_phrase_only.insert(END, " ")

listbox1_phrase_only.bind("<<ListboxSelect>>", click_on_phrase_only)
listbox_mark_phrase_only.bind("<ButtonRelease-1>", lambda event: mark_phrase_only_tab(event))
Frame4_phrase_only = Frame(higher_view_phrases_only_window, bg='white')
Label(Frame4_phrase_only, text='Phrase: ', bg='white', font='Helvetica 10 bold', fg='navy').grid(row=0, column=0,
                                                                                                 sticky='w')
Label(Frame4_phrase_only, text='Label: ', bg='white', font='Helvetica 10 bold', fg='white').grid(row=1, column=0,
                                                                                                 sticky='w')
p1_phrase_only = Label(Frame4_phrase_only, text='', bg='white')
p1_phrase_only.grid(row=0, column=1, sticky='w')
p2_phrase_only = Label(Frame4_phrase_only, text='', bg='white', fg='white')
p2_phrase_only.grid(row=1, column=1, sticky='w')

Frame4_phrase_only.pack(side=TOP, anchor=W, padx=10, pady=10)
global previous_tab_id_phrase_only
previous_tab_id_phrase_only = 0


global notebook_phrases_only
notebook_phrases_only = ttk.Notebook(higher_view_phrases_only_window)
notebook_phrases_only.pack(side=LEFT, fill=BOTH, expand=1)

notebook_phrases_only.bind('<<NotebookTabChanged>>', set_previous_tab_index_phrases_only)

notebook_main.add(higher_view_phrases_only_window, text="PHRASES")

count = 0
for item in phrases:
    FP_validation.append(" ")
    exist_m_related_concept.append(" ")
    x = NodeType(" ", " ", " ", " ", " ", " ")
    Node_list = []
    list_ext_concepts = []
    x_2 = NodeType(Node_list, " ", list_ext_concepts, " ", " ", " ")
    if count == 0:
        FP_metadata[0] = x
        FP_metadata_2[0] = x_2
        count += 1
    else:
        FP_metadata.append(x)
        FP_metadata_2.append(x_2)
        FP_metadata_md.append(" ")
        FP_metadata_refined.append(" ")

save_flag_meta_data = 0
Frame10 = Frame(higher_view_phrase_window, bg='white')

Frame1 = Frame(Frame10, bg='white')
Frame_temp = Frame(Frame1, bg='white')
Label(Frame_temp, text='     Phrases', bg='white', font='Helvetica 12 bold', fg='navy').pack(side="left")
Frame_temp.pack()
listbox_mark = Listbox(Frame1, width=3)
listbox1 = Listbox(Frame1, width=50, exportselection=False)
listbox2 = Listbox(Frame1, width=10)
scrollbary = Scrollbar(Frame1, command=yview_main)
listbox1.bind("<MouseWheel>", OnMouseWheel)
listbox2.bind("<MouseWheel>", OnMouseWheel)
listbox1.config(yscrollcommand=scrollbary.set)
listbox2.config(yscrollcommand=scrollbary.set)
listbox_mark.config(yscrollcommand=scrollbary.set)

scrollbary.pack(side="right", fill=Y, expand=False)
listbox_mark.pack(side="left", fill=BOTH, expand=True)
listbox1.pack(side="left", fill=BOTH, expand=True)
listbox2.pack_forget()
Frame1.pack(side="left", fill=Y, padx=1)
Frame10.pack(side="left", fill=Y, padx=5, pady=5)

for item in phrases:
    i = phrases.index(item)
    listbox1.insert(END, item)
    listbox2.insert(END, FP_validation[i])
    listbox_mark.insert(END, " ")

listbox1.bind("<<ListboxSelect>>", click_on_phrase)
listbox1.bind('<Control-z>', listbox_undo)
listbox_mark.bind("<ButtonRelease-1>", lambda event: mark_phrase(event))

Frame4 = Frame(higher_view_phrase_window, bg='white')
Label(Frame4, text='Phrase: ', bg='white', font='Helvetica 10 bold', fg='navy').grid(row=0, column=0, sticky='w')
Label(Frame4, text='Label: ', bg='white', font='Helvetica 10 bold', fg='white').grid(row=1, column=0, sticky='w')

p1 = Label(Frame4, text='', bg='white')
p1.grid(row=0, column=1, sticky='w')
p2 = Label(Frame4, text='', bg='white', fg='white')

p2.grid(row=1, column=1, sticky='w')
Button2 = Button(Frame4, text="Mark phrase as DONE", width=20, fg='black', bg='paleturquoise', font=('comicsans', 10),
                 command=mark_phrase_done_button).grid(row=0, column=2, sticky='e', padx=50)

Frame4.pack(side=TOP, anchor=W, padx=10, pady=10)
listbox1_menu = Menu(Frame1, tearoff=False)
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
window_phrase_matching_view = Frame(notebook_phrases_only, width=950, height=450, bg="white")
global window_phrase_note_view
window_phrase_note_view = Frame(notebook_phrases, width=950, height=450, bg="white")
global window_phrase_note_view_only
window_phrase_note_view_only = Frame(notebook_phrases_only, width=950, height=450, bg="white")
global window_mdo_info_view_set_up
window_mdo_info_view_set_up = Frame(notebook_set_up, width=900, height=450, bg="white")

global axiom_color_edge
axiom_color_edge = []
global axiom_color
axiom_color = []
global sub_super_p_button_color_yes
sub_super_p_button_color_yes = 'lightBlue1'
global sub_super_p_button_color_no
sub_super_p_button_color_no = 'lightBlue1'
notebook_main.add(higher_view_phrase_window, text="Phrase -> Concept")

global higher_view_concept_only_window
higher_view_concept_only_window = Frame(notebook_main, bg="white")

Frame1_concept_view_only = Frame(higher_view_concept_only_window, bg='white')
Frame_temp_only = Frame(Frame1_concept_view_only, bg='white')
Label(Frame_temp_only, text=' Concept', bg='white', font='Helvetica 12 bold', fg='navy').pack(side="left")
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

scrollbary_only.pack(side="right", fill=Y, expand=False)
listbox_mark_concepts_only.pack(side="left", fill=BOTH, expand=True)
listbox1_concept_names_only.pack(side="left", fill=BOTH, expand=True)
listbox2_concept_origin_only.pack_forget()
listbox1_concept_names_only.bind("<<ListboxSelect>>", click_on_concept_only)
listbox_mark_concepts_only.bind("<ButtonRelease-1>", lambda event: mark_concept_only(event))

Frame1_concept_view_only.pack(side="left", fill=Y, padx=5, pady=5)

Frame20_only = Frame(higher_view_concept_only_window, bg='white')
Label(Frame20_only, text='Concept: ', bg='white', font='Helvetica 10 bold', fg='navy').grid(row=0, column=0, sticky='w')
Label(Frame20_only, text='Origin: ', bg='white', font='Helvetica 10 bold', fg='navy').grid(row=1, column=0, sticky='w')

global concept_name_only
concept_name_only = Label(Frame20_only, text='', bg='white')
concept_name_only.grid(row=0, column=1, sticky='w')
concept_origin_only = Label(Frame20_only, text='', bg='white')
concept_origin_only.grid(row=1, column=1, sticky='w')
Frame20_only.pack(side=TOP, anchor=W, padx=10, pady=10)

global notebook_concepts_only
notebook_concepts_only = ttk.Notebook(higher_view_concept_only_window)
notebook_concepts_only.pack(side=LEFT, fill=BOTH, expand=1)
notebook_main.add(higher_view_concept_only_window, text="CONCEPTS")
global previous_tab_id_concept_only
previous_tab_id_concept_only = 0

notebook_concepts_only.bind('<<NotebookTabChanged>>', set_previous_tab_index_concepts_only)
global window_concept_only
window_concept_only = Frame(notebook_concepts_only, width=950, height=450, bg="white")

global window_concept_only_note_view
window_concept_only_note_view = Frame(notebook_concepts_only, width=950, height=450, bg="white")

Frame1_concept_view = Frame(higher_view_concept_window, bg='white')
Frame_temp = Frame(Frame1_concept_view, bg='white')
Label(Frame_temp, text=' Concept', bg='white', font='Helvetica 12 bold', fg='navy').pack(side="left")
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
listbox_mark_concepts.pack(side="left", fill=BOTH, expand=True)
listbox1_concept_names.pack(side="left", fill=BOTH, expand=True)
listbox2_concept_origin.pack_forget()
listbox1_concept_names.bind("<<ListboxSelect>>", click_on_concept)
listbox_mark_concepts.bind("<ButtonRelease-1>", lambda event: mark_concept(event))
listbox1_concept_names.bind('<Control-z>', listbox_concept_undo)

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
listbox_mark_concepts_menu.add_command(label="Mark as Done", command=mark_concept_done)
listbox_mark_concepts_menu.add_command(label="UnMark as Done", command=unmark_concept_done)

listbox1_concept_names.bind("<Button-3>", my_popup_listbox1_concept_view)
listbox1_concept_names.bind('<FocusOut>', lambda e: clear_seached_concepts())
notebook_main.add(higher_view_concept_window, text="Concept -> Axiom")

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
root.bind('<Control-f>', find_window)
toolTip = ToolTip(root)

root.mainloop()