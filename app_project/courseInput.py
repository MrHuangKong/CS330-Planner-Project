# Devin Zeller & Nicolas Huang
# CS330 - Software Engineering Project
# Course Scheduler App
# ----------------------------------------------------------------------------------------------------------------------

import tkinter
import tkinter.messagebox

import customtkinter as ctk
from tkinter import *
from tinydb import TinyDB, Query


class MainWindow(ctk.CTk):
    def __init__(self):
        self.mainFrame = super(MainWindow, self).__init__()
        self.geometry("700x450")
        self.title("Course Scheduler")

        # Save gui elements to the list so we can destroy them when switching frames
        self.mainGuiElements = []
        self.listGuiElements = []
        self.weeklyGuiElements = []

        # Start the Database
        self.db = TinyDB('courses.json')

        # Define a boolean variable to switch between the windows
        self.windowMode = 0  # 0 - Main, 1 - List, 2 - Weekly view

        # Set window's frame to the courseInput gui
        self.courseInputGUI()

    def __del__(self):
        # Close the database
        self.db.close()

    def cleanText(self, text: str) -> str:
        """
        Cleans a string by removing punctuation, and capitalizing it
        :param text: A string to clean
        :return: A cleaned string
        """
        # Define a set of characters to filter out
        filters = ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "\"", "/", "\n",
                   ",", ".", "?", "~", "`", "-", "\'", "\\", "+", "=")

        # Clean user inputted strings
        for filter_ in filters:
            text = text.replace(f"{filter_}", "")
        return text.title()

    def saveCourse(self):
        """
        Save all course information into the database
        :return: None
        """
        # Save the lengths of each entry box
        name = self.courseEntry.get()
        code = self.codeEntry.get()
        credit = self.creditEntry.get()
        # meeting = self.meetingTimeEntry.get()
        location = self.locationEntry.get()
        section = self.courseSectionEntry.get()
        instructor = self.instructorEntry.get()

        # Clean our entries
        name = self.cleanText(name)
        code = self.cleanText(code).upper()
        credit = self.cleanText(credit)
        # meeting = self.cleanText(meeting).upper()
        location = self.cleanText(location)
        section = self.cleanText(section)
        instructor = self.cleanText(instructor)

        # Create a state to break out of our loop
        notFound = True

        # Make sure all entry's are filled
        if len(name) and len(code) and len(credit) and len(instructor) and len(section) and len(location):
            # Check if Course overlaps with previously saved courses
            database = self.db.all()
            # Is database empty?
            if len(database) != 0:
                for courses in database:
                    # If we have a duplicate
                    if (courses['name'] == name and courses['number'] == code and courses['credit'] == credit
                            and courses['instructor'] == instructor and courses['location'] == location and
                            courses['section'] == section):
                        tkinter.messagebox.showwarning("Warning", "Course already exists!")
                        notFound = False
                    # If we have a time conflict
                    # elif courses['meeting'] == meeting:
                    #     tkinter.messagebox.showwarning("Warning", f"Unable to add course, time conflict with "
                    #                                               f"{courses['number']}: {courses['name']} at ")
                    #
                    #     notFound = False
                # If there are no duplicates or time conflicts, save to database
                if notFound:
                    # Save information to data base
                    course = {'number': code, 'name': name, 'section': section, 'credit': credit,
                              'instructor': instructor, 'location': location}
                    self.db.insert(course)
                    print(self.db.all())

                    # Clear our entries
                    self.courseEntry.delete(0, ctk.END)
                    self.codeEntry.delete(0, ctk.END)
                    self.creditEntry.delete(0, ctk.END)
                    self.locationEntry.delete(0, ctk.END)
                    self.instructorEntry.delete(0, ctk.END)


            # Database is empty, add course
            else:
                # Save information to data base
                course = {'number': code, 'name': name, 'section': section, 'credit': credit,
                          'instructor': instructor, 'location': location}
                self.db.insert(course)
                print(self.db.all())

                # Clear our entries
                self.courseEntry.delete(0, ctk.END)
                self.codeEntry.delete(0, ctk.END)
                self.creditEntry.delete(0, ctk.END)
                self.locationEntry.delete(0, ctk.END)
                self.instructorEntry.delete(0, ctk.END)
                self.courseSectionEntry.delete(0, ctk.END)

                # check boxes
                # self.dayOfTheWeekCheckBoxSunday.delete(0, ctk.END)
                # self.dayOfTheWeekCheckBoxMonday.delete(0, ctk.END)
                # self.dayOfTheWeekCheckBoxTuesday.delete(0, ctk.END)
                # self.dayOfTheWeekCheckBoxWednesday.delete(0, ctk.END)
                # self.dayOfTheWeekCheckBoxThursday.delete(0, ctk.END)
                # self.dayOfTheWeekCheckBoxFriday.delete(0, ctk.END)
                # self.dayOfTheWeekCheckBoxSaturday.delete(0, ctk.END)

        else:
            tkinter.messagebox.showwarning("Warning", "All course information must be filled out")

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
        courseInputFrame = ctk.CTkScrollableFrame(self, width=400, height=200)
        courseInputFrame.grid(row=1, column=0, columnspan=3, padx=30, pady=5, sticky="EW")
        self.mainGuiElements.append(courseInputFrame)
        # ---------------------------------------------------------------
        #                          Buttons
        # ---------------------------------------------------------------

        # Create course list button
        courseListButton = ctk.CTkButton(self, text="Course List")
        courseListButton.grid(row=0, column=2, padx=15, pady=5, sticky="EW")
        self.mainGuiElements.append(courseListButton)  # Add to our list of elements so we can delete it

        # Weekly View button
        weeklyView = ctk.CTkButton(self, text="Weekly View", command=self.weeklyGui)
        weeklyView.grid(row=0, column=0, padx=15, pady=5, sticky="EW")
        self.mainGuiElements.append(weeklyView)  # Add to our list of elements so we can delete it

        # Add course button
        addCourseButton = ctk.CTkButton(self, text="Add Course", command=self.saveCourse)
        addCourseButton.grid(row=5, column=2, padx=50, pady=5, sticky="EW")
        self.mainGuiElements.append(addCourseButton)  # Add to our list of elements so we can delete it


        # ---------------------------------------------------------------
        #                         Entry Fields
        # ---------------------------------------------------------------

        # Course name
        self.courseEntry = ctk.CTkEntry(self, placeholder_text="Course Name*")
        self.courseEntry.grid(row=2, column=0, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.courseEntry)

        # Course code entry
        self.codeEntry = ctk.CTkEntry(self, placeholder_text="Course Code*")
        self.codeEntry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.codeEntry)

        # Course Credit
        self.creditEntry = ctk.CTkEntry(self, placeholder_text="Credit(s)*")
        self.creditEntry.grid(row=3, column=1, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.creditEntry)

        # Course meeting Location
        self.locationEntry = ctk.CTkEntry(self, placeholder_text="Location*")
        self.locationEntry.grid(row=3, column=0, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.locationEntry)

        # Course Instructor name
        self.instructorEntry = ctk.CTkEntry(self, placeholder_text="Instructor Name*")
        self.instructorEntry.grid(row=2, column=2, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.instructorEntry)

        # Course Section number
        self.courseSectionEntry = ctk.CTkEntry(self, placeholder_text="Section Number*")
        self.courseSectionEntry.grid(row=3, column=2, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.courseSectionEntry)

        # ---------------------------------------------------------------
        #                         Check Box
        # ---------------------------------------------------------------

        # Course day of the week check boxes
        # Frame for check boxes to get packed to
        self.checkBoxFrame = ctk.CTkFrame(self, width=400, height=30, fg_color="transparent")
        self.checkBoxFrame.grid(row=4, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxFrame)

        # Sunday
        self.checkBoxSunday = ctk.CTkCheckBox(self.checkBoxFrame, text="Sun")
        self.checkBoxSunday.grid(row=0, column=0, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxSunday)

        # Monday
        self.checkBoxMonday = ctk.CTkCheckBox(self.checkBoxFrame, text="Mon")
        self.checkBoxMonday.grid(row=0, column=1, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxMonday)

        # Tuesday
        self.checkBoxTuesday = ctk.CTkCheckBox(self.checkBoxFrame, text="Tue")
        self.checkBoxTuesday.grid(row=0, column=2, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxTuesday)

        # Wednesday
        self.checkBoxWednesday = ctk.CTkCheckBox(self.checkBoxFrame, text="Wed")
        self.checkBoxWednesday.grid(row=0, column=4, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxWednesday)

        # Thursday
        self.checkBoxThursday = ctk.CTkCheckBox(self.checkBoxFrame, text="Thu")
        self.checkBoxThursday.grid(row=0, column=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxThursday)

        # Friday
        self.checkBoxFriday = ctk.CTkCheckBox(self.checkBoxFrame, text="Fri")
        self.checkBoxFriday.grid(row=0, column=6, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxFriday)

        # Saturday
        self.checkBoxSaturday = ctk.CTkCheckBox(self.checkBoxFrame, text="Sat")
        self.checkBoxSaturday.grid(row=0, column=7, pady=5, sticky="EW")
        self.mainGuiElements.append(self.checkBoxSaturday)

        # ---------------------------------------------------------------
        #                         Option Menu
        # ---------------------------------------------------------------

        # ---------------------------------
        # Option Menu Lags Window, pls fix -NH
        # ---------------------------------
        # Frame to add the Start hours, minutes, and AM/PM option menus to
        self.startTimeFrame = ctk.CTkFrame(self, width=5, height=15, fg_color="transparent")
        self.startTimeFrame.grid(row=5, column=0, rowspan=1, sticky="EW")
        self.mainGuiElements.append(self.startTimeFrame)

        # Start
        self.startLabel = ctk.CTkLabel(self.startTimeFrame, text="Start:")
        self.startLabel.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.startLabel)

        # Start Hours
        self.startHoursMenu = ctk.CTkOptionMenu(self.startTimeFrame, width=20, values=["1", "2", "3", "4", "5", "6",
                                                                                       "7", "8", "9", "10", "11", "12"])
        self.startHoursMenu.grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.startHoursMenu)

        # start: ":" for formatting
        self.startTimeLabel = ctk.CTkLabel(self.startTimeFrame, text=":")
        self.startTimeLabel.grid(row=0, column=2, sticky="EW")
        self.mainGuiElements.append(self.startTimeLabel)

        # Start Minutes
        self.startMinutesMenu = ctk.CTkOptionMenu(self.startTimeFrame, width=20, values=["00", "05", "10", "15", "20",
                                                                                         "25", "30", "35", "40", "45",
                                                                                         "50", "55"])
        self.startMinutesMenu.grid(row=0, column=3, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.startMinutesMenu)

        # Start AM/PM
        self.startAmPmMenu = ctk.CTkOptionMenu(self.startTimeFrame, width=20, values=["AM", "PM"])
        self.startAmPmMenu.grid(row=0, column=4, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.startAmPmMenu)

        # Frame to add the End hours, minutes, and AM/PM option menus to
        self.endTimeFrame = ctk.CTkFrame(self, width=5, height=15, fg_color="transparent")
        self.endTimeFrame.grid(row=5, column=1, rowspan=1, sticky="EW")
        self.mainGuiElements.append(self.endTimeFrame)

        # End
        self.endLabel = ctk.CTkLabel(self.endTimeFrame, text="End:")
        self.endLabel.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.endLabel)

        # End Hours
        self.endHoursMenu = ctk.CTkOptionMenu(self.endTimeFrame, width=20, values=["1", "2", "3", "4", "5", "6", "7",
                                                                                   "8", "9", "10", "11", "12"])
        self.endHoursMenu.grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.endHoursMenu)

        # end: ":" for formatting
        self.endTimeLabel = ctk.CTkLabel(self.endTimeFrame, text=":")
        self.endTimeLabel.grid(row=0, column=2, sticky="EW")
        self.mainGuiElements.append(self.endTimeLabel)

        # End Minutes
        self.endMinutesMenu = ctk.CTkOptionMenu(self.endTimeFrame, width=20, values=["00", "05", "10", "15", "20",
                                                                                     "25", "30", "35", "40", "45", "50",
                                                                                     "55"])
        self.endMinutesMenu.grid(row=0, column=3, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.endMinutesMenu)

        # End AM/PM
        self.endAmPmMenu = ctk.CTkOptionMenu(self.endTimeFrame, width=20, values=["AM", "PM"])
        self.endAmPmMenu.grid(row=0, column=4, padx=5, pady=5, sticky="EW")
        self.mainGuiElements.append(self.endAmPmMenu)

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
