# Devin Zeller & Nicolas Huang
# CS330 - Software Engineering Project
# Course Class
# ----------------------------------------------------------------------------------------------------------------------

import tkinter
import tkinter.messagebox

import customtkinter as ctk
from tkinter import *
from tinydb import TinyDB, Query


class CourseFrame(ctk.CTk):

    def __int__(self, containingFrame, courseName: str, courseCode: str, instructorName: str, location: str, courseCredits: str,
                sectionNumber: str, daysOfWeek: list, startTime: float, endTime: float):
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
        self.deleteButton = None
        self.editButton = None

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
        self.frame = ctk.CTkFrame(
            self.containingFrame,
            width=380,
            height=50,
            fg_color="#73726f")
        self.frame.pack(padx=10, pady=10)

        # adding course name to frame
        self.courseNameLabel = ctk.CTkLabel(
            self.frame,
            text=self.courseName)
        self.courseNameLabel.grid(row=0, column=0, padx=10)

        # adding instructor name to frame
        self.insrtuctorNameLabel = ctk.CTkLabel(
            self.frame,
            text=self.instructorName)
        self.instructorNameLabel.grid(row=0, column=1, padx=10)

        # adding credits to frame
        self.creditsLabel = ctk.CTkLabel(
            self.frame,
            text=self.credits)
        self.creditsLabel.grid(row=0, column=2, padx=10)

        # adding course code to frame
        self.courseCodeLabel = ctk.CTkLabel(
            self.frame,
            text=self.courseCode)
        self.courseCodeLabel.grid(row=1, column=0, padx=10)

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
            self,
            text=startEndTime)
        self.meetingTimeLabel.grid(row=1, column=2, padx=10)

        self.deleteButton = ctk.CTkButton(
            self.frame,
            text="🗑",
            width=30)
        self.deleteButton.grid(row=0, column=3, padx=5, pady=5)

        self.editButton = ctk.CTkButton(
            self.frame,
            text="✎",
            width=30)
        self.editButton.grid(row=1, column=3, padx=5, pady=5)
        