from customtkinter import *
import PIL.Image
import zipfile
import itertools
import threading
import pyperclip
import random
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
import hashlib

# database
username_list = ["hero", "bubo", "goni", "rock", "pipe", "wexp"]
password_list = ['3726', '1234', '1234', '1234', '1234', '1234']


# Defining employee database
def empdb():
    # function to define database
    def Database():
        global conn, cursor
        # creating student database
        conn = sqlite3.connect("student.db")
        cursor = conn.cursor()
        # creating STUD_REGISTRATION table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS STUD_REGISTRATION (STU_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "STU_NAME TEXT, STU_CONTACT TEXT, STU_EMAIL TEXT, STU_ROLLNO TEXT, STU_BRANCH TEXT)")

    # defining function for creating GUI Layout
    def DisplayForm():
        # creating window
        display_screen = CTkToplevel(top)
        # setting width and height for window
        display_screen.geometry("900x400")
        # setting title for window
        display_screen.title("Employee Management System")
        global tree
        global SEARCH
        global name, contact, email, rollno, branch
        SEARCH = StringVar()
        name = StringVar()
        contact = StringVar()
        email = StringVar()
        rollno = StringVar()
        branch = StringVar()
        # creating frames for layout
        # topview frame for heading
        TopViewForm = Frame(display_screen, width=600, bd=1, relief=SOLID)
        TopViewForm.pack(side=TOP, fill=X)
        # first left frame for registration from
        LFrom = Frame(display_screen, width="350", bg="#1a1716")
        LFrom.pack(side=LEFT, fill=Y)
        # second left frame for search form
        LeftViewForm = Frame(display_screen, width=500, bg="gray")
        LeftViewForm.pack(side=LEFT, fill=Y)
        # mid-frame for displaying students record
        MidViewForm = Frame(display_screen, width=600)
        MidViewForm.pack(side=RIGHT)
        # label for heading
        lbl_text = Label(TopViewForm, text="Employee Management System", font=('verdana', 18), width=600, bg="black",
                         fg="white")
        lbl_text.pack(fill=X)
        # creating registration form in first left frame
        Label(LFrom, text="Name  ", font=("Kozuka Mincho Pr6N B", 12), bg="#1a1716", fg="white").pack(side=TOP, pady=10)
        Entry(LFrom, font=("Kozuka Mincho Pr6N B", 10, "bold"), textvariable=name).pack(side=TOP, padx=10, fill=X)
        Label(LFrom, text="Contact ", font=("Kozuka Mincho Pr6N B", 12), bg="#1a1716", fg="white").pack(side=TOP,
                                                                                                        pady=10)
        Entry(LFrom, font=("Kozuka Mincho Pr6N B", 10, "bold"), textvariable=contact).pack(side=TOP, padx=10, fill=X)
        Label(LFrom, text="Email ", font=("Kozuka Mincho Pr6N B", 12), bg="#1a1716", fg="white").pack(side=TOP, pady=10)
        Entry(LFrom, font=("Kozuka Mincho Pr6N B", 10, "bold"), textvariable=email).pack(side=TOP, padx=10, fill=X)
        Label(LFrom, text="Rollno ", font=("Kozuka Mincho Pr6N B", 12), bg="#1a1716", fg="white").pack(side=TOP,
                                                                                                       pady=10)
        Entry(LFrom, font=("Kozuka Mincho Pr6N B", 10, "bold"), textvariable=rollno).pack(side=TOP, padx=10, fill=X)
        Label(LFrom, text="Branch ", font=("Kozuka Mincho Pr6N B", 12), bg="#1a1716", fg="white").pack(side=TOP,
                                                                                                       pady=10)
        Entry(LFrom, font=("Kozuka Mincho Pr6N B", 10, "bold"), textvariable=branch).pack(side=TOP, padx=10, fill=X)
        Button(LFrom, text="Submit", font=("Kozuka Mincho Pr6N B", 10, "bold"), command=register).pack(side=TOP,
                                                                                                       padx=10, pady=15,
                                                                                                       fill=X)
        # creating delete button
        btn_delete = Button(LFrom, text="Delete", font=("Arial", 10, "bold"), command=Delete)
        btn_delete.pack(side=TOP, padx=10, pady=20, fill=X)

        # creating search label and entry in second frame
        lbl_txtsearch = Label(LeftViewForm, text="Search for Name", font=('verdana', 15), bg="gray")
        lbl_txtsearch.pack(pady=10)
        # creating search entry
        search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
        search.pack(side=TOP, padx=10, fill=X)
        # creating search button
        btn_search = Button(LeftViewForm, text="Search", command=SearchRecord)
        btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
        # creating view button
        btn_view = Button(LeftViewForm, text="View All", command=DisplayData)
        btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
        # creating reset button
        btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
        btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
        # setting scrollbar
        scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
        scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
        styletree = ttk.Style()
        styletree.configure("Treeview", background='#1a1716', foreground='white', fieldbackground='#1a1716')
        styletree.map('Treeview',background=[('selected', '#3d3d3d')])

        tree = ttk.Treeview(MidViewForm, columns=("Student Id", "Name", "Contact", "Email", "Rollno", "Branch"),
                            selectmode="extended", height=100, yscrollcommand=scrollbary.set,
                            xscrollcommand=scrollbarx.set)
        styletree.theme_use('alt')
        scrollbary.config(command=tree.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        scrollbarx.config(command=tree.xview)
        scrollbarx.pack(side=BOTTOM, fill=X)
        # setting headings for the columns
        tree.heading('Student Id', text="Employee Id", anchor=W)
        tree.heading('Name', text="Name", anchor=W)
        tree.heading('Contact', text="Contact", anchor=W)
        tree.heading('Email', text="Email", anchor=W)
        tree.heading('Rollno', text="Rollno", anchor=W)
        tree.heading('Branch', text="Branch", anchor=W)
        # setting width of the columns
        tree.column('#0', stretch=NO, minwidth=0, width=0)
        tree.column('#1', stretch=NO, minwidth=0, width=100)
        tree.column('#2', stretch=NO, minwidth=0, width=150)
        tree.column('#3', stretch=NO, minwidth=0, width=80)
        tree.column('#4', stretch=NO, minwidth=0, width=120)
        tree.pack()
        DisplayData()

    # function to insert data into database
    def register():
        Database()
        # getting form data
        name1 = name.get()
        con1 = contact.get()
        email1 = email.get()
        rol1 = rollno.get()
        branch1 = branch.get()
        # applying empty validation
        if name1 == '' or con1 == '' or email1 == '' or rol1 == '' or branch1 == '':
            tkMessageBox.showinfo("Warning", "Please fill the empty field!")
        else:
            # execute query
            conn.execute('INSERT INTO STUD_REGISTRATION (STU_NAME,STU_CONTACT,STU_EMAIL,STU_ROLLNO,STU_BRANCH) \
                  VALUES (?,?,?,?,?)', (name1, con1, email1, rol1, branch1));
            conn.commit()
            tkMessageBox.showinfo("Message", "Stored successfully")
            # refresh table data
            DisplayData()
            conn.close()

    def Reset():
        # clear current data from table
        tree.delete(*tree.get_children())
        # refresh table data
        DisplayData()
        # clear search text
        SEARCH.set("")
        name.set("")
        contact.set("")
        email.set("")
        rollno.set("")
        branch.set("")

    def Delete():
        # open database
        Database()
        if not tree.selection():
            tkMessageBox.showwarning("Warning", "Select data to delete")
        else:
            result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                              icon="warning")
            if result == 'yes':
                curItem = tree.focus()
                contents = (tree.item(curItem))
                selecteditem = contents['values']
                tree.delete(curItem)
                cursor = conn.execute("DELETE FROM STUD_REGISTRATION WHERE STU_ID = %d" % selecteditem[0])
                conn.commit()
                cursor.close()
                conn.close()

    # function to search data
    def SearchRecord():
        # open database
        Database()
        # checking search text is empty or not
        if SEARCH.get() != "":
            # clearing current display data
            tree.delete(*tree.get_children())
            # select query with where clause
            cursor = conn.execute("SELECT * FROM STUD_REGISTRATION WHERE STU_NAME LIKE ?",
                                  ('%' + str(SEARCH.get()) + '%',))
            # fetch all matching records
            fetch = cursor.fetchall()
            # loop for displaying all records into GUI
            for data in fetch:
                tree.insert('', 'end', values=(data))
            cursor.close()
            conn.close()

    # defining function to access data from SQLite database
    def DisplayData():
        # open database
        Database()
        # clear current data
        tree.delete(*tree.get_children())
        # select query
        cursor = conn.execute("SELECT * FROM STUD_REGISTRATION")
        # fetch all data from database
        fetch = cursor.fetchall()
        # loop for displaying all data in GUI
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

    DisplayForm()


