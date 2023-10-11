import tkinter as tk
import socket
import subprocess

game_path = "pong.py"

# Create socket connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 6969

# Connect to server
client_socket.connect((host, port))

def send_message():
    message = entry.get()
    if message:
        chat_listbox.insert(tk.END, "You: " + message)
        entry.delete(0, tk.END)
        client_socket.send(message.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8")
        if response == "exit":
            client_socket.close()
            root.destroy()
            return
        elif response == "game":
            client_socket.send("received".encode("utf-8"))
            try:
                subprocess.Popen(["python", game_path])
            except Exception as e:
                print(e)
            finally:
                response = client_socket.recv(1024).decode("utf-8")
        elif response.startswith("Here are the top"):
            cnt = int(response.split()[4])
            receive_message(response)
            for _ in range(2 * cnt):
                response = client_socket.recv(1024).decode("utf-8")
                client_socket.send("received".encode("utf-8"))
                receive_message(response)
            response = client_socket.recv(1024).decode("utf-8")

        receive_message(response)
        entry.delete(0, tk.END)

def receive_message(message):
    chat_listbox.insert(tk.END, "Fang: " + message)

# Main window
root = tk.Tk()
root.geometry("500x500")
root.title("Chatbot")

# Chat history listbox
chat_listbox = tk.Listbox(root, width=75, height=20, font=("Arial", 12), bd=3)
chat_listbox.pack(padx=10, pady=10)

# Input field
entry = tk.Entry(root, width=50, font=("Arial", 12), justify=tk.CENTER, bd=3)
entry.pack(padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="SEND", command=send_message, width=20, height=2, bg="blue", fg="white", bd=3, activebackground="lightblue")
send_button.pack(padx=10, pady=10)

# Handle pressing Enter key
def handle_keypress(event):
    if event.keysym == "Return":
        send_message()

# Press enter key to send_message
entry.bind("<KeyPress>", handle_keypress)

root.mainloop()
