import cv2
import numpy as np
import time
import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import Cards  # Make sure you have your Cards module in the same directory

# Define constants and initialize variables
GAP_WIDTH = 40
GAP_WIDTH_BY_4 = 19
GAP_COLOR = 120
WHITE = 0

# Function to start the card detection process
def start():
    global videostream, img_label, detected_cards, selected_card_index, pre_proc_img, threshold_img, final_img, card_image

    # Camera settings
    IM_WIDTH = 1280
    IM_HEIGHT = 720
    FRAME_RATE = 10

    # Define font to use
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize camera object and video feed from the camera.
    videostream = cv2.VideoCapture('http://192.168.1.12:8080/video')
    time.sleep(1)  # Give the camera time to warm up

    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = Cards.load_ranks(path + '/Card_Imgs/')
    train_suits = Cards.load_suits(path + '/Card_Imgs/')

    ret, image = videostream.read()
    if not ret:
        return
    
    # Step 1: Show the captured image
    show_image(image, img_label, title='Captured Image')

    # Step 2: Pre-process the image (gray, blur, and threshold it)
    pre_proc = Cards.preprocess_image(image)
    show_image(pre_proc, pre_proc_img, is_gray=True, title='Pre-Processed Image')

    # Step 3: Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

    final_image = image.copy()
    detected_cards.clear()
    card_listbox.delete(0, END)
    if len(cnts_sort) != 0:
        cards = []
        k = 0
        for i in range(len(cnts_sort)):
            if cnt_is_card[i] == 1:
                temp = Cards.preprocess_card(cnts_sort[i], image)
                cards.append(temp)

                cards[k].best_rank_match, cards[k].best_suit_match, cards[k].rank_diff, cards[k].suit_diff = Cards.match_card(cards[k], train_ranks, train_suits)

                final_image = Cards.draw_results(final_image, cards[k])
                detected_cards.append(cards[k])
                card_listbox.insert(END, f"Card {k+1}")
                k += 1

        if len(cards) != 0:
            for i in range(len(cards)):
                temp_image = image.copy()
                cv2.drawContours(temp_image, [cards[i].contour], -1, (255, 0, 0), 2)
                show_image(temp_image, card_image, title='Detected Card')

    # Step 4: Show the final processed image
    show_image(final_image, final_img, title='Final Image')

    videostream.release()

# Function to show images in Tkinter labels
def show_image(image, label, is_gray=False, title='Image'):
    if is_gray:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=img)
    label.config(image=imgtk)
    label.image = imgtk

# Function to stop the camera
def stop():
    global cam_quit
    cam_quit = 1
    videostream.release()
    cv2.destroyAllWindows()

# Function to display selected card's rank and suit
def show_card_details(event):
    global selected_card_index, detected_cards, rank_label, suit_label

    selected_card_index = card_listbox.curselection()[0]
    if detected_cards and selected_card_index < len(detected_cards):
        card = detected_cards[selected_card_index]
        rank_img = card.rank_img
        suit_img = card.suit_img

        # Display rank image
        rank_img = cv2.cvtColor(rank_img, cv2.COLOR_GRAY2RGB)
        rank_img = Image.fromarray(rank_img)
        rank_imgtk = ImageTk.PhotoImage(image=rank_img)
        rank_label.config(image=rank_imgtk)
        rank_label.image = rank_imgtk

        # Display suit image
        suit_img = cv2.cvtColor(suit_img, cv2.COLOR_GRAY2RGB)
        suit_img = Image.fromarray(suit_img)
        suit_imgtk = ImageTk.PhotoImage(image=suit_img)
        suit_label.config(image=suit_imgtk)
        suit_label.image = suit_imgtk

# Initialize the Tkinter window
root = Tk()
root.title("Card Detection")
root.geometry("1280x720")

# Create a frame for the video feed
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(N, S, E, W))

# Create labels for the images at each step
img_label = Label(frame)
img_label.grid(row=0, column=0, columnspan=2)

pre_proc_img = Label(frame)
pre_proc_img.grid(row=1, column=0, columnspan=2)

threshold_img = Label(frame)
threshold_img.grid(row=2, column=0, columnspan=2)

final_img = Label(frame)
final_img.grid(row=3, column=0, columnspan=2)

card_image = Label(frame)
card_image.grid(row=4, column=0, columnspan=2)

rank_label = Label(frame)
rank_label.grid(row=5, column=0, padx=5, pady=5)

suit_label = Label(frame)
suit_label.grid(row=5, column=1, padx=5, pady=5)

# Create a listbox for detected cards
detected_cards = []
selected_card_index = 0

card_listbox = Listbox(frame)
card_listbox.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
card_listbox.bind('<<ListboxSelect>>', show_card_details)

# Create buttons to start and stop the card detection
start_button = ttk.Button(frame, text="Capture and Process", command=start)
start_button.grid(row=7, column=0, padx=5, pady=5)

stop_button = ttk.Button(frame, text="Stop", command=stop)
stop_button.grid(row=7, column=1, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