# Defining generator window
def open_generator():
    root = CTkToplevel(top)
    root.geometry("700x500")
    root.title("Generator")
    passwrd = StringVar()
    passlen = IntVar()
    passlen.set(0)

    def generate():  # Function to generate the password
        pass1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                 'Y', 'Z', '1', '2', '3', '4', '5', '6', '7', '8',
                 '9', '0', ' ', '!', '@', '#', '$', '%', '^', '&',
                 '*', '(', ')']
        password = ""
        for x in range(passlen.get()):
            password = password + random.choice(pass1)
        passwrd.set(password)

    # function to copy the passcode

    def copyclipboard():
        random_password = passwrd.get()
        pyperclip.copy(random_password)

    # Labels

    qwerty = CTkLabel(root, text="Password Generator")
    qwerty.configure(font=('Kozuka Mincho Pr6N B', 60))
    qwerty.pack(pady=10)
    qwert = CTkLabel(root, text="Enter how many character you want your password to be")
    qwert.configure(font=('Kozuka Mincho Pr6N B', 20))
    qwert.pack(pady=10)
    CTkEntry(root, textvariable=passlen).pack(pady=10)
    CTkButton(root, text="Generate ", command=generate).pack(pady=7)
    CTkEntry(root, textvariable=passwrd).pack(pady=10)
    CTkButton(root, text="Tap to copy clipboard", command=copyclipboard).pack(pady=10)
    root.mainloop()


