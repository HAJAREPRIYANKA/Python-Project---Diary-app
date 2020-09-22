from tkinter import *
import tkinter.ttk as ttk
import sqlite3
import datetime
from tkinter import messagebox

m_w = Tk()
m_w.geometry("620x430")
m_w.resizable(height=FALSE, width=FALSE)
m_w.title("")


# db creation
conn = sqlite3.connect('diary_data.db')

# cursor creation
c = conn.cursor()


#to create table

def create_table():
    c.execute(""" CREATE TABLE data(
            TITLE text,
            NOTE text,
            c_date text
            )""")

try:
    create_table()
except sqlite3.OperationalError:
    pass



# to save data in table
def submit_clear():
    global date_e, title_entry, text_ent, t_ent, txt_ent, d_ent
    con = sqlite3.connect('diary_data.db')
    c = con.cursor()

    # validation
    if len(title_entry.get()) == 0:
        messagebox.showerror("error", "Empty title Field !")
        return False
    if len(date_e.get()) == 0:
        messagebox.showerror("error", "Empty date Field !")
        return False
    '''
    if len(text_ent.get('0.1',END)) == 0:
        messagebox.showerror("error", "Empty text Field !")
        return False
    '''
    title_sub = title_entry.get()
    print(title_sub)
    text_sub = text_ent.get("1.0", END)
    print(text_sub)
    c_d = date_e.get()
    print(type(c_d))
    # to insert data

    c.execute("""INSERT INTO data VALUES(?,?,?)
    """, (title_sub, text_sub, c_d))
    con.commit()
    con.close()
    messagebox.showinfo("SUCCESS", "Succesfully Saved !")

    # to clear
    title_entry.delete(0, END)
    text_ent.delete('1.0', END)
    date_e.delete(0, END)

# to show notelist
def show():
    global v_ent
    show_win = Toplevel()
    show_win.resizable(height=FALSE, width=FALSE)
    show_win.configure(bg="pink")

    con = sqlite3.connect('diary_data.db')
    c = con.cursor()
    # query the database
    c.execute("SELECT rowid,* FROM data")
    records = c.fetchall()
    lst = list(records)
    total_rows = len(lst)
    try:
        global total_columns
        total_columns = len(lst[0])
    except IndexError:
        messagebox.showerror("error", "Empty Records !")

    lbl = Label(show_win, text="Id", padx=113)
    lbl.grid(row=0, column=0, pady=2)
    lbl = Label(show_win, text="Note title", padx=95)
    lbl.grid(row=0, column=1)
    lbl = Label(show_win, text="Date & Time", padx=85)
    lbl.grid(row=0, column=3)
    lbl = Label(show_win, text="To view", padx=45)
    lbl.grid(row=0, column=4)
    lbl = Label(show_win, text="To delete ", padx=40)
    lbl.grid(row=5, column=4)

    #for table creation of note list

    for i in range(total_rows):
        for j in range(total_columns):
            if j == (len(lst[0]) - 2):
                continue
            e = Entry(show_win, fg='blue',width=40)
            e.grid(row=i + 1, column=j,pady=1)
            e.insert(END, str(lst[i][j]))
    v_lbl = Label(show_win, text='Enter ID :',padx=40)
    v_lbl.grid(row=1, column=len(lst[0]), padx=10, pady=2)
    v_ent = Entry(show_win)
    v_ent.grid(row=2, column=len(lst[0]), padx=10, pady=2)
    v_btn = Button(show_win, text="view", padx=20,bg="skyblue", command=open_note)
    v_btn.grid(row=3, column=len(lst[0]), padx=10, pady=2)

    global dl_ent
    d_lbl = Label(show_win, text='Enter ID :',padx=42)
    d_lbl.grid(row=6, column=len(lst[0]), padx=10, pady=2)
    dl_ent = Entry(show_win)
    dl_ent.grid(row=7, column=len(lst[0]), padx=10, pady=2)
    dl_btn = Button(show_win, text="delete", padx=20,bg="skyblue",command=del_btn)
    dl_btn.grid(row=8, column=len(lst[0]), padx=10, pady=2)
    con.commit()
    con.close()


