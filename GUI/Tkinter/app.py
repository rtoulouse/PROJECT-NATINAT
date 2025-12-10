from tkinter import *

#créer une premiere fenetre
window = Tk()

#personnaliser la fenetre
window.title("My Application")
window.geometry("1080x720")
window.minsize(480, 360)
window.iconbitmap("logo-guardia.ico")
window.config(background='black')

#creer la frame
frame = Frame(window, bg='black')

#ajouter un premier texte
label_title = Label (frame, text="Bienvenue sur l'Application", font=("Bebas Neue", 40), bg='black', fg='white')
label_title.pack()

#ajouter un second texte
label_subtitle = Label (frame, text="ajouter une description", font=("Bebas Neue", 15), bg='black', fg='white')
label_subtitle.pack()

#ajouter un premier bouton (s'inscrire)
yt_button = Button(frame, text="S'inscrire", font=("Bebas Neue", 15), bg='white', fg='black')
yt_button.pack(pady=15)

#ajouter un second bouton (se connecter)
yt_button = Button(frame, text="Se Connecter", font=("Bebas Neue", 15), bg='white', fg='black')
yt_button.pack()

#ajouter la frame
frame.pack(expand=YES)

#afficher
window.mainloop()