# Defining cracker window
def open_cracker():
    cr = CTkToplevel(top)
    cr.title("Password Cracker")
    cr.resizable(0, 0)
    cr.iconbitmap('favicon.ico')

    def extractFile(zip_file, password):
        try:
            zip_file.extractall(pwd=password)
            return True
        except KeyboardInterrupt:
            exit(0)
        except Exception:
            pass

    def creaker(zipname, n, first_half, last_half, uPPER, lOWER, nUM, sYM):
        # Function for extracting zip files
        n = int(n)
        # Main code starts here...
        count = 0
        # All char to try
        lowerAlp = 'abcdefghijklmnopqrstuvwxyz'
        upperAlp = lowerAlp.upper()
        numBer = '0123456789'
        specSymbol = '!@#$%^&*()'
        pool = ''
        zipfilename = zipname + '.zip'
        if lOWER == 1:
            pool += lowerAlp
        if uPPER == 1:
            pool += upperAlp
        if nUM == 1:
            pool += numBer
        if sYM == 1:
            pool += specSymbol
        zip_file = zipfile.ZipFile(zipfilename)
        # n = int(input('How many characters do you want to try?\n'))
        myLabel.configure(text='Starting...')
        for c in itertools.product(pool, repeat=n):
            # Joining first and last to pw
            password = first_half + ''.join(c) + last_half
            # Try to extract the file.Starting...
            count += 1
            if count % 10000 == 0:
                myLabel.configure(text=f"Tested({count}): %s" % password)
            # For printing the current"Try %s" % password
            if extractFile(zip_file, str.encode(password)):
                myLabel.configure(text='Pwrd found: %s' % password)
                exit(0)
        # If no password was found
        myLabel.configure(text='Pwrd not found')

    cap = IntVar()
    low = IntVar()
    num = IntVar()
    sym = IntVar()

    CTkLabel(master=cr, text="Please enter the Zip file name (everything before .zip)",
             justify=LEFT, anchor="w").grid(row=0, column=0, pady=10, padx=10, sticky=W)
    zFileName = CTkEntry(master=cr)
    zFileName.grid(row=0, column=1, padx=10)
    CTkLabel(master=cr, text="Please enter the total char you want to try", justify=LEFT, anchor="w") \
        .grid(row=1, column=0, pady=10, padx=10, sticky=W)
    numchar = CTkEntry(master=cr)
    numchar.grid(row=1, column=1, padx=10)
    CTkLabel(master=cr, text="If you would like to add anything before the combination enter it here:",
             justify=LEFT, anchor="w").grid(row=2, column=0, pady=10, padx=10, sticky=W)
    befo = CTkEntry(master=cr)
    befo.grid(row=2, column=1, padx=10)
    CTkLabel(master=cr, text="If you would like to add anything after the combination enter it here:",
             justify=LEFT, anchor="w").grid(row=3, column=0, pady=10, padx=10, sticky=W)
    afte = CTkEntry(master=cr)
    afte.grid(row=3, column=1, padx=10)
    CTkLabel(master=cr, text="Please check the following box if you'd like any of them added to the character pool",
             justify=LEFT, anchor="w").grid(row=4, pady=10, padx=10, columnspan=2, sticky=W)
    CTkLabel(master=cr, text='').grid(row=5)
    CTkLabel(master=cr, text='').grid(row=6)
    CTkCheckBox(master=cr, text="Capital Letter", variable=cap).place(x=10, y=250)
    CTkCheckBox(master=cr, text="Lowercase Letter", variable=low).place(x=160, y=250)
    CTkCheckBox(master=cr, text="Number", variable=num).place(x=310, y=250)
    CTkCheckBox(master=cr, text="Symbol", variable=sym).place(x=460, y=250)
    login_button = CTkButton(master=cr, text="Enter", command=lambda: threading.Thread(target=creaker, args=(
        zFileName.get(), numchar.get(), befo.get(), afte.get(),
        cap.get(), low.get(), num.get(), sym.get())).start())

    login_button.grid(row=7, pady=10)
    myLabel = CTkLabel(master=cr, text="")
    myLabel.place(x=380, y=310)


