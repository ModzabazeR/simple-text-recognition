import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
# from PIL import Image, ImageGrab

# Configure your tesseract path here
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\TesseractOCR\tesseract.exe'
root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename()
img = cv2.imread(filepath)
img = cv2.resize(img, None, fx=1, fy=1)


def trim_str(raw_txt):
    new_txt = ''
    for i in range(len(raw_txt)):
        if ord(raw_txt[i]) != 32:  # space
            new_txt += raw_txt[i]
        elif ord(raw_txt[i + 1]) < 3585:  # not Thai character --> include space
            new_txt += raw_txt[i]
    return new_txt


def detect_characters():
    # Detecting Characters
    hImg, wImg = img.shape
    boxes = pytesseract.image_to_boxes(img)
    print("Detected: ")

    for b in boxes.splitlines():
        b = b.split(' ')  # [letter, x, y, width, height, 0]

        # Define a variable based on list's data
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])

        # Create a box around the letters
        cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 0, 255), 1)

        # Shows the detected text
        cv2.putText(img, b[0], (x, hImg - y + 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 255), 1)

        print(b[0])
    cv2.imshow('Result', img)
    cv2.waitKey(0)


def detect_words():
    # Detecting Words
    hImg, wImg = img.shape
    conf = "--psm 3"
    boxes = pytesseract.image_to_data(img, config=conf, lang='eng+tha')
    b_string = ""
    new_txt = ""

    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()  # Turns b into a list
            if len(b) == 12:
                # Define a variable based on list's data
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                # Create a box around the words
                cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
                # Shows the detected text
                cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 255), 1)
                b_string = b_string + b[11] + " "

    # for x, i in enumerate(range(len(b_string))):
    #     print(x, b_string[i])

    print(f"Detected: \n{b_string}")
    cv2.imshow('Result', img)
    cv2.waitKey(0)


def detect_digits():
    # Detecting digits
    hImg, wImg = img.shape
    cong = r'--oem 3 --psm 6 outputbase digits'
    boxes = pytesseract.image_to_data(img, config=cong)
    print("Detected: ")

    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()  # Turns b into a list
            if len(b) == 12:
                # Define a variable based on list's data
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                # Create a box around the words
                cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
                # Shows the detected text
                cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50, 50, 255), 1)
                print(b[11])

    cv2.imshow('Result', img)
    cv2.waitKey(0)


def main():
    def alternative():
        if e.get() == "beta":
            result = pytesseract.image_to_string(img, lang='eng+tha')
            new_txt = trim_str(result)
            print(new_txt)
            cv2.imshow('Result', img)
            cv2.waitKey(0)
        else:
            return

    fixed_font = "Calibri"
    main_root = tk.Tk()
    main_root.geometry("488x813")
    main_root.title("Text Recognition")

    size_slider = tk.Scale(main_root, from_=1, to=100, orient=tk.HORIZONTAL)
    size_slider.set(100)

    heading = tk.Label(main_root, text="What do you want to detect?", bg="#11BE94", width="300", height="2",
                       font=(fixed_font, 13))

    characters = tk.Button(main_root, text="Characters", command=detect_characters, height="2", width="30")
    words = tk.Button(main_root, text="Words", command=detect_words, height="2", width="30")
    digits = tk.Button(main_root, text="Digits", command=detect_digits, height="2", width="30")

    resize_label = tk.Label(main_root, text="Image Resize (%) :")

    e = tk.Entry(main_root, width=25)
    beta_button = tk.Button(main_root, text="Done", command=alternative, height="2", width="10")

    heading.pack()

    tk.Label(main_root, text="").pack()

    characters.pack()

    tk.Label(main_root, text="").pack()

    words.pack()

    tk.Label(main_root, text="").pack()

    digits.pack()

    tk.Label(main_root, text="").pack()

    resize_label.pack()
    size_slider.pack()

    tk.Label(main_root, text="").pack()
    tk.Label(main_root, text="").pack()

    e.pack()
    tk.Label(main_root, text="").pack()
    beta_button.pack()

    root.mainloop()

    size_indicator = size_slider.get() / 100


try:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 81, 11)
    main()

except cv2.error:
    print("Unsupported file extension.")
    input("Press Enter to exit.")
