import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
from datetime import datetime

# Create GUI window
root = tk.Tk()
root.title("MESSENGER")
root.geometry("700x500")
root.resizable(False, False)

# Frame for chat display & user list
frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# User List Panel
user_list = tk.Listbox(frame, width=20)
user_list.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

# Chat display area
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state='disabled')
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Entry field
entry_field = tk.Entry(root, font=('Arial', 14))
entry_field.pack(padx=10, pady=(0, 10), fill=tk.X)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = ""

def listen_for_messages():
    while True:
        try:
            message = client_socket.recv(2048).decode('utf-8')
            if message:
                sender, content = message.split('~', 1)
                display_message(f"[{datetime.now().strftime('%H:%M:%S')}] {sender}: {content}")
            else:
                break
        except:
            break

def display_message(msg):
    text_area.config(state='normal')
    text_area.insert(tk.END, msg + '\n')
    text_area.yview(tk.END)
    text_area.config(state='disabled')

def send_message(event=None):
    msg = entry_field.get().strip()
    if msg:
        try:
            client_socket.sendall(msg.encode())
            entry_field.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "Message not sent. Server may be down.")

def disconnect():
    client_socket.sendall("exit".encode())  # Notify server
    client_socket.close()
    root.destroy()

def connect_to_server():
    global username
    try:
        client_socket.connect(('127.0.0.1', 1234))
    except:
        messagebox.showerror("Error", "Unable to connect to server.")
        root.destroy()
        return

    username = simpledialog.askstring("Username", "Enter your username", parent=root)
    if not username:
        messagebox.showwarning("Username Required", "You must enter a username.")
        root.destroy()
        return

    client_socket.sendall(username.encode())

    # Start listening thread
    threading.Thread(target=listen_for_messages, daemon=True).start()

# Bind Enter key to send message
entry_field.bind('<Return>', send_message)

# Disconnect Button
disconnect_button = tk.Button(root, text="Disconnect", command=disconnect, fg="red", font=('Arial', 12))
disconnect_button.pack(pady=(0, 10))

# Start everything
connect_to_server()
root.mainloop()