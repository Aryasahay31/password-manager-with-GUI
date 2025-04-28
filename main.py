from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters =randint(8, 10)
    nr_symbols =randint(2, 4)
    nr_numbers =randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)

    pyperclip.copy(password)  #copies the password in the clipboard as soon as it is generated

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data ={
        website:{
            "email": email,
            "password": password,
        }
    }

    if len(website) ==0  or len(password) == 0:
        messagebox.showinfo(title = "Oops", message= "Please make sure you haven't left any field empty.")

    else:
        try:
            with open("data.json", "r") as data_file:
                # json.dump(new_data, data_file, indent = 4)   #TODO: write data to json file
                # data = json.load(data_file)                  #TODO: json.load converts json data into python dictionary
                # STEP-1 Reading old data
                data = json.load(data_file)               #TODO: updating json data has 3 step process

        except FileNotFoundError:
            with open ("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent= 4)

        else:
            # STEP-2 Updating old data with new data
            data.update(new_data)


            with open("data.json", "w") as data_file:
                # STEP-3 Saving updated data
                json.dump(data, data_file, indent = 4)

        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)
# ---------------------------- FIND PASSWORD SETUP ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open ("data.json") as data_file:
            data = json.load(data_file)  #python dictionary created from java format data
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="This file does not exist!")
    else:
        if website in data:
            email= data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email} Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No detail for {website} exists!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx= 20, pady=20)
canvas = Canvas(width=200, height=200) #same as the size of the image
logo_img = PhotoImage(file= "logo.png")
canvas.create_image(100, 100, image= logo_img)
canvas.grid(row=0, column=1, )


# Buttons
gp_button = Button(text= "Generate Password", command= generate_password)
gp_button.grid(column= 2, row =3)

add_button = Button(text= "Add", width= 35, command = save)
add_button.grid(column= 1, row = 4, columnspan = 2)

search_button = Button(text="Search", width=13, command = find_password)
search_button.grid( row=1, column=2)

#Labels
website_label = Label(text="Website:")
website_label.grid(row= 1, column= 0)

email_label = Label(text="Email/Username:")
email_label.grid( row= 2, column= 0)

password_label = Label(text="Password:")
password_label.grid(row= 3, column= 0)

# Entry
website_input = Entry(width = 18)
website_input.grid(row =1,column =1)
website_input.focus()

email_input = Entry(width = 35)
email_input.grid(row =2, column =1, columnspan = 2 )
email_input.insert(0, "aryasahay2001@gmail.com")
password_input = Entry(width = 18)
password_input.grid(row =3, column =1)

window.mainloop()
