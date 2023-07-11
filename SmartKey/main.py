import baseManager as bm
import tkinter as tk
from tkinter import ttk
import time as t
import os

user_dict = {}

def ding_dong():
  
    status_txt.set("Zvono aktivirano. Molimo, pričekajte.")

    user_clear()

def admin_st_clear():

    cls_list = [list_box, id_num_lbl, id_num_ent, ime_lbl, ime_ent, 
                prezime_lbl, prezime_ent, pins_lbl, pins_ent, active_btn,
                save_btn, del_btn, del_all_btn, add_btn, exit_btn]

    for i in cls_list:
        i.grid_remove()


def admin_clear():
    
    cls_list = [yes_btn, no_btn, sub_btn, pin_ent, pin_lbl, status_dp, pozvoni_btn, unlock_btn]

    for i in cls_list:
        i.grid_forget()

    id_num_var.set("")
    ime_var.set("")
    prezime_var.set("")
    pin_var.set("")
    status_txt.set("")


def half_clear():

     cls_list = [yes_btn, no_btn, sub_btn, pin_ent, pin_lbl]

     for i in cls_list:
        i.grid_remove()


def user_clear():

    cls_list = [sub_btn, pin_ent, pin_lbl]

    for i in cls_list:
        i.grid_remove()


def save_cmd():

    bm.update_user(user_id=id_num_var.get(), 
                    ime=ime_var.get(), 
                    prezime=prezime_var.get(), 
                    pin=pin_var.get(),
                    aktivan=active_var.get()
                    )
    
    refresh_lb()

    status_txt.set("Podaci uspješno spremljeni.")

def del_cmd():

    if id_num_var.get() != 0:
        
        bm.delete_user(user_id=id_num_var.get()),
        list_box.delete(first=list_box.curselection(),
                        last=list_box.curselection()
                        )
        
        status_txt.set("Korisnik uspješno izbrisan.")

        refresh_lb()

    else:

        status_txt.set("Ne možete obrisati admina.")


def del_all_cmd():

    bm.delete_db()
    bm.create_admin()

    refresh_lb()

    status_txt.set("Svi podaci izbrisani.")


def add_cmd():

    bm.add_user(id_num=id_num_var.get(), 
                ime=ime_var.get(), 
                prezime=prezime_var.get(),
                pin=pin_var.get(),
                aktivan=active_var.get()
                )

    if bm.complete_check == 1:
        status_txt.set("Korisnik već postoji.")
    
    elif bm.complete_check == 0:
        status_txt.set("Novi korisnik dodan.")
    
    else:
        status_txt.set("Krivi unos.")

    refresh_lb()


def exit_cmd():
    
    refresh_lb()

    admin_st_clear() 
    pozvoni_btn.grid(column=1, row=2) 
    unlock_btn.grid(column=3, row=2) 
    status_dp.grid(column= 1,row=4, ipadx=90, sticky="s")
    status_txt.set("")
    

def item_selected(event):
   
    selected = list_box.get(list_box.curselection())
    
    with bm.get_db() as session:

        korisnik = session.query(bm.Korisnik).filter(bm.Korisnik.ime == selected[0], bm.Korisnik.prezime == selected[1]).one_or_none()

        id_num_var.set(korisnik.id_num)
        ime_var.set(korisnik.ime)
        prezime_var.set(korisnik.prezime)
        pin_var.set(korisnik.pin)
        active_var.set(korisnik.aktivan)
    
    refresh_lb()

    status_txt.set("")


def refresh_lb():
    global user_dict
    
    user_dict = {}

    get_users()
        

