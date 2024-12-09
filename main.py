from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con
from utils import *

ui, _  = loadUiType('ValetTracker.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0) #sets the home page the first to pop up
        self.btn_Create_New_Entry.clicked.connect(self.show_add_new_entry) #calls show_add_new_entry function to opens the new entry page and increment the id
        self.btn_Raw_Data.clicked.connect(lambda: self.tabWidget.setCurrentIndex(3)) #navigates to the calculated stats page 
        #self.btn_TBD.clicked.connect(lambda: self.tabWidget.setCurrentIndex(3)) #navigates to the TBD page that will be set up later
         
        self.btn_My_Stats.clicked.connect(self.show_calc_data)
        self.btn_save_changes.clicked.connect(self.save_entry) #button that commits the entries to database in the new entry page
        self.btn_Raw_Data.clicked.connect(self.show_raw_data)

    def show_add_new_entry(self): #add new entry
        self.tabWidget.setCurrentIndex(1) #page position
        self.fill_next_id() #calls method below

    def fill_next_id(self): #function to auto fill the id and autoincrement it to the next id
        try:
            id = 0 #id number
            mydb = con.connect(host = "localhost", user = "root",password = "", db = "valettracker") #Connects to sql database
            cursor = mydb.cursor()
            cursor.execute("select * from entries") #calls entire entries database
            result = cursor.fetchall() #fetch all lines
            if result:
                for ent in result: #for each line in database
                    id += 1 #add one to keep unique key
            self.textBrowser_id.setText(str(id + 1)) 
        except con.Error as e:
            print(f"Database connection error: {e}")
            QMessageBox.critical(self, "Database Error", f"Error connecting to the database: {e}")

    def save_entry(self): #function to save the entry when the button is hit on the new entry page
        try:
            mydb = con.connect(host = "localhost", user = "root",password = "", db = "valettracker") #Connects to sql database
            cursor = mydb.cursor()
            # Retrieve input from the user interface in all text input boxes
            date= self.lineEdit_Date.text()
            Total_tips_earned= self.lineEdit_Total_tips_earned.text()
            valets_on_duty= self.lineEdit_Valets_on_duty.text()
            duration= self.lineEdit_Duration.text()
            cars_parked= self.lineEdit_Cars_parked.text()
            TBD_1= self.lineEdit_TBD_1.text()
            TBD_2= self.lineEdit_TBD_2.text()

            # SQL query for inserting data
            query = """
            INSERT INTO entries (date, Total_tips_earned, valets_on_duty, duration, cars_parked, TBD_1, TBD_2)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (date, Total_tips_earned, valets_on_duty, duration, cars_parked, TBD_1, TBD_2)

            # Execute the query
            cursor.execute(query, values)
            mydb.commit()  # Commit the transaction

            QMessageBox.information(self, "Success", "Entry saved successfully!") #message box successful

            self.lineEdit_Date.setText("")      #resets all text boxes back empty  once entry saved
            self.lineEdit_Total_tips_earned.setText("")
            self.lineEdit_Valets_on_duty.setText("")
            self.lineEdit_Duration.setText("")
            self.lineEdit_Cars_parked.setText("")
            self.lineEdit_TBD_1.setText("")
            self.lineEdit_TBD_2.setText("")

            self.tabWidget.setCurrentIndex(0) #changes the page back to the home page


        except con.Error as err: #all error messages
            QMessageBox.critical(self, "Database Error", f"Could not save entry: {err}")
            print(f"SQL Error: {err}")
        except ValueError as ve:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {ve}")
            print(f"Input Error: {ve}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            print(f"Error details: {e}")

    def show_calc_data(self): #show calc data page
        self.tabWidget.setCurrentIndex(2) #page position

        self.textBrowser_Total_Tips_recieved.setText(str(calc_data_tips()))   #output of calc_data_tips to the button

        self.textBrowser_Average_tips_per_shift.setText(str(calc_avg_tips()))  #output of calc_avg_tips to the button

        self.textBrowser_Average_tips_per_hr.setText(str(calc_tips_per_hr()))   #output of calc_tips_per_hr to the button

        self.textBrowser_Total_hours_worked.setText(str(calc_total_hours_worked()))  #output of duration to the button

        self.textBrowser_Total_cars_parked.setText(str(calc_cars_parked()))  #output of cars_parked to the button

        self.textBrowser_Cars_per_hour.setText(str(calc_cars_per_hour()))  #output of cars_parked to the button

    #function to print the raw data in a good format so the user can view, delete(by id,error message if invalid id) and maybe edit
    def show_raw_data(self):
        self.tabWidget.setCurrentIndex(3) #page position to raw data


#change the navigation system so the top menu works, and hide menu above instead of the buttons 
# redo the main page layout so its not buttons and an inviting info page
# translate the sql to slqlite so it can be deployed as a local application

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