#function for delete button
def del_btn():
    global dl_ent
    con = sqlite3.connect('diary_data.db')
    c = con.cursor()

    IDS = dl_ent.get()

    c.execute("SELECT rowid,* FROM data")
    row_ids = c.fetchall()
    list_id = list(row_ids)
    available_RID = []
    for records in list_id:
        available_RID.append(records[0])
    if len(IDS) == 0:
       return 0
    if int(IDS) in available_RID:
        c.execute("DELETE from data WHERE rowid = (?)", (IDS,))
        messagebox.showinfo("SUCCESS", "Successfully Deleted")
    else:
       messagebox.showerror("error", "No Such Row Id Exists...")
    dl_ent.delete(0, END)


    con.commit()
    con.close()

# to display note

def open_note():
    global v_ent
    display = Tk()
    display.geometry("620x430")
    display.resizable(height=FALSE, width=FALSE)
    display.configure(bg="pink")



    global d_e,w_e,t_e,e

    id_lbl = Label(display,text="ID :",bg="pink",fg="black")
    id_lbl.place(x=565,y=10)
    e = Entry(display)
    e.place(x=590,y=10,height=20,width=20)

    d_e =Entry(display,bg="white",fg="blue",font="1")
    d_e.place(x=4,y=35,height=30,width=610)

    t_e = Entry(display,bg="white",fg="black",font="bold")
    t_e.place(x=4,y=75,height=30,width=610)

    Scrl = Scrollbar(display)
    Scrl.place(x=598, y=120, height=270)

    w_e =Text(display,fg="black",yscrollcommand=Scrl.set)
    Scrl.config(command=w_e.yview)
    w_e.place(x=4,y=120,width=597,height=270)


    # db
    conn = sqlite3.connect('diary_data.db')
    c = conn.cursor()
    # Retriving data from lst_data
    c.execute('SELECT rowid,* FROM data')
    diary_data = c.fetchall()

    IDS = v_ent.get()

    c.execute("SELECT rowid,* FROM data")
    row_ids = c.fetchall()
    list_id = list(row_ids)
    available_RID = []
    for records in list_id:
        available_RID.append(records[0])
    if len(IDS) == 0:
        return 0
    if int(IDS) in available_RID:
        # viewing selected id
        selected_id = int(IDS)
        for info in diary_data:
            if info[0] == selected_id:
                e.insert(0, info[0])
                d_e.insert(0, str(info[3]))
                t_e.insert(0, info[1])
                w_e.insert(END, info[2])
    else:
        messagebox.showerror("error", "No Such Row Id Exists...")
        v_ent.delete(0, END)
    ch_btn = Button(display,text="close This window",bg="skyblue",fg="black",command=display.destroy)
    ch_btn.place(x=300,y=395)

    ch_btn = Button(display, text="save changes ", bg="skyblue",fg="black",command=change)
    ch_btn.place(x=200, y=395)

    conn.commit()
    conn.close()
    display.mainloop()

def change():
    global d_e,w_e,t_e,v_ent,e

    # validation
    if len(e.get()) == 0:
        messagebox.showerror("error", "Empty date Field !")
        return False
    if len(t_e.get()) == 0:
        messagebox.showerror("error", "Empty title Field !")
        return False
    if len(d_e.get()) == 0:
        messagebox.showerror("error", "Empty date Field !")
        return False

    if len(w_e.get('0.1',END)) == 0:
        messagebox.showerror("error", "Empty text Field !")
        return False
    '''
    if len((t_e.get()and w_e.get()and t_e.get() and e.get())) == 0:
        messagebox.showerror("error", "All fields are empty !Please fill all the fields !")
        return False
    '''
    # db
    conn = sqlite3.connect('diary_data.db')
    c = conn.cursor()

    rid = v_ent.get()

    up_qry = """UPDATE data SET
                        TITLE = ?,
                        NOTE =  ?,
                        c_date =  ?
                        WHERE rowid =  ?"""
    up_columns = (t_e.get(), w_e.get('0.1', END), d_e.get(), rid)
    try:
        c.execute(up_qry, up_columns)
    except:
        pass
    conn.commit()
    conn.close()
    messagebox.showinfo("SUCCESS", "Succesfully Saved !")


