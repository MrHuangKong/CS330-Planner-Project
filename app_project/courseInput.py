# Devin Zeller & Nicolas Huang
# CS330 - Software Engineering Project
# Course Scheduler App
# ----------------------------------------------------------------------------------------------------------------------

# Import library for GUI
import tkinter
import tkinter.messagebox
from tkinter import *
import customtkinter as ctk

# Import database
from tinydb import TinyDB, Query

# Import our CourseClass frame object
from CourseClass import CourseFrame

# Import Process library to change priority
import psutil
import os
import sys

class MainWindow(ctk.CTk):
    def __init__(self):
        self.mainFrame = super(MainWindow, self).__init__()
        self.geometry("700x450")
        self.title("Course Scheduler")
        self.iconbitmap("schedule5-32.ico")

        # Save gui elements to the list so we can destroy them when switching frames
        # Use if we aren't destroying children widgets (aka using grid_forget(), currently has memory leak)
        # self.mainGuiElements = []
        # self.listGuiElements = []
        # self.weeklyGuiElements = []

        # Start the Database
        self.db = TinyDB('courses.json')

        # Define a boolean variable to switch between the windows
        self.windowMode = 0  # 0 - Main, 1 - List, 2 - Weekly view

        # Set window's frame to the courseInput gui
        self.courseInputGUI()

        # Keep track if we're in edit mode
        self.editMode = False

        # Keep track of what entity we're editing in the database
        self.docID = None

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
        text = text.lstrip().rstrip()
        return text.title()

    def checkDays(self, newDays: list, savedDays: list) -> bool:
        """
        Check if any of the new days overlap with our existing saved days in the database
        :param newDays: List of days that a new course has
        :param savedDays: List of days that a saved course has
        :return: Return True if we have a days overlap, false if not
        """
        dayOverlap = False
        for i in zip(newDays, savedDays):
            # If we have a match for the days, return True
            if i[0] == i[1] and i[0] == 1:
                dayOverlap = True
                break
            else:  # No class day matches
                pass
        return dayOverlap

    def saveCourse(self):
        """
        Save all course information into the database
        :return: None
        """
        # Save the lengths of each entry box
        name = self.courseEntry.get()
        code = self.codeEntry.get()
        credit = self.creditEntry.get()
        location = self.locationEntry.get()
        section = self.courseSectionEntry.get()
        instructor = self.instructorEntry.get()

        # Save the days of the week to a list
        dayOfWeek = [self.checkBoxSunday.get(), self.checkBoxMonday.get(), self.checkBoxTuesday.get(),
                     self.checkBoxWednesday.get(), self.checkBoxThursday.get(), self.checkBoxFriday.get(),
                     self.checkBoxSaturday.get()]

        # Save the time from the option menu
        sH = int(self.startHoursMenu.get())
        sM = int(self.startMinutesMenu.get())
        eH = int(self.endHoursMenu.get())
        eM = int(self.endMinutesMenu.get())

        # Calculate starting time
        if self.startAmPmMenu.get() == 'AM' and sH != 12:
            startTime = sH + (sM / 60)
        elif sH == 12 and self.startAmPmMenu.get() == 'PM':  # Its noon
            startTime = sH + (sM / 60)
        else:  # PM
            startTime = (sH + 12) + (sM / 60)

        # Calculate ending time
        if self.endAmPmMenu.get() == 'AM' and eH != 12:
            endTime = eH + (eM / 60)
        elif eH == 12 and self.endAmPmMenu.get() == 'PM':  # Its noon
            endTime = eH + (eM / 60)
        else:  # PM
            endTime = (eH + 12) + (eM / 60)

        # Clean our entries
        name = self.cleanText(name)
        code = self.cleanText(code).upper()
        credit = self.cleanText(credit)
        location = self.cleanText(location)
        section = self.cleanText(section)
        instructor = self.cleanText(instructor)

        # Create a state to break out of our loop
        notFound = True

        # Save whether user wants to add course or not
        checkUser = 'yes'

        # User is editing a course
        if self.editMode:
            # Update the Database
            self.db.update({'number': code, 'name': name, 'section': section, 'credit': credit,
                                  'startTime': startTime, 'endTime':endTime, 'dayOfWeek':dayOfWeek,
                                  'instructor': instructor, 'location': location}, doc_ids=[self.docID.doc_id])
            # Refresh the frame with the CourseClass objects
            self.backToMain()

            self.editMode = False
        # User isn't editing a course
        else:
            # Make sure all entry's are filled
            if len(name) and len(code) and len(credit) and len(instructor) and len(section) and len(location) and \
                    sum(dayOfWeek):

                # Check if user is entering a start time late in the day
                if startTime >= 21 and checkUser == "yes":
                    checkUser = tkinter.messagebox.askquestion("Warning", "Start time is later than 9 PM, add anyways?",
                                                               icon="warning")

                # Check if start time and end time isn't too long
                if abs(startTime - endTime) > 3.0 and checkUser == "yes":
                    checkUser = tkinter.messagebox.askquestion("Warning", "Class duration seems too long, add anyways?",
                                                               icon="warning")

                #  Cancel adding the class
                if checkUser == 'no':
                    return

                # Check if Course overlaps with previously saved courses
                database = self.db.all()
                # Is database empty?
                if len(database) != 0:
                    for courses in database:
                        # If we have a duplicate
                        if courses['name'] == name and courses['number'] == code and courses['section'] == section and \
                            notFound:
                            tkinter.messagebox.showwarning("Warning", "Course already exists!")
                            notFound = False
                        # If we have a time and classroom conflict
                        elif courses['startTime'] <= endTime and startTime <= courses['endTime'] \
                                and self.checkDays(dayOfWeek, courses['dayOfWeek']) and courses['location'] == location:
                            tkinter.messagebox.showwarning("Warning", f"Unable to add course, due to time and classroom "
                                                                      f"conflict with \n"
                                                                      f"{courses['number']}: {courses['name']}-"
                                                                      f"{courses['section']} in room "
                                                                      f"{courses['location']}")

                            notFound = False
                    # If there are no duplicates or time conflicts, save to database
                    if notFound:
                        # Save information to data base
                        course = {'number': code, 'name': name, 'section': section, 'credit': credit,
                                  'startTime': startTime, 'endTime':endTime, 'dayOfWeek':dayOfWeek,
                                  'instructor': instructor, 'location': location}
                        self.db.insert(course)
                        # Add course to our course view
                        courseFrame = CourseFrame(self, self.courseInputFrame, name, code,
                                                  instructor,
                                                  location, credit, section,
                                                  dayOfWeek, startTime, endTime, self.db)
                        courseFrame.createUI()
                        #TODO: Remove or comment out, debugging purposes
                        print(self.db.all())

                        # Clear our entries
                        self.courseEntry.delete(0, ctk.END)
                        self.codeEntry.delete(0, ctk.END)
                        self.creditEntry.delete(0, ctk.END)
                        self.locationEntry.delete(0, ctk.END)
                        self.instructorEntry.delete(0, ctk.END)
                        self.courseSectionEntry.delete(0, ctk.END)

                        # reset check boxes
                        self.checkBoxSunday.deselect()
                        self.checkBoxMonday.deselect()
                        self.checkBoxTuesday.deselect()
                        self.checkBoxWednesday.deselect()
                        self.checkBoxThursday.deselect()
                        self.checkBoxFriday.deselect()
                        self.checkBoxSaturday.deselect()

                        # reset time option menu
                        self.startHoursMenu.set("9")
                        self.startMinutesMenu.set("00")
                        self.startAmPmMenu.set("AM")
                        self.endHoursMenu.set("10")
                        self.endMinutesMenu.set("00")
                        self.endAmPmMenu.set("AM")

                # Database is empty, add course
                else:
                    # Save information to data base
                    course = {'number': code, 'name': name, 'section': section, 'credit': credit,
                              'startTime': startTime, 'endTime': endTime, 'dayOfWeek': dayOfWeek,
                              'instructor': instructor, 'location': location}
                    self.db.insert(course)
                    # Add course to our course view
                    courseFrame = CourseFrame(self, self.courseInputFrame, name, code,
                                              instructor,
                                              location, credit, section,
                                              dayOfWeek, startTime, endTime, self.db)
                    courseFrame.createUI()
                    # TODO: Remove or comment out, debugging purposes
                    print(self.db.all())

                    # Clear our entries
                    self.courseEntry.delete(0, ctk.END)
                    self.codeEntry.delete(0, ctk.END)
                    self.creditEntry.delete(0, ctk.END)
                    self.locationEntry.delete(0, ctk.END)
                    self.instructorEntry.delete(0, ctk.END)
                    self.courseSectionEntry.delete(0, ctk.END)

                    # reset check boxes
                    self.checkBoxSunday.deselect()
                    self.checkBoxMonday.deselect()
                    self.checkBoxTuesday.deselect()
                    self.checkBoxWednesday.deselect()
                    self.checkBoxThursday.deselect()
                    self.checkBoxFriday.deselect()
                    self.checkBoxSaturday.deselect()

                    # reset time option menu
                    self.startHoursMenu.set("9")
                    self.startMinutesMenu.set("00")
                    self.startAmPmMenu.set("AM")
                    self.endHoursMenu.set("10")
                    self.endMinutesMenu.set("00")
                    self.endAmPmMenu.set("AM")

            else:
                tkinter.messagebox.showwarning("Warning", "All course information must be filled out")

    def filterCourse(self):
        """

        :return:
        """
        option = self.filterOptionMenu.get()
        grep = Query()

        # Clear all the widgets/elements in the frame
        for element in self.courseFrame.winfo_children():
            element.destroy()

        # Generate all courses
        if option == "All":
            # Read contents of database, and populate our scrollable frame courseInputFrame
            database = self.db.all()
            # Make sure database isn't empty while we generate CourseClass objects
            if len(database) != 0:
                for courses in database:
                    courseFrame = CourseFrame(self, self.courseFrame, courses['name'], courses['number'],
                                              courses['instructor'],
                                              courses['location'], courses['credit'], courses['section'],
                                              courses['dayOfWeek'], courses['startTime'], courses['endTime'], self.db)
                    courseFrame.createUI()
                    # deletes the delete and edit button
                    courseFrame.deleteButton.grid_forget()
                    courseFrame.editButton.grid_forget()

        # Generate only courses with this specific instructor
        elif option == "Instructor":
            key = self.cleanText(self.filterEntry.get())
            id = self.db.search((grep.instructor == key))
            for courses in id:
                courseFrame = CourseFrame(self, self.courseFrame, courses['name'], courses['number'],
                                          courses['instructor'],
                                          courses['location'], courses['credit'], courses['section'],
                                          courses['dayOfWeek'], courses['startTime'], courses['endTime'], self.db)
                courseFrame.createUI()
                # deletes the delete and edit button
                courseFrame.deleteButton.grid_forget()
                courseFrame.editButton.grid_forget()
        # Generate only courses with this classroom
        elif option == "Classroom":
            key = self.cleanText(self.filterEntry.get())
            id = self.db.search((grep.location == key))
            for courses in id:
                courseFrame = CourseFrame(self, self.courseFrame, courses['name'], courses['number'],
                                          courses['instructor'],
                                          courses['location'], courses['credit'], courses['section'],
                                          courses['dayOfWeek'], courses['startTime'], courses['endTime'], self.db)
                courseFrame.createUI()
                # deletes the delete and edit button
                courseFrame.deleteButton.grid_forget()
                courseFrame.editButton.grid_forget()

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
        self.courseInputFrame = ctk.CTkScrollableFrame(self, width=400, height=200)
        self.courseInputFrame.grid(row=1, column=0, columnspan=3, padx=30, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.courseInputFrame)
        # ---------------------------------------------------------------
        #                          Buttons
        # ---------------------------------------------------------------

        # Create course list button
        courseListButton = ctk.CTkButton(self, text="Course List", command=self.listGUI)
        courseListButton.grid(row=0, column=2, padx=15, pady=5, sticky="EW")
        # self.mainGuiElements.append(courseListButton)  # Add to our list of elements so we can delete it

        # Weekly View button
        weeklyView = ctk.CTkButton(self, text="Weekly View", command=self.weeklyGui)
        weeklyView.grid(row=0, column=0, padx=15, pady=5, sticky="EW")
        # self.mainGuiElements.append(weeklyView)  # Add to our list of elements so we can delete it

        # Add course button
        addCourseButton = ctk.CTkButton(self, text="Add Course", command=self.saveCourse)
        addCourseButton.grid(row=5, column=2, padx=50, pady=5, sticky="EW")
        # self.mainGuiElements.append(addCourseButton)  # Add to our list of elements so we can delete it

        # ---------------------------------------------------------------
        #                         Entry Fields
        # ---------------------------------------------------------------

        # Course code entry
        self.codeEntry = ctk.CTkEntry(self, placeholder_text="Course Code*")
        self.codeEntry.grid(row=2, column=0, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.codeEntry)

        # Course name
        self.courseEntry = ctk.CTkEntry(self, placeholder_text="Course Name*")
        self.courseEntry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.courseEntry)

        # Course Section number
        self.courseSectionEntry = ctk.CTkEntry(self, placeholder_text="Section Number*")
        self.courseSectionEntry.grid(row=2, column=2, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.courseSectionEntry)

        # Course Credit
        self.creditEntry = ctk.CTkEntry(self, placeholder_text="Credit(s)*")
        self.creditEntry.grid(row=3, column=0, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.creditEntry)

        # Course meeting Location
        self.locationEntry = ctk.CTkEntry(self, placeholder_text="Location*")
        self.locationEntry.grid(row=3, column=1, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.locationEntry)

        # Course Instructor name
        self.instructorEntry = ctk.CTkEntry(self, placeholder_text="Instructor Name*")
        self.instructorEntry.grid(row=3, column=2, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.instructorEntry)

        # ---------------------------------------------------------------
        #                         Check Box
        # ---------------------------------------------------------------

        # Course day of the week check boxes
        # Frame for check boxes to get packed to
        self.checkBoxFrame = ctk.CTkFrame(self, width=400, height=30, fg_color="transparent")
        self.checkBoxFrame.grid(row=4, column=0, columnspan=3, rowspan=1, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxFrame)

        # Sunday
        self.checkBoxSunday = ctk.CTkCheckBox(self.checkBoxFrame, text="Sun")
        self.checkBoxSunday.grid(row=0, column=0, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxSunday)

        # Monday
        self.checkBoxMonday = ctk.CTkCheckBox(self.checkBoxFrame, text="Mon")
        self.checkBoxMonday.grid(row=0, column=1, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxMonday)

        # Tuesday
        self.checkBoxTuesday = ctk.CTkCheckBox(self.checkBoxFrame, text="Tue")
        self.checkBoxTuesday.grid(row=0, column=2, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxTuesday)

        # Wednesday
        self.checkBoxWednesday = ctk.CTkCheckBox(self.checkBoxFrame, text="Wed")
        self.checkBoxWednesday.grid(row=0, column=4, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxWednesday)

        # Thursday
        self.checkBoxThursday = ctk.CTkCheckBox(self.checkBoxFrame, text="Thu")
        self.checkBoxThursday.grid(row=0, column=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxThursday)

        # Friday
        self.checkBoxFriday = ctk.CTkCheckBox(self.checkBoxFrame, text="Fri")
        self.checkBoxFriday.grid(row=0, column=6, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxFriday)

        # Saturday
        self.checkBoxSaturday = ctk.CTkCheckBox(self.checkBoxFrame, text="Sat")
        self.checkBoxSaturday.grid(row=0, column=7, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.checkBoxSaturday)

        # ---------------------------------------------------------------
        #                         Option Menu
        # ---------------------------------------------------------------

        # ---------------------------------
        # Option Menu Lags Window, pls fix -NH
        # ---------------------------------
        # Frame to add the Start hours, minutes, and AM/PM option menus to
        self.startTimeFrame = ctk.CTkFrame(self, width=5, height=15, fg_color="transparent")
        self.startTimeFrame.grid(row=5, column=0, rowspan=1, sticky="EW")
        # self.mainGuiElements.append(self.startTimeFrame)

        # Start
        self.startLabel = ctk.CTkLabel(self.startTimeFrame, text="Start:")
        self.startLabel.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.startLabel)

        # Start Hours
        self.startHoursMenu = ctk.CTkOptionMenu(self.startTimeFrame, width=20, values=["1", "2", "3", "4", "5", "6",
                                                                                       "7", "8", "9", "10", "11", "12"])
        self.startHoursMenu.set("9")
        self.startHoursMenu.grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.startHoursMenu)

        # start: ":" for formatting
        self.startTimeLabel = ctk.CTkLabel(self.startTimeFrame, text=":")
        self.startTimeLabel.grid(row=0, column=2, sticky="EW")
        # self.mainGuiElements.append(self.startTimeLabel)

        # Start Minutes
        self.startMinutesMenu = ctk.CTkOptionMenu(self.startTimeFrame, width=20, values=["00", "05", "10", "15", "20",
                                                                                         "25", "30", "35", "40", "45",
                                                                                         "50", "55"])
        self.startMinutesMenu.grid(row=0, column=3, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.startMinutesMenu)

        # Start AM/PM
        self.startAmPmMenu = ctk.CTkOptionMenu(self.startTimeFrame, width=20, values=["AM", "PM"])
        self.startAmPmMenu.grid(row=0, column=4, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.startAmPmMenu)

        # Frame to add the End hours, minutes, and AM/PM option menus to
        self.endTimeFrame = ctk.CTkFrame(self, width=5, height=15, fg_color="transparent")
        self.endTimeFrame.grid(row=5, column=1, rowspan=1, sticky="EW")
        # self.mainGuiElements.append(self.endTimeFrame)

        # End
        self.endLabel = ctk.CTkLabel(self.endTimeFrame, text="End:")
        self.endLabel.grid(row=0, column=0, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.endLabel)

        # End Hours
        self.endHoursMenu = ctk.CTkOptionMenu(self.endTimeFrame, width=20, values=["1", "2", "3", "4", "5", "6", "7",
                                                                                   "8", "9", "10", "11", "12"])
        self.endHoursMenu.set("10")
        self.endHoursMenu.grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.endHoursMenu)

        # end: ":" for formatting
        self.endTimeLabel = ctk.CTkLabel(self.endTimeFrame, text=":")
        self.endTimeLabel.grid(row=0, column=2, sticky="EW")
        # self.mainGuiElements.append(self.endTimeLabel)

        # End Minutes
        self.endMinutesMenu = ctk.CTkOptionMenu(self.endTimeFrame, width=20, values=["00", "05", "10", "15", "20",
                                                                                     "25", "30", "35", "40", "45", "50",
                                                                                     "55"])
        self.endMinutesMenu.grid(row=0, column=3, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.endMinutesMenu)

        # End AM/PM
        self.endAmPmMenu = ctk.CTkOptionMenu(self.endTimeFrame, width=20, values=["AM", "PM"])
        self.endAmPmMenu.grid(row=0, column=4, padx=5, pady=5, sticky="EW")
        # self.mainGuiElements.append(self.endAmPmMenu)

        # ---------------------------------------------------------------
        #                         Generate Saved Courses
        # ---------------------------------------------------------------

        # Read contents of database, and populate our scrollable frame courseInputFrame
        database = self.db.all()

        # Make sure database isn't empty while we generate CourseClass objects
        if len(database) != 0:
            for courses in database:
                courseFrame = CourseFrame(self, self.courseInputFrame, courses['name'], courses['number'], courses['instructor'],
                                          courses['location'], courses['credit'], courses['section'],
                                          courses['dayOfWeek'], courses['startTime'], courses['endTime'], self.db)
                courseFrame.createUI()

    def weeklyGui(self):
        """
        Weekly Calendar view gui
        :return: None
        """
        # Remove the main gui widgets to make room for weekly view widgets
        self.removeMainGui()

        # Set our window mode to weekly view
        self.windowMode = 2

        self.geometry("900x700")
        self.title("Weekly View")

        # Specify Grid (Rows x Columns) for our buttons and labels
        # for i in range(0, 4):
        #     Grid.rowconfigure(self, i, weight=1)
        #     Grid.columnconfigure(self, i, weight=1)

        # Frame for weekly calendar view
        self.weeklyViewFrame = ctk.CTkScrollableFrame(self, width=800, height=600)
        self.weeklyViewFrame.grid(row=1, column=0)
        # self.weeklyGuiElements.append(self.weeklyViewFrame)

        # Add our widgets (change stuff here, this is just test code)
        self.randomButton = ctk.CTkButton(self, text="Course Input", command=self.backToMain)
        self.randomButton.grid(row=0, column=0, padx=0)
        # self.weeklyGuiElements.append(self.randomButton)

        # ---------------------------------------------------------------
        #                         Week Day Labels
        # ---------------------------------------------------------------

        # creating time labels
        daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        col = 1
        for day in daysOfWeek:
            dayLabel = ctk.CTkLabel(self.weeklyViewFrame, text=day)
            dayLabel.grid(row=0, column=col, padx=25)
            # self.weeklyGuiElements.append(dayLabel)
            col += 1

        # ---------------------------------------------------------------
        #                         Time Labels
        # ---------------------------------------------------------------

        rowIndex = 1
        minHeight = 0
        for hour in range(7, 22):
            printHour = hour
            hourRowIndex = hour - 6
            pm = "AM"
            if printHour > 11:
                pm = "PM"
            if printHour > 12:
                printHour -= 12
            hourText = f"{printHour}:00 {pm}"
            timeLabel = ctk.CTkLabel(self.weeklyViewFrame, text=hourText, height=1, anchor="n")
            timeLabel.grid(row=rowIndex, column=0, padx=5, pady=(0, 0))
            rowIndex += 1
            # self.weeklyGuiElements.append(timeLabel)

            minutesLabel = None
            if hour < 21:
                for i in range(3):
                    # 15 & 45 min intervals
                    text = "-"
                    # 30 min interval
                    if i == 1:
                        text = "—"
                    minutesLabel = ctk.CTkLabel(self.weeklyViewFrame, text=text, height=1, anchor="n")
                    # starts minutes on the row after the hour row
                    minutesLabel.grid(row=rowIndex, column=0, padx=5, pady=(0, 0))
                    rowIndex += 1
                    # self.weeklyGuiElements.append(minutesLabel)
                    # get the height of text
                    if minHeight == 0:
                        minutesLabel.update()
                        minHeight = minutesLabel.winfo_height()

        # ---------------------------------------------------------------
        #                         Course Frames
        # ---------------------------------------------------------------
        courses = self.getCourses()
        for course in courses:
            startRow = int(((course["start"] - 7) / .25) + 1)
            # Increases by 15 min intervals. Inbetween numbers will round down.
            span = int((course["end"] - course["start"]) / .25)
            for day in range(len(course["days"])):
                if course["days"][day] == 1:
                    # frame being placed on calendar
                    courseFrame = ctk.CTkFrame(self.weeklyViewFrame, width=60, height=(minHeight*span),
                                               fg_color="#04AA6D")
                    # TODO: is span+1 right? might be span
                    courseFrame.grid(row=startRow, column=day+1, rowspan=span+1, padx=25)
                    # self.weeklyGuiElements.append(courseFrame)

                    # text going over the courses frame
                    codeText = f"{course['code']}-{course['section']}"
                    CourseCodeLabel = ctk.CTkLabel(courseFrame, text=codeText, wraplength=50, font=("Arial", 10))
                    CourseCodeLabel.pack(expand=True, anchor=ctk.CENTER)
                    # locks the Frame size, so label does not take over the frame size
                    courseFrame.pack_propagate(False)
                    # self.weeklyGuiElements.append(CourseCodeLabel)

    def listGUI(self):
        """
        Course list GUI
        :return: None
        """

        # Remove all Course Input widgets
        self.removeMainGui()

        # Set window mode to main gui
        self.windowMode = 1
        self.title("Course List")

        # ---------------------------------------------------------------
        #                         Frames
        # ---------------------------------------------------------------

        self.courseFrame = ctk.CTkScrollableFrame(self, width=400, height=350)
        self.courseFrame.grid(row=1, column=0, columnspan=4, padx=30, pady=5, sticky="EW")
        # self.listGuiElements.append(self.courseFrame)

        # ---------------------------------------------------------------
        #                         Options menu
        # ---------------------------------------------------------------

        self.filterOptionMenu = ctk.CTkOptionMenu(self, values=["All", "Instructor", "Classroom"])
        self.filterOptionMenu.grid(row=0, column=1)
        # self.listGuiElements.append(self.filterOptionMenu)

        # ---------------------------------------------------------------
        #                         Entries
        # ---------------------------------------------------------------

        self.filterEntry = ctk.CTkEntry(self, placeholder_text="Instructor/Classroom")
        self.filterEntry.grid(row=0, column=2)
        # self.listGuiElements.append(self.filterEntry)

        # ---------------------------------------------------------------
        #                         Buttons
        # ---------------------------------------------------------------

        self.courseInputButton = ctk.CTkButton(self, text="Course Input", command=self.backToMain)
        self.courseInputButton.grid(row=0, column=0)
        # self.listGuiElements.append(self.courseInputButton)

        self.filterButton = ctk.CTkButton(self, text="Filter", command=self.filterCourse)
        self.filterButton.grid(row=0, column=3)
        # self.listGuiElements.append(self.filterButton)

    def getCourses(self) -> list:

        # Read contents of database, and populate our scrollable frame courseInputFrame
        database = self.db.all()

        coursesList = []

        if len(database) != 0:
            for courses in database:
                courseInfo = {"code": courses['number'], "section": courses['section'], "start": courses['startTime'],
                              "end": courses['endTime'], "days": courses['dayOfWeek']}
                coursesList.append(courseInfo)

        return coursesList

    def removeMainGui(self):
        """
        Removes elements on course input to allow new elements to populate
        :return: None
        """
        # Causes memory leak
        # for element in self.mainGuiElements:
        #     element.grid_forget()

        for element in self.winfo_children():
            element.destroy()

    def removeListGui(self):
        """
        Removes elements on course list to allow new elements to populate
        :return: None
        """
        # reset window title
        self.title("Course Scheduler")

        # Causes memory leak
        # for element in self.listGuiElements:
        #     element.grid_forget()

        for element in self.winfo_children():
            element.destroy()

    def removeWeeklyGui(self):
        """
        Removes elements on weekly calendar view to allow new elements to populate
        :return: None
        """
        # reset window size & title
        self.geometry("700x450")
        self.title("Course Scheduler")

        # Causes memory leak
        # for element in self.weeklyGuiElements:
        #     element.grid_forget()

        for element in self.winfo_children():
            element.destroy()

    def backToMain(self):
        """
        Called when we want to move our frame back to the main gui frame.
        :return: None
        """
        # Window mode set to main, reset our list of widgets
        if self.windowMode == 0:
            self.removeMainGui()
            # self.mainGuiElements = []

        # Window mode set to list, reset our list of widgets
        elif self.windowMode == 1:
            self.removeListGui()
            # self.listGuiElements = []

        # Window mode set to weekly view, reset our list of widgets
        elif self.windowMode == 2:
            self.removeWeeklyGui()
            # self.weeklyGuiElements = []

        # Return to the main gui
        self.courseInputGUI()


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    # Check if its windows or macos
    try:
        sys.getwindowsversion()
    except AttributeError:
        isWindows = False
    else:
        isWindows = True

    # Grab our process id from os
    p = psutil.Process(os.getpid())
    if isWindows:
        # Set pid priority to high
        p.nice(psutil.HIGH_PRIORITY_CLASS)
    else:
        # Set pid to 10
        p.nice(10)
    main()
