import cv2
import numpy as np
import time
import os
import Cards

### ---- INITIALIZATION ---- ###
# Define constants and initialize variables

GAP_WIDTH = 40
GAP_WIDTH_BY_4 = 19
GAP_COLOR = 120
WHITE = 0


def merge_horiz(image1, image2):
    height1, width1 = image1.shape
    height2, width2 = image2.shape

    new_height = max(height1, height2)
    new_width = width1 + width2

    merged_image = WHITE * np.ones( (new_height, new_width+GAP_WIDTH), dtype=np.uint8)

    pad = (new_height - height1)//2
    
    # Copy over the first image
    for x in range(height1):
        for y in range(width1):
            merged_image[x+pad][y] = image1[x][y]

    # vertical gap of width 4px
    for x in range(new_height):
        for i in range(GAP_WIDTH_BY_4, GAP_WIDTH-GAP_WIDTH_BY_4):
            merged_image[x][width1+i] = GAP_COLOR

    # Copy over the second image
    pad = (new_height - height2)//2
    for x in range(height2):
        for y in range(width2):
            merged_image[x+pad][width1 + GAP_WIDTH +y] = image2[x][y]

    return merged_image

def merge_vert(image1, image2):
    height1, width1 = image1.shape

    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    height2, width2 = image2.shape

    new_width = max(width1, width2)
    new_height = height1 + height2

    merged_image = WHITE * np.ones( (new_height+GAP_WIDTH, new_width), dtype=np.uint8)

    pad = (new_width - width1)//2
    # Copy over the first image
    for x in range(height1):
        for y in range(width1):
            merged_image[x][y+pad] = image1[x][y]
    
    # horiz gap of width 4px
    for y in range(new_width):
        for i in range(GAP_WIDTH_BY_4, GAP_WIDTH-GAP_WIDTH_BY_4):
            merged_image[height1+i][y] = GAP_COLOR

    # Copy over the second image
    pad = ( new_width - width2)//2
    for x in range(height2):
        for y in range(width2):
            merged_image[height1 + GAP_WIDTH + x][y+pad] = image2[x][y]

    return merged_image


def merge_images(image1, image2, horiz = False):
    if horiz:
        return merge_horiz(image1,image2)
    else:
        return merge_vert(image1,image2)


def start():
    ## Camera settings
    IM_WIDTH = 1280
    IM_HEIGHT = 720 
    FRAME_RATE = 10

    ## Initialize calculated frame rate because it's calculated AFTER the first time it's displayed
    frame_rate_calc = 1
    freq = cv2.getTickFrequency()

    ## Define font to use
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Initialize camera object and video feed from the camera. The video stream is set up
    # as a seperate thread that constantly grabs frames from the camera feed. 
    # See VideoStream.py for VideoStream class definition
    ## IF USING USB CAMERA INSTEAD OF PICAMERA,
    ## CHANGE THE THIRD ARGUMENT FROM 1 TO 2 IN THE FOLLOWING LINE:
    
    videostream = cv2.VideoCapture('http://192.168.1.12:8080/video')
    time.sleep(1) # Give the camera time to warm up

    # Load the train rank and suit images
    path = os.path.dirname(os.path.abspath(__file__))
    train_ranks = Cards.load_ranks( path + '/Card_Imgs/')
    train_suits = Cards.load_suits( path + '/Card_Imgs/')


    ### ---- MAIN LOOP ---- ###
    # The main loop repeatedly grabs frames from the video stream
    # and processes them to find and identify playing cards.

    def show(image, title = 'Image'):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cam_quit = 0 # Loop control variable

    # Begin capturing frames
    if 1 == 1:
    # while cam_quit == 0:

        # Grab frame from video stream
        ret, image = videostream.read()
        #image = cv2.imread('D:\\4-1\\OpenCV-Playing-Card-Detector-master\\OpenCV-Playing-Card-Detector-master\\images\\cardd.jpg')
        
        #image = cv2.resize(image, (1024,1024))
        #show(image,title="Input Image")
        # image = cv2.resize(image, (1024,1024))
        # ret = True

        # if not ret:
        #     continue

        # Start timer (for calculating frame rate)
        # t1 = cv2.getTickCount()

        # global gui
        # gui.show_on_left(image)

        # Pre-process camera image (gray, blur, and threshold it)
        pre_proc = Cards.preprocess_image(image)
        # gui.add_to_list(pre_proc)
        
        # Find and sort the contours of all cards in the image (query cards)
        cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

        # print(len(cnts_sort))

        final_image = image.copy()
        # If there are no contours, do nothing
        if len(cnts_sort) != 0:

            # Initialize a new "cards" list to assign the card objects.
            # k indexes the newly made array of cards.
            cards = []
            k = 0
            
            # For each contour detected:
            for i in range(len(cnts_sort)):
                if (cnt_is_card[i] == 1):

                    # Create a card object from the contour and append it to the list of cards.
                    # preprocess_card function takes the card contour and contour and
                    # determines the cards properties (corner points, etc). It generates a
                    # flattened 200x300 image of the card, and isolates the card's
                    # suit and rank from the image.
                    temp = Cards.preprocess_card(cnts_sort[i],image)
                    cards.append(temp)

                    # show(temp.rank_img, 'Temporary')

                    # Find the best rank and suit match for the card.
                    cards[k].best_rank_match,cards[k].best_suit_match,cards[k].rank_diff,cards[k].suit_diff = Cards.match_card(cards[k],train_ranks,train_suits)

                    # Draw center point and match result on the image.
                    
                    final_image = Cards.draw_results(final_image, cards[k])

                    k = k + 1
            
            # Draw card contours on image (have to do contours all at once or
            # they do not show up properly for some reason)
            if (len(cards) != 0):
                temp_cnts = []
                for i in range(len(cards)):
                    temp_image = image.copy()
                    temp_cnts.append(cards[i].contour)
                    cv2.drawContours(temp_image, [cards[i].contour], -1, (255,0,0),2)

                    merged_horizontal = merge_horiz(cards[i].suit_img, cards[i].rank_img)
                    # merged = merge_vert(merged_horizontal, temp_image)
                    # gui.add_to_list(merged)
                    
                    cv2.imshow('Suit', cards[i].suit_img)
                    cv2.imshow('Rank', cards[i].rank_img)
                    show(temp_image, title='Main image')

                # cv2.drawContours(image,temp_cnts, -1, (255,0,0), 2)
            
        # Draw framerate in the corner of the image. Framerate is calculated at the end of the main loop,
        # so the first time this runs, framerate will be shown as 0.
        cv2.putText(final_image,"FPS: "+str(int(frame_rate_calc)),(10,26),font,0.7,(255,0,255),2,cv2.LINE_AA)

        # Finally, display the image with the identified cards!
        show(final_image, 'Final image')
        # cv2.imshow("Card Detector",final_image)

        # Calculate framerate
        # t2 = cv2.getTickCount()
        # time1 = (t2-t1)/freq
        # frame_rate_calc = 1/time1
        
        # Poll the keyboard. If 'q' is pressed, exit the main loop.
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cam_quit = 1
            

    # Close all windows and close the PiCamera video stream.
    cv2.waitKey(0)
    cv2.destroyAllWindows()

gui = None
def set_gui(g):
    global gui
    gui = g

start()