# window to create new note
def new():
    global date_e, title_entry, text_ent, t_ent, txt_ent, d_ent
    f2 = Frame(bg="grey")
    f2.place(x=0, y=0, width=620, height=80)
    f3 = Frame(bg="pink")
    f3.place(x=0, y=80, width=620, height=350)

    def sv_btn(e):
        b1['bg'] = "skyblue"
        b1['fg'] = "black"
    def sv_l_btn(e):
        b1['bg'] = "white"
        b1["fg"] = "black"

    b1 = Button(f2, text="back", command=home,fg="black",bg="white")
    b1.place(x=10, y=4)
    b1.bind('<Enter>',sv_btn)
    b1.bind('<Leave>',sv_l_btn)

    d_ent = DoubleVar()
    date_e = Entry(f2, width=30, textvariable=d_ent)
    date_e.place(x=450, y=4, height=20, width=160)

    title_lbl = Label(f2, text="Title : ", bg="grey", fg="white", font="Helvetica,20")
    title_lbl.place(x=10, y=35)

    t_ent = StringVar()
    title_entry = Entry(f2, width=60, font="10", textvariable=t_ent)
    title_entry.place(x=70, y=38, height=30)

    lbl = Label(f3, text="Write text :", font="10,Helvetica ", bg="pink")
    lbl.place(x=5, y=5)

    # txt_ent = StringVar()
    #vertical scroll
    Scrl = Scrollbar(f3)
    Scrl.place(x=597, y=35, height=270)
    #horizontal scroll
    #Scrl_h = Scrollbar(f3,orient=HORIZONTAL)
    #Scrl_h.place(x=5, y=300,width=600)

    text_ent = Text(f3, font="1",yscrollcommand=Scrl.set)
    Scrl.config(command=text_ent.yview)
    #Scrl_h.config(command=text_ent.xview)
    text_ent.place(x=5, y=35, width=592,height=270)

    def sv_btn(e):
        save['bg'] = "skyblue"
        save['fg'] = "black"
    def sv_l_btn(e):
        save['bg'] = "grey"
        save['fg'] = "white"

    save = Button(f3, text="SAVE", bg="grey",fg="white",command=submit_clear)
    save.place(x=280, y=315, width=60)
    save.bind('<Enter>',sv_btn)
    save.bind('<Leave>',sv_l_btn)


    # for date creation
    cd = datetime.datetime.now()
    #res = cd.strftime("%x")
    # title_entry.set(res)
    d_ent.set(cd)


def home():
    #for hower effect
    def onbtn(e):
        b1['bg'] = "skyblue"
    def leavebtn(e):
        b1['bg'] = "white"
        b1['fg'] = "black"

    def onbtn1(e):
        b2['bg'] = "skyblue"
    def leavebtn1(e):
        b2['bg'] = "white"

    def onbtn2(e):
        b3['bg'] = "Grey"
        b3['fg'] = "white"
    def leavebtn2(e):
        b3['bg'] = "white"
        b3['fg'] = "black"
    f1 = Frame(m_w, bg="grey")
    f1.place(x=0, y=0, width=620, height=80)

    f3 = Frame(m_w, bg="pink")
    f3.place(x=0, y=80, width=620, height=270)

    lb = Label(f1, text="Welcome to E-diary", font="Helvetica 20 ", pady=5, padx=206)
    lb.place(x=0, y=15)

    b1 = Button(f3, text="NEW NOTE", font="Helvetica", padx=30, command=new,bg="white")
    b1.place(x=230, y=40)
    b1.bind('<Enter>',onbtn)
    b1.bind('<Leave>',leavebtn)

    b2 = Button(f3, text="SHOW NOTES", font="Helvetica", padx=20, command=show)
    b2.place(x=230, y=120)
    b2.bind('<Enter>', onbtn1)
    b2.bind('<Leave>', leavebtn1)

    b3 = Button(f3, text="EXIT", font="Helvetica", padx=60, command=m_w.destroy,bg="white")
    b3.place(x=230, y=200)
    b3.bind('<Enter>', onbtn2)
    b3.bind('<Leave>', leavebtn2)

    f2 = Frame(m_w, bg="grey", borderwidth=6)
    f2.place(x=0, y=350, width=620, height=80)


home()

conn.commit()
conn.close()

m_w.mainloop()
