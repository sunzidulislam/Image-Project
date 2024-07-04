import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from CardDetector import *

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera Capture App")
        
        # Set the window to full-screen mode
        self.root.attributes('-fullscreen', True)
        
        # Create frames for left and right sections
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.left_frame = tk.Frame(root, width=screen_width//2, height=screen_height, bg='black')
        self.left_frame.place(x=0, y=0)
        
        self.right_frame = tk.Frame(root, width=screen_width//2, height=screen_height, bg='black')
        self.right_frame.place(x=screen_width//2, y=0)
        
        self.left_label = tk.Label(self.left_frame)
        self.left_label.pack(expand=True)
        
        self.right_label = tk.Label(self.right_frame)
        self.right_label.pack(expand=True)
        
        # Create buttons and place them at the bottom
        self.button_frame = tk.Frame(root)
        self.button_frame.place(relx=0.5, rely=0.95, anchor=tk.S)

        self.capture_button = ttk.Button(self.button_frame, text="Capture Image", command=self.capture_image)
        self.capture_button.grid(row=0, column=0, padx=20, pady=10)
        
        self.show_button = ttk.Button(self.button_frame, text="Show Image on Right", command=self.show_image_on_right)
        self.show_button.grid(row=0, column=1, padx=20, pady=10)
        
        self.quit_button = ttk.Button(self.button_frame, text="Quit", command=self.quit_app)
        self.quit_button.grid(row=0, column=2, padx=20, pady=10)
        
        self.list = []
        self.index = -1
        self.cap = None
        set_gui(self)
        
    def capture_image(self):
        self.index = -1
        self.list.clear()
        start()
    
    def add_to_list(self, image):
        self.list.append(image)
        print("Added to list")

    def show_on_left(self,image):
        print("Showing on left")

        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)

        imgtk = ImageTk.PhotoImage(image=img)

        self.left_label.config(image=imgtk)
        self.left_label.image = imgtk

    def show_image_on_right(self):
        print(f"Showing on right: {self.index}")

        if self.index+1 >= len(self.list):
            return
        self.index += 1
        image = self.list[self.index]
        
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)

        imgtk = ImageTk.PhotoImage(image=img)
        self.right_label.config(image=imgtk)
        self.right_label.image = imgtk

    def quit_app(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
