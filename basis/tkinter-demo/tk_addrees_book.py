import pickle
import os.path
from tkinter import *
import tkinter.messagebox


class Address:
    def __init__(self, name, street, city, state, zip):
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip


class AddressBook:
    def __init__(self):
        window = Tk()
        window.title("Address Book")
        self.nameVar = StringVar()
        self.streetVar = StringVar()
        self.cityVar = StringVar()
        self.stateVar = StringVar()
        self.zipVar = StringVar()

        frame1 = Frame(window)
        frame1.pack()
        Label(frame1, text = "Name").grid(row = 1, column = 1, sticky = W)
        Entry(frame1, textvariable = self.nameVar, width = 40).grid(row = 1, column = 2)

        frame2 = Frame(window)
        frame2.pack()
        Label(frame2, text = "Street").grid(row = 1, column = 1, sticky = W)
        Entry(frame2, textvariable = self.streetVar, width = 40).grid(row = 1, column = 2)

        frame3 = Frame(window)
        frame3.pack()
        Label(frame3, text = "City").grid(row = 1, column = 1, sticky = W)
        Entry(frame3, textvariable = self.cityVar, width = 40).grid(row=  1, column = 2)
        Label(frame3, text = "State").grid(row = 1, column = 3, sticky = W)
        Entry(frame3, textvariable = self.stateVar, width = 5).grid(row=  1, column = 4)
        Label(frame3, text = "Zip").grid(row = 1, column = 5, sticky = W)
        Entry(frame3, textvariable = self.zipVar, width = 5).grid(row =  1, column = 6)

        frame4 = Frame(window)
        frame4.pack()
        Button(frame4, text = "Add", command = self.processAdd).grid(row = 1, column = 1)
        btFirst = Button(frame4, text = "First", command = self.processFirst).grid(row = 1, column = 2)
        btNext = Button(frame4, text = "Next", command = self.processNext).grid(row = 1, column = 3)
        btPrevious = Button(frame4, text = "Previous", command = self.processPrevious).grid(row = 1, column = 4)
        btLast = Button(frame4, text = "Last", command = self.processLast).grid(row = 1, column = 5)

        self.addressList = self.loadAddress()
        self.current = 0

        if len(self.addressList) > 0:
            self.setAddree()

        window.mainloop()

    def saveAdress(self):
        outfile = open("address.dat", 'wb')
        pickle.dump(self.addressList, outfile)
        tkinter.messagebox.showinfo("Address saved", "A new address is saved")
        outfile.close()

    def loadAddress(self):
        if not os.path.isfile("address.dat"):
            return []
        try:
            infile = open("address.dat", "rb")
            addressList = pickle.load()
        except:
            addressList = []
        return addressList

    def processAdd(self):
        # put a object into address
        address = Address(self.nameVar.get(),
                          self.streetVar.get(), self.cityVar.get(),
                          self.stateVar.get(), self.zipVar.get())
        self.addressList.append(address)
        self.saveAdress()

    def processFirst(self):
        self.current = 0
        self.setAddress()

    def processNext(self):
        if self.current < len(self.addressList) - 1:
            self.current += 1
            self.setAddress()

    def processPrevious(self):
        if self.current > 0:
            self.current -= 1
            self.setAddress()

    def processLast(self):
        self.current = len(self.addressList) - 1
        self.setAddress()

    def setAddress(self):
        self.nameVar.set(self.addressList[self.current].name)
        self.stateVar.set(self.addressList[self.current].state)
        self.streetVar.set(self.addressList[self.current].street)
        self.cityVar.set(self.addressList[self.current].city)
        self.zipVar.set(self.addressList[self.current].zip)

if __name__ == '__main__':
    AddressBook()
