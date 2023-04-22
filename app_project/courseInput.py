# Devin Zeller & Nicolas Huang
# CS330 - Software Engineering Project
# Course Scheduler App
# ----------------------------------------------------------------------------------------------------------------------

import tkinter
import customtkinter as ctk
from tkinter import *


class MainWindow(ctk.CTk):
    def __init__(self):
        self.mainFrame = super(MainWindow, self).__init__()
        self.geometry("600x400")
        self.title("Course Scheduler")

        # Save gui elements to the list so we can destroy them when switching frames
        self.mainGuiElements = []
        self.listGuiElements = []
        self.weeklyGuiElements = []

        # Define a boolean variable to switch between the windows
        self.windowMode = 0  # 0 - Main, 1 - List, 2 - Weekly view

        # Set window's frame to the courseInput gui
        self.courseInputGUI()


    def courseInputGUI(self):
        """
        Main Gui for user to enter Course information to add to database
        :return: None
        """
        # Set window mode to main gui
        self.windowMode = 0
        
        # Specify Grid (Rows x Columns) for our buttons and labels
        for i in range(0, 4):
            Grid.rowconfigure(self, i, weight=1)
            Grid.columnconfigure(self, i, weight=1)

        # Create the scrollable frame so we can populate it with added courses
        courseInputFrame = ctk.CTkScrollableFrame(
            self,
            width=400,
            height=200
        )
        courseInputFrame.grid(row=1, column=0, columnspan=3, padx=30, pady=5, sticky="EW")
        self.mainGuiElements.append(courseInputFrame)
        # ---------------------------------------------------------------
        #                          Buttons
        # ---------------------------------------------------------------

        # Create course list button
        courseListButton = ctk.CTkButton(self, text="Course List")
        courseListButton.grid(row=0, column=2, pady=5, sticky="EW")
        self.mainGuiElements.append(courseListButton)

        # Add course button
        addCourseButton = ctk.CTkButton(self, text="Add Course")
        addCourseButton.grid(row=3, column=2, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(addCourseButton)

        # Weekly View button
        weeklyView = ctk.CTkButton(self, text="Weekly View", command=self.weeklyGui)
        weeklyView.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(weeklyView)

        # ---------------------------------------------------------------
        #                         Entry Fields
        # ---------------------------------------------------------------

        # Course name
        courseEntry = ctk.CTkEntry(self, placeholder_text="Course Name")
        courseEntry.grid(row=2, column=0, padx=5, sticky="EW")
        self.mainGuiElements.append(courseEntry)

        # Course code entry
        codeEntry = ctk.CTkEntry(self, placeholder_text="Course Code")
        codeEntry.grid(row=2, column=1, sticky="EW")
        self.mainGuiElements.append(codeEntry)

        # Course Credit
        creditEntry = ctk.CTkEntry(self, placeholder_text="Credit(s)")
        creditEntry.grid(row=2, column=2, padx=5, sticky="EW")
        self.mainGuiElements.append(creditEntry)

        # Course meeting time
        meetingTimeEntry = ctk.CTkEntry(self, placeholder_text="Meeting Time")
        meetingTimeEntry.grid(row=3, column=0, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(meetingTimeEntry)

        instructorEntry = ctk.CTkEntry(self, placeholder_text="Instructor Name")
        instructorEntry.grid(row=3, column=1, pady=5, sticky="EW")
        self.mainGuiElements.append(instructorEntry)

    def weeklyGui(self):
        """
        Weekly Calendar view gui
        :return: None
        """
        # Remove the main gui widgets to make room for weekly view widgets
        self.removeMainGui()

        # Set our window mode to weekly view
        self.windowMode = 2

        # Add our widgets (change stuff here, this is just test code)
        randomButton = ctk.CTkButton(self, text="Course Input", command=self.backToMain)
        randomButton.grid(row=2, column=2)
        self.weeklyGuiElements.append(randomButton)

    def removeMainGui(self):
        """
        Removes elements on course input to allow new elements to populate
        :return: None
        """
        for element in self.mainGuiElements:
            element.grid_forget()

    def removeListGui(self):
        """
        Removes elements on course list to allow new elements to populate
        :return: None
        """
        for element in self.listGuiElements:
            element.grid_forget()

    def removeWeeklyGui(self):
        """
        Removes elements on weekly calendar view to allow new elements to populate
        :return: None
        """
        for element in self.weeklyGuiElements:
            element.grid_forget()

    def backToMain(self):
        """
        Called when we want to move our frame back to the main gui frame.
        :return: None
        """
        # Window mode set to main, reset our list of widgets
        if self.windowMode == 0:
            self.removeMainGui()
            self.mainGuiElements = []

        # Window mode set to list, reset our list of widgets
        elif self.windowMode == 1:
            self.removeListGui()
            self.listGuiElements = []

        # Window mode set to weekly view, reset our list of widgets
        elif self.windowMode == 2:
            self.removeWeeklyGui()
            self.weeklyGuiElements = []

        # Return to the main gui
        self.courseInputGUI()



def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