def admin_settings():

    global list_box, id_num_lbl, id_num_ent, ime_lbl, ime_ent, prezime_lbl, prezime_ent, pins_lbl, pins_ent, active_btn, save_btn, del_btn, del_all_btn, add_btn, exit_btn

    admin_clear()

    get_users()

    list_box = tk.Listbox(
            root,
            listvariable=user_dict_var,
            background="LightBlue",
            font=("Segoe UI bold", 15),
            width=25,
            height=18,
            selectmode="SINGLE",
            yscrollcommand=True,
            selectbackground="SkyBlue4",
            selectforeground="white",
            relief="groove"
            )
    
    list_box.bind('<<ListboxSelect>>', item_selected)
            
    list_box.grid(
            column=0,
            row=1,
            columnspan=2,
            rowspan=5
            )
    
    id_num_lbl = tk.Label(
        root,
        text="Identifikacijski broj",
        font=("Segoe UI bold", 16), 
        justify="right"
        )

    id_num_lbl.grid(
        column=2, 
        row=2,
        sticky="ne"
        )

    id_num_ent = tk.Entry(
        root, 
        textvariable=id_num_var, 
        font=("Segoe UI", 16), 
        border=1,
        background="lightblue",
        justify="left" 
        )
    
    id_num_ent.grid(
        column=3, 
        row=2,
        sticky="n"
        )
    
    ime_lbl = tk.Label(
        root,
        text="Ime",
        font=("Segoe UI bold", 16), 
        justify="right"
        )

    ime_lbl.grid(
        column=2, 
        row=3,
        sticky="ne"
        )

    ime_ent = tk.Entry(
        root, 
        textvariable=ime_var, 
        font=("Segoe UI", 16), 
        border=1, 
        background="lightblue",
        justify="left"
        )
    
    ime_ent.grid(
        column=3, 
        row=3,
        sticky="n"
        )
    
    prezime_lbl = tk.Label(
        root,
        text="Prezime",
        font=("Segoe UI bold", 16), 
        justify="right"
        )

    prezime_lbl.grid(
        column=2, 
        row=4,
        sticky="ne"
        )

    prezime_ent = tk.Entry(
        root,  
        textvariable=prezime_var,
        font=("Segoe UI", 16), 
        border=1, 
        background="lightblue",
        justify="left"
        )
    
    prezime_ent.grid(
        column=3, 
        row=4,
        sticky="n"
        )
    
    pins_lbl = tk.Label(
        root,
        text="PIN",
        font=("Segoe UI bold", 16), 
        justify="right"
        )

    pins_lbl.grid(
        column=2, 
        row=5,
        sticky="ne"
        )
    
    pins_ent = tk.Entry(
        root,
        textvariable=pin_var,  
        font=("Segoe UI", 16), 
        border=1,
        background="lightblue", 
        justify="left"
        )
    
    pins_ent.grid(
        column=3, 
        row=5,
        sticky="n"
        )
    
    active_btn = tk.Checkbutton(
        root,
        text="Aktivan",
        variable=active_var,
        font=("Segoe UI bold", 16),
        
    )

    active_btn.grid(
        column=5,
        row=5,
        sticky="nw"
    )
    
    status_dp.grid(
        column=6,
        row=3,
        ipadx=16
        )
    
    save_btn = tk.Button(
        root,
        text="Spremi",
        background="SkyBlue2",
        font=("Segoe UI bold", 12),
        padx=12,
        pady=7,
        command=save_cmd
        )
            
    save_btn.grid(
        column=0,
        row=6,
        sticky="n"
        )

    del_btn = tk.Button(
        root,
        text="Izbriši",
        background="SkyBlue2",
        font=("Segoe UI bold", 12),
        padx=12,
        pady=7,
        command=del_cmd
        )
    
    del_btn.grid(
        column=0,
        row=6,
        sticky="ne"
    )

    del_all_btn = tk.Button(
        root,
        text="Izbriši sve",
        background="SkyBlue2",
        font=("Segoe UI bold", 12),
        padx=12,
        pady=7,
        command=del_all_cmd
        )
    
    del_all_btn.grid(
        column=6,
        row=0,
        sticky="s"
    )
    
    add_btn = tk.Button(
        root,
        text="Dodaj",
        background="SkyBlue2",
        font=("Segoe UI bold", 12),
        padx=12,
        pady=7,
        command=add_cmd
        )
            
    add_btn.grid(
        column=3,
        row=6,
        sticky="n"
        )
    
    exit_btn = tk.Button(
        root,
        text="Izlaz",
        background="SkyBlue2",
        font=("Segoe UI bold", 12),
        padx=12,
        pady=7,
        command=exit_cmd
        )
            
    exit_btn.grid(
        column=6,
        row=6,
        sticky="n"
        )


