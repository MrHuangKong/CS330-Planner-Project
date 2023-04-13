# Adding this line for Exercise 7 - NH
# Adding this line for Exercise 7 - DZ

import tkinter
import customtkinter


# Create the scrollable frame
class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)



# Create the window
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.my_frame = MyFrame(master=self, width=300, height=200)
        self.my_frame.grid(row=0, column=0, padx=20, pady=20)

    def button_event():
        print("button pressed")

    button = customtkinter.CTkButton(master=MyFrame, text="CTkButton", command=button_event)
    button.pack(padx=20, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()

