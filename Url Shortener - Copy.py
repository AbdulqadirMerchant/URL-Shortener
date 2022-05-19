from tkinter import *
from tkinter import messagebox
import warnings
import subprocess
import yagmail
warnings.filterwarnings("ignore")
import bitly_api

access = bitly_api.Connection(access_token = "<BITLY ACCESS TOKEN>")
#To register the mail id and password to yagmail
yagmail.register("Sender's mail address", "Sender's password")

#To establish the SMTP connection
mail = yagmail.SMTP(user = "Sender's mail address")

mail_message = """A person has sent you a mail who wants you to click this shortened URL:
{shortened_link}
The original link is this:
{original_link}"""


def shorten_url():
    global shortened_url
    main_url = url_entrybox.get()
    try:
        shortened_url = access.shorten(main_url)
        shortened_url_entrybox.insert(0, shortened_url["url"])
        url_entrybox.delete(0, END)
    except Exception as e:
        messagebox.showerror("Error", e)


def copy_to_clipboard():
    if not shortened_url_entrybox.get():
        messagebox.showerror("Error", "Nothing to copy !!")
        return
    text = "echo "+shortened_url_entrybox.get()+"|clip"
    subprocess.check_call(text, shell = True)


def send_email():
    try:
        mail.send(to = email_entry_box.get(), subject = "Python Shortened URL",
                  contents = mail_message.format(shortened_link = shortened_url["url"],
                                                 original_link = shortened_url["long_url"]))
    except Exception as e:
        messagebox.showerror("Error", e)
        print(e)
    mail_window.destroy()


def open_mail_window():
    global email_entry_box, mail_window
    if not shortened_url_entrybox.get():
        messagebox.showerror("Error", "Please shorten a link to send an email!!")
        return
    mail_window = Toplevel()
    mail_window.title("Send Email")
    mail_window.configure(bg = "cyan")

    send_email_label = Label(mail_window, text = "Enter the mail address:", bg = "cyan",
                             font = ("Verdana", 15))
    send_email_label.grid(row = 0, column = 0, pady = 10)

    email_entry_box = Entry(mail_window, width = 60, font = ("Times New Roman", 20))
    email_entry_box.grid(row = 0, column = 1)

    send_email_button = Button(mail_window, text = "Send Mail", font = ("Comic Sans MS", 15),
                               command = send_email)
    send_email_button.grid(row = 1, column = 1, pady = 10)


root = Tk()
root.configure(bg = "cyan")
root.title("URL Shortener")

enter_url_label = Label(root, text = "Enter the URL:", font = ("Verdana", 15), bg = "cyan")
enter_url_label.grid(row = 0, column = 0)

url_entrybox = Entry(root, width = 60, font = ("Times New Roman", 20))
url_entrybox.grid(row = 0, column = 1, pady = 10)
url_entrybox.focus()

shortened_url_label = Label(root, text = "Shortened URL:", font = ("Verdana", 15), bg = "cyan")
shortened_url_label.grid(row = 1, column = 0)

shortened_url_entrybox = Entry(root, width = 60, font = ("Times New Roman", 20))
shortened_url_entrybox.grid(row = 1, column = 1, pady = 10)

shorten_url_button =  Button(root, text = "Shorten", font = ("Comic Sans MS", 15), command = shorten_url)
shorten_url_button.grid(row = 2, column = 1, pady = 10)

copy_clipboard_button = Button(root, text = "Copy to clipboard", font = ("Comic Sans MS", 15),
                               command = copy_to_clipboard)
copy_clipboard_button.grid(row = 3, column = 1)

send_email_button = Button(root, text = "Send Email", font = ("Comic Sans MS", 15),
                           command = open_mail_window)
send_email_button.grid(row = 4, column = 1, pady = 10)

root.mainloop()