def check_pin():
    global yes_btn, no_btn
    
    with bm.get_db() as session:

        ent_pin = pin_check.get()

        korisnik = session.query(bm.Korisnik).filter(bm.Korisnik.pin == ent_pin).one_or_none()
        
        
        if korisnik is None:
            status_txt.set("Pogrešan PIN")

        elif korisnik.aktivan == True:
            status_txt.set(f"Dobrodošli, {korisnik.ime} {korisnik.prezime}.")
            user_clear()

        elif korisnik.aktivan == False:
            status_txt.set(f"{korisnik.ime} {korisnik.prezime} nema pristup.")
            user_clear()

        if korisnik.id_num == 0 and korisnik.pin == 8888:
            
            status_txt.set("Želite li ući u administracijske postavke?")

            yes_btn = tk. Button(
                root,
                text="Da",
                background="SkyBlue2",
                padx=15,
                pady=5,
                font=("Segoe UI bold", 11),
                command=lambda: (admin_settings(), admin_clear())
                )
            
            yes_btn.grid(
                column=1,
                row=6,
                sticky="nw"
                )

            no_btn = tk.Button(
                root,
                text="Ne",
                background="SkyBlue2",
                font=("Segoe UI bold", 11),
                padx=15,
                pady=5,
                command= lambda: (status_txt.set(f"Dobrodošli, {korisnik.ime} {korisnik.prezime}."), half_clear())
                )
            
            no_btn.grid(
                column=1,
                row=6,
                sticky="ne"
                )

        
            

def ask_pin():
    global pin_ent, pin_lbl, sub_btn

    status_txt.set("")
    pin_check.set("")

    pin_lbl = tk.Label(
        root,
        text="Unesite PIN",
        font=("Segoe UI", 16), 
        justify="center"
        )

    pin_lbl.grid(
        column=3, 
        row=3,
        )

    pin_ent = tk.Entry(
        root, 
        textvariable=pin_check, 
        font=("Segoe UI", 16), 
        border=3, 
        justify="center",
        show="*"
        )
    
    pin_ent.grid(
        column=3, 
        row=4, 
        sticky="n"
        )

    sub_btn = tk.Button(
        root, 
        text="Otvori", 
        padx=10, 
        pady=5,
        font=("Segoe UI bold", 12),
        background="SkyBlue2",
        command=check_pin
        )
    
    sub_btn.grid(
        column=3, 
        row=5
        )

def get_users():

    with bm.get_db() as session:

        users = session.query(bm.Korisnik).all()

        for user in users:
            user_dict.update({f"korisnik_{user.id_num}" : {
                                    "id_num" : user.id_num,
                                    "ime" : user.ime,
                                    "prezime" : user.prezime,
                                    "pin" : user.pin,
                                    "aktivan" : user.aktivan
                                    }
                                }
                            )
            
    session.close()

    user_dict_var.set([(user_dict[user]["ime"], user_dict[user]["prezime"]) for user in sorted(user_dict)])
    
        
root = tk.Tk()

root.title("SmartKey")
root.geometry("1400x800")

root.columnconfigure((0,1,2,3,4,5,6,7), weight=1, minsize=60) 
root.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1, minsize=10)


status_txt = tk.StringVar()
pin_check = tk.IntVar()
active_var = tk.BooleanVar()
user_dict_var = tk.Variable()
user_dict_var.set([(user_dict[user]["ime"], user_dict[user]["prezime"]) for user in sorted(user_dict)])

id_num_var = tk.IntVar()
id_num_var.set("")
ime_var = tk.StringVar()
prezime_var = tk.StringVar()
pin_var = tk.IntVar()
pin_var.set("")



logo_frame = tk.Frame(
    root,
    height=80,
    width=232,
    background="SkyBlue2"
    )

logo_frame.grid(
    column=0,
    row=0,
    sticky="se"
    )

logo_lbl = tk.Label(
    root,
    text="SmartKey",
    font=("Courier", 26),
    background="SkyBlue2",
    foreground="navy",
    padx=30,
    pady=25
    )

logo_lbl.grid(
    column=0,
    row=0,
    sticky="ne"
    )

pozvoni_btn = tk.Button(
    root, 
    padx=39,
    pady=15, 
    text="Pozvoni", 
    font=("Segoe UI bold", 16), 
    background="SkyBlue2", 
    border=2, 
    justify="center", 
    command=ding_dong
    )

pozvoni_btn.grid(
    column=1, 
    row=2
    )

status_dp = tk.Entry(
    root, 
    textvariable=status_txt, 
    font=("Segoe UI", 18), 
    border=0, 
    state="readonly", 
    justify="center"
    )

status_dp.grid(
    column= 1,
    row=4, 
    ipadx=90, 
    sticky="s"
    )

unlock_btn = tk.Button(
    root, 
    padx=35, 
    pady=15, 
    text="Otključaj", 
    font=("Segoe UI bold", 16), 
    background="SkyBlue2", 
    border=2, 
    justify="center", 
    command=ask_pin
    )

unlock_btn.grid(
    column=3, 
    row=2
    )

bar_frm = tk.Frame(

)

root.mainloop()