# defining the popup LOGIN window
def open_popup():
    root = CTkToplevel(top)
    root.title("The App")
    root.geometry('250x275')
    root.resizable(0, 0)

    # Behaviours - Methods
    def close_app():
        top.destroy()

    def bypass():
        top.deiconify()
        root.destroy()

    def inibutton():
        welcome_page.pack_forget()
        login_check_screen.pack()

    def check_credentials(name, pw):
        # check if the entered credentials match the correct ones
        name = name.strip().lower()
        pwd = hashlib.md5(pw.encode('utf-8')).hexdigest()
        # open database
        conn = sqlite3.connect('login.db')
        # select query
        cursor = conn.execute('SELECT * from ADMIN where USERNAME="%s" and PASSWORD="%s"' % (name, pwd))
        if cursor.fetchone():
            top.deiconify()
            root.destroy()
        else:
            myLabel.configure(text="Invalid credentials. Try again.")

    # making frames
    welcome_page = CTkFrame(master=root)
    login_check_screen = CTkFrame(master=root)
    # bypass log in here
    initiateBTN = CTkButton(master=welcome_page, text="Initiate", command=bypass)

    # --------------------Welcome Page----------------------
    root.protocol('WM_DELETE_WINDOW', close_app)
    welcomeTle = CTkLabel(master=welcome_page, text="The APP")
    welcomeTle.pack(pady=(20, 10))
    welcomeTle.configure(font=('Kozuka Mincho Pr6N B', 27))
    CTkLabel(master=welcome_page, text="Hello! Welcome!").pack()
    initiateBTN.pack(padx=62, pady=(10, 150))
    welcome_page.pack()

    # --------------------Login Page----------------------
    # entry widgets for username and password
    superrandomspacing = CTkLabel(master=login_check_screen, text="")
    superrandomspacing.pack()
    login_check_screen_uname = CTkLabel(master=login_check_screen, text="Please enter your Username")
    login_check_screen_uname.pack()
    username_entry = CTkEntry(master=login_check_screen)
    username_entry.pack(padx=60, pady=10)

    login_check_screen_pw = CTkLabel(master=login_check_screen, text="Please enter your Password")
    login_check_screen_pw.pack()
    password_entry = CTkEntry(master=login_check_screen)
    password_entry.pack(padx=10, pady=10)

    # login buttons
    login_button = CTkButton(master=login_check_screen,
                             text="Enter",
                             command=lambda: check_credentials(username_entry.get(), password_entry.get())
                             )
    login_button.pack(padx=10, pady=10)
    myLabel = CTkLabel(master=login_check_screen, text="")
    myLabel.pack(padx=10, pady=10)


# theme
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

