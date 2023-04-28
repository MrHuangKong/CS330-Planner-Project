# Devin Zeller & Nicolas Huang
# CS330 - Software Engineering Project
# Course Class
# ----------------------------------------------------------------------------------------------------------------------

import tkinter
import tkinter.messagebox

import customtkinter as ctk
from tkinter import *
from tinydb import TinyDB, Query, where


class CourseFrame(ctk.CTk):

    def __init__(self, rootFrame, containingFrame, courseName: str, courseCode: str, instructorName: str, location: str, courseCredits: str,
                sectionNumber: str, daysOfWeek: list, startTime: float, endTime: float, database: TinyDB):

        self.root = rootFrame
        self.containingFrame = containingFrame
        self.courseName = courseName
        self.courseCode = courseCode
        self.instructorName = instructorName
        self.location = location
        self.credits = courseCredits
        self.sectionNumber = sectionNumber
        self.daysOfWeek = daysOfWeek
        self.startTime = startTime
        self.endTime = endTime

        self.courseNameLabel = None
        self.instructorNameLabel = None
        self.creditsLabel = None
        self.courseCodeLabel = None
        self.meetingTimeLabel = None
        self.daysOfWeekLabel = None
        self.instructorLabel = None
        self.sectionNumberLabel = None
        self.deleteButton = None
        self.editButton = None

        # Point to the database to allow deleting and modifying
        self.database = database

    def decimalTimeToStardardTime(self, decimalTime: float) -> str:
        """
        turns time form decimal form into starndard form
        :param decimalTime: 12.50 = 12:30 PM
        :return: start form of decimalTime
        """
        hours = int(decimalTime)
        minutes = int((decimalTime - hours) * 60)
        if hours >= 12:
            amPm = "PM"
        else:
            amPm = "AM"
        if hours == 0:
            hours = 12
        elif hours > 12:
            hours -= 12
        time = "{:02d}:{:02d} {}".format(hours, minutes, amPm)
        return time

    def createUI(self):
        """
        creates a frame that holds labels with all the course information
        :return: None
        """
        self.frame = ctk.CTkFrame(
            self.containingFrame,
            width=500,
            height=50,
            fg_color=("#B7B7B7", "#73726f"))
        self.frame.pack(padx=10, pady=10)

        # adding course name to frame
        self.courseNameLabel = ctk.CTkLabel(
            self.frame,
            text=self.courseName)
        self.courseNameLabel.grid(row=0, column=1, padx=10)

        # adding instructor name to frame
        self.instructorNameLabel = ctk.CTkLabel(
            self.frame,
            text=f"Instructor: {self.instructorName}")
        self.instructorNameLabel.grid(row=0, column=3, padx=10)

        # adding credits to frame
        self.creditsLabel = ctk.CTkLabel(
            self.frame,
            text=f"Credit(s): {self.credits}")
        self.creditsLabel.grid(row=1, column=0, padx=10)

        # adding course code to frame
        self.courseCodeLabel = ctk.CTkLabel(
            self.frame,
            text=self.courseCode)
        self.courseCodeLabel.grid(row=0, column=0, padx=10)

        # reading day of the week list and converting to a string
        daysInAWeek = ["S", "M", "T", "W", "Th", "F", "S"]
        classDays = ""
        for day in range(len(self.daysOfWeek)):
            if self.daysOfWeek[day] == 1:
                if len(classDays) == 0:
                    classDays = daysInAWeek[day]
                else:
                    classDays += f"/{daysInAWeek[day]}"

        # adding days of week to frame
        self.daysOfWeekLabel = ctk.CTkLabel(
            self.frame,
            text=classDays)
        self.daysOfWeekLabel.grid(row=1, column=1, padx=10)

        # make str of start-end time
        startTime = self.decimalTimeToStardardTime(self.startTime)
        endTime = self.decimalTimeToStardardTime(self.endTime)
        startEndTime = f"{startTime}-{endTime}"

        # adding meeting time to frame
        self.meetingTimeLabel = ctk.CTkLabel(
            self.frame,
            text=startEndTime)
        self.meetingTimeLabel.grid(row=1, column=2, padx=10)

        # adding section number to frame
        self.sectionNumberLabel = ctk.CTkLabel(
            self.frame,
            text=f"Section: {self.sectionNumber}")
        self.sectionNumberLabel.grid(row=0, column=2, padx=5, pady=5)

        # adding location to frame
        self.instructorLabel = ctk.CTkLabel(
            self.frame,
            text=f"Room: {self.location}")
        self.instructorLabel.grid(row=1, column=3, padx=10)

        # adding delete button to frame
        self.deleteButton = ctk.CTkButton(
            self.frame,
            text="❌",
            font=("Arial", 10),
            text_color=("#000000", "#f2f2f2"),
            width=30,
            border_width=1,
            border_color=("#cccccc", "#9b9a97"),
            fg_color=("#DBDBDB", "#8f8d8a"),
            command=self.deleteEntryDB)
        self.deleteButton.grid(row=0, column=4, padx=5, pady=5)

        # Commenting the below out, and placing it inside our courseInput to allow callback database values
        # adding edit button to frame
        self.editButton = ctk.CTkButton(
            self.frame,
            text="✎",
            font=("Arial", 10),
            text_color=("#000000", "#f2f2f2"),
            width=30,
            border_width=1,
            border_color=("#cccccc", "#9b9a97"),
            fg_color=("#DBDBDB", "#8f8d8a"),
            command=self.editEntryDB)
        self.editButton.grid(row=1, column=4, padx=5, pady=5)

    def editEntryDB(self):
        # Set root into edit mode
        self.root.editMode = True

        # Find the match in the database, and store it into self.docID
        grep = Query()
        id = self.database.get((grep.number == self.courseCode) & (grep.name == self.courseName)
                             & (grep.section == self.sectionNumber))
        self.root.docID = id

        # Populate entries with whats stored in frame
        # Course Code
        self.root.codeEntry.delete(0, ctk.END)
        self.root.codeEntry.insert(0, f"{self.courseCode}")
        # Course Name
        self.root.courseEntry.delete(0, ctk.END)
        self.root.courseEntry.insert(0, f"{self.courseName}")
        # Section Number
        self.root.courseSectionEntry.delete(0, ctk.END)
        self.root.courseSectionEntry.insert(0, f"{self.sectionNumber}")
        # Credits
        self.root.creditEntry.delete(0, ctk.END)
        self.root.creditEntry.insert(0, f"{self.credits}")
        # Location
        self.root.locationEntry.delete(0, ctk.END)
        self.root.locationEntry.insert(0, f"{self.location}")
        # Instructor Name
        self.root.instructorEntry.delete(0, ctk.END)
        self.root.instructorEntry.insert(0, f"{self.instructorName}")

        # Days of Week
        self.root.checkBoxSunday.deselect()
        if self.daysOfWeek[0]:
            self.root.checkBoxSunday.select()
        self.root.checkBoxMonday.deselect()
        if self.daysOfWeek[1]:
            self.root.checkBoxMonday.select()
        self.root.checkBoxTuesday.deselect()
        if self.daysOfWeek[2]:
            self.root.checkBoxTuesday.select()
        self.root.checkBoxWednesday.deselect()
        if self.daysOfWeek[3]:
            self.root.checkBoxWednesday.select()
        self.root.checkBoxThursday.deselect()
        if self.daysOfWeek[4]:
            self.root.checkBoxThursday.select()
        self.root.checkBoxFriday.deselect()
        if self.daysOfWeek[5]:
            self.root.checkBoxFriday.select()
        self.root.checkBoxSaturday.deselect()
        if self.daysOfWeek[6]:
            self.root.checkBoxSaturday.select()

        # Start time
        s = self.decimalTimeToStardardTime(self.startTime)
        self.root.startHoursMenu.set(f"{s[:2]}")
        self.root.startMinutesMenu.set(f"{s[3:5]}")
        self.root.startAmPmMenu.set(f"{s[6:]}")

        # End time
        e = self.decimalTimeToStardardTime(self.endTime)
        self.root.endHoursMenu.set(f"{e[:2]}")
        self.root.endMinutesMenu.set(f"{e[3:5]}")
        self.root.endAmPmMenu.set(f"{e[6:]}")


    def deleteEntryDB(self):
        """
        Deletes the course from GUI and Database
        :return:
        """
        # Create a query instance when called
        grep = Query()

        # Find the match in the database, and delete it
        self.database.remove((grep.number == self.courseCode) & (grep.name == self.courseName)
                             & (grep.section == self.sectionNumber))

        # Remove from parent frame to show user deleted the course
        self.frame.destroy()

