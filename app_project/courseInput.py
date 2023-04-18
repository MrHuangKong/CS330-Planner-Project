<<<<<<< Updated upstream
# Adding this line for Exercise 7 - NH
# Adding this line for Exercise 7 - DZ
=======
# import tkinter
# import customtkinter
#
#
# # Create the scrollable frame
# class MyFrame(customtkinter.CTkScrollableFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#
#         # add widgets onto the frame...
#         self.label = customtkinter.CTkLabel(self)
#         self.label.grid(row=0, column=0, padx=20)
#
#
#
# # Create the window
# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#
#         self.my_frame = MyFrame(master=self, width=300, height=200)
#         self.my_frame.grid(row=0, column=0, padx=20, pady=20)
#
#     # def button_event(self):
#     #     print("button pressed")
#     #
#     # button = customtkinter.CTkButton(master=self.my_frame, text="CTkButton", command=button_event)
#     # button.pack(padx=20, pady=10)
#     #
#
# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
#

# ----------------------------------------------------------------------------------------------------------------------
>>>>>>> Stashed changes

import tkinter
import customtkinter as ctk
from tkinter import *

# window
window = ctk.CTk()
# labeling window

window.title('Class Input')
# frame to populate classes that have been input

window.geometry("600x350")

# Specify Grid
Grid.rowconfigure(window, 0, weight=1)
Grid.columnconfigure(window, 0, weight=1)
Grid.rowconfigure(window, 1, weight=1)
Grid.columnconfigure(window, 1, weight=1)
Grid.rowconfigure(window, 2, weight=1)
Grid.columnconfigure(window, 2, weight=1)
Grid.rowconfigure(window, 3, weight=1)
Grid.columnconfigure(window, 3, weight=1)


courseInputFrame = ctk.CTkScrollableFrame(
    window,
    width=400,
    height=200)
courseInputFrame.grid(row=1, column=0, columnspan=3, padx=30, pady=5, sticky="EW")

# generate course list button
generateCourseListButton = ctk.CTkButton(
    window,
    text="Generate Course List")
generateCourseListButton.grid(row=0, column=2, pady=5, sticky="EW")
# Add Course button
generateAddCourse = ctk.CTkButton(
    window,
    text="Add Course")
generateAddCourse.grid(row=3, column=2, pady=5, sticky="EW")
# Weekly View button
generateWeeklyView = ctk.CTkButton(
    window,
    text="Weekly View")
generateWeeklyView.grid(row=0, column=0, pady=5, sticky="EW")

# Course Name Entry
entry = ctk.CTkEntry(
    window,
    placeholder_text="Course Name")
entry.grid(row=2, column=0, sticky="EW")
# Course Code Entry
entry = ctk.CTkEntry(
    window,
    placeholder_text="Course Code")
entry.grid(row=2, column=1, sticky="EW")
# Course Credit
entry = ctk.CTkEntry(
    window,
    placeholder_text="Credit")
entry.grid(row=2, column=2, sticky="EW")
# Course Meeting Time
entry = ctk.CTkEntry(
    window,
    placeholder_text="Meeting Time")
entry.grid(row=3, column=0, pady=5, sticky="EW")
# Course Instructor
entry = ctk.CTkEntry(
    window,
    placeholder_text="Instructor")
entry.grid(row=3, column=1, pady=5, sticky="EW")

# run
window.mainloop()