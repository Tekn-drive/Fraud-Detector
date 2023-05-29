from pathlib import Path
import tensorflow as tf
import keras
import keras_nlp
import re
import numpy as np
from tkinter import Tk,Canvas,Entry,Text,Button,PhotoImage,messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"build/assets/frame0")
model = tf.keras.models.load_model('SEmodel',compile=False)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),metrics=tf.keras.metrics.BinaryAccuracy())

rating = 0.0
category=""
review=""

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_enter_pressed_rating(event):
    global rating
    rating = float(entry_1.get())

def on_enter_pressed_cat(event):
    global category
    category = entry_2.get()

def on_enter_pressed_review(event):
    global review
    review = entry_3.get("1.0","end-1c")

def identify_review():
    category_list = {'Home and Kitchen': 3,
                    'Sports and Outdoors': 7,
                    'Electronics': 2,
                    'Movies and TV': 5,
                    'Tools and Home Improvement': 8,
                    'Pet Supplies': 6,
                    'Kindle Store': 4,
                    'Books': 0,
                    'Toys and Games': 9,
                    'Clothing, Shoes and Jewelry': 1
                    }

    category_int=category_list[category]
    predictions = model.predict({'text':np.array([review]).astype(str),'rat':np.array([rating]).astype('float32'),'cat':np.array([category_int]).astype('int32')})
    predict = np.round(predictions,0)
    
    if(predict==0):
        messagebox.showinfo('Fraud',"The review is likely to be bot generated/fraud")
    elif(predict==1):
        messagebox.showinfo('Legit',"The review is likely to be legit")

window = Tk()
window.title('Fraud Detector')
window.geometry("700x500")
window.configure(bg = "#FFFFFF")

canvas = Canvas(window,bg = "#FFFFFF",height = 500,width = 700,bd = 0,highlightthickness = 0,relief = "ridge")

canvas.place(x = 0, y = 0)
canvas.create_rectangle(0.0,0.0,700.0,500.0,fill="#3CACEA",outline="")

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(350.0,78.0,image=image_image_1)

canvas.create_text(19.0,132.0,anchor="nw",text="RATING",fill="#000000",font=("Poppins SemiBold", 15 * -1))

canvas.create_text(19.0,212.0,anchor="nw",text="REVIEW",fill="#000000",font=("Poppins SemiBold", 15 * -1))

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(99.0,171.0,image=image_image_2)

image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(350.0,307.0,image=image_image_3)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(99.0,171.0,image=entry_image_1)
entry_1 = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
entry_1.place(x=30.0,y=161.0,width=138.0,height=18.0)
entry_1.bind("<Return>",on_enter_pressed_rating)

image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(598.0,171.0,image=image_image_4)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(598.0,171.0,image=entry_image_2)
entry_2 = Entry(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
entry_2.place(x=525.0,y=161.0,width=146.0,height=18.0)
entry_2.bind("<Return>",on_enter_pressed_cat)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(350.5,307.0,image=entry_image_3)
entry_3 = Text(bd=0,bg="#FFFFFF",fg="#000716",highlightthickness=0)
entry_3.place(x=29.0,y=245.0,width=643.0,height=122.0)
entry_3.bind("<Return>",on_enter_pressed_review)

canvas.create_text(514.0,132.0,anchor="nw",text="CATEGORY",fill="#000000",font=("Poppins SemiBold", 15 * -1))

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=identify_review,relief="flat")
button_1.place(x=250.0,y=429.0,width=200.0,height=33.00006103515625)

window.resizable(False, False)
window.mainloop()