# ######------MAIN APP STARTS HERE------###### #
top = CTk()
top.geometry("900x500")
top.title("The APP")
top.resizable(0, 0)

top.iconbitmap('favicon.ico')


def default_home():
    top.withdraw()
    open_popup()
    f2 = CTkFrame(master=top, width=900, height=500)
    f2.place(x=0, y=45)
    l2 = CTkLabel(f2, text='The APP')
    l2.configure(font=('Kozuka Mincho Pr6N B', 90))
    l2.place(x=260, y=150)


# ---Frames
def home():
    f1.destroy()
    f2 = CTkFrame(master=top, width=900, height=500)
    f2.place(x=0, y=45)
    l2 = CTkLabel(f2, text='The APP')
    l2.configure(font=('Kozuka Mincho Pr6N B', 90))
    l2.place(x=260, y=150)
    toggle_win()


def Pw_Cracker():
    f1.destroy()
    f2 = CTkFrame(master=top, width=900, height=500, )
    f2.place(x=0, y=45)
    l2 = CTkLabel(f2, text='Pw_Cracker', )
    l2.configure(font=('Kozuka Mincho Pr6N B', 90))
    l2.place(x=210, y=150)
    toggle_win()
    open_cracker()


def Pw_Generator():
    f1.destroy()
    f2 = CTkFrame(master=top, width=900, height=500)
    f2.place(x=0, y=45)
    l2 = CTkLabel(f2, text='Pw_Generator')
    l2.configure(font=('Kozuka Mincho Pr6N B', 90))
    l2.place(x=210, y=150)
    toggle_win()
    open_generator()


def Database():
    f1.destroy()
    f2 = CTkFrame(master=top, width=900, height=500)
    f2.place(x=0, y=45)
    l2 = CTkLabel(f2, text='Database')
    l2.configure(font=('Kozuka Mincho Pr6N B', 90))
    l2.place(x=210, y=150)
    toggle_win()
    empdb()


def apple():
    f1.destroy()
    f2 = CTkFrame(master=top, width=900, height=500)
    f2.place(x=0, y=45)
    l2 = CTkLabel(f2, text='Comming Soon')
    l2.configure(font=('Kozuka Mincho Pr6N B', 90))
    l2.place(x=210, y=150)
    toggle_win()


def acer():
    f1.destroy()
    f2 = CTkFrame(master=top, width=900, height=500)
    f2.place(x=0, y=45)
    l2 = CTkLabel(f2, text='Coming Soon')
    l2.configure(font=('Kozuka Mincho Pr6N B', 90))
    l2.place(x=210, y=150)
    toggle_win()


def toggle_win():
    global f1
    f1 = CTkFrame(master=top, width=200, height=500, fg_color='#333333')
    f1.place(x=0, y=0)

    # buttons
    def bttn(x, y, text, bcolor, fcolor, cmd):
        def on_entera(e):
            myButton1['background'] = bcolor  # ffcc66
            myButton1['foreground'] = '#ffbbee'  # 000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground'] = '#ffbbee'

        myButton1 = CTkButton(master=f1, text=text, width=42, height=10, command=cmd)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    bttn(10, 80, 'H O M E ', '#0f9d9a', '#12c4c0', home)
    bttn(10, 191, 'C R A C K E R ', '#0f9d9a', '#12c4c0', Pw_Cracker)
    bttn(10, 154, 'G E N E R A T O R ', '#0f9d9a', '#12c4c0', Pw_Generator)
    bttn(10, 117, 'D A T A B A S E ', '#0f9d9a', '#12c4c0', Database)
    bttn(10, 228, 'A P P L E ', '#0f9d9a', '#12c4c0', apple)
    bttn(10, 265, 'A C E R ', '#0f9d9a', '#12c4c0', acer)

    def dele():
        f1.destroy()
        b2 = CTkButton(master=top, text='Open Menu', image=img1, command=toggle_win)
        b2.place(x=10, y=8)

    global img2
    img2 = CTkImage(PIL.Image.open("close.png"))

    CTkButton(master=f1, text='Close Menu', image=img2, command=dele).place(x=10, y=8)


default_home()

img1 = CTkImage(PIL.Image.open("open.png"))
global b2
b2 = CTkButton(master=top, text='Open Menu', image=img1, command=toggle_win)
b2.place(x=10, y=8)
top.mainloop()
