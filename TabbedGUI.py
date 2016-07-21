from tkinter import *
import ECMath
from EllipticCurve import EllipticCurve
from Point import Point
from Polynomial import Polynomial
from PolynomialPoint import PolynomialPoint
from BinaryEllipticCurve import BinaryEllipticCurve
from random import randint

__author__ = 'Aaron Blumenfeld'

# Tabbed GUI originally written by Sunjay Varma, modified by me

BASE = RAISED
SELECTED = FLAT


class Tab(Frame):

    def __init__(self, master, name):
        Frame.__init__(self, master)
        self._tabName = name


class PrimeTab(Tab):

    def __init__(self, master, name):
        Tab.__init__(self, master, name)

        self.a = 64379 # initially E : y^2 = x^3 + 64379x + 22921 (mod 71933)
        self.b = 22921
        self.p = 71933
        self.Gx = 25598 # initially G = (25598, 32444)
        self.Gy = 32444
        self.Px = 50889 # initially P = (50889, 7921)
        self.Py = 7921
        self.Qx = 43091 # initially Q = (43091, 34892)
        self.Qy = 34892
        self.k = 2016 # initially k = 2016
        self.n = 5 # initially n = 5 random curves
        self.m = 10 # initially m = 10 random points

        outputFrame = Frame(self)
        Button(outputFrame, text="Clear Output", bg="blue", fg="white", command=(lambda: self.clear()), borderwidth=1).pack(side=BOTTOM, pady=3)
        self._output = Text(outputFrame, height=15, width=60)
        self._output.pack(side=LEFT, pady=3)
        scrollbar = Scrollbar(outputFrame)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self._output.yview)

        ecInfo = Frame(self)
        ptsInfo = Frame(self)
        arithmeticFrame = Frame(self)
        orderFrame = Frame(self)
        listFrame = Frame(self)
        ptsFrame = Frame(self)

        Label(ecInfo, text="E : y^2 = x^3 + ", bg="orange", fg="black", borderwidth=1).grid(row=1,column=1)
        self._a = Entry(ecInfo, width = 6)
        self._a.insert(0, self.a)
        self._a.bind("<Return>", (lambda event: self.changeA()))
        self._a.grid(row=1, column=2)
        Label(ecInfo, text="x + ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=3)
        self._b = Entry(ecInfo, width=6)
        self._b.insert(0, self.b)
        self._b.bind("<Return>", (lambda event: self.changeB()))
        self._b.grid(row=1, column=4)
        Label(ecInfo, text=" (mod ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=5)
        self._p = Entry(ecInfo, width=6)
        self._p.insert(0, self.p)
        self._p.bind("<Return>", (lambda event: self.changePrime()))
        self._p.grid(row=1, column=6)
        Label(ecInfo, text="), Generator G = (", bg="orange", fg="black", borderwidth=1).grid(row=1, column=7)
        self._Gx = Entry(ecInfo, width=6)
        self._Gx.insert(0, self.Gx)
        self._Gx.bind("<Return>", (lambda event: self.changeG()))
        self._Gx.grid(row=1, column=8)
        Label(ecInfo, text=", ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=9)
        self._Gy = Entry(ecInfo, width=6)
        self._Gy.insert(0, self.Gy)
        self._Gy.bind("<Return>", (lambda event: self.changeG()))
        self._Gy.grid(row=1, column=10)
        Label(ecInfo, text=")", bg="orange", fg="black", borderwidth=1).grid(row=1, column=11)

        Label(ptsInfo, text="P = (", bg="blue", fg="white", borderwidth=1).grid(row=1, column=1, pady=3)
        self._Px = Entry(ptsInfo, width=6)
        self._Px.insert(0, self.Px)
        self._Px.bind("<Return>", (lambda event: self.changeP()))
        self._Px.grid(row=1, column=2, pady=3)
        Label(ptsInfo, text=", ", bg="blue", fg="white", borderwidth=1).grid(row=1, column=3, pady=3)
        self._Py = Entry(ptsInfo, width=6)
        self._Py.insert(0, self.Py)
        self._Py.bind("<Return>", (lambda event: self.changeP()))
        self._Py.grid(row=1, column=4, pady=3)
        Label(ptsInfo, text="), Q = (", bg = "blue", fg = "white", borderwidth=1).grid(row=1, column=5, pady=3)
        self._Qx = Entry(ptsInfo, width=6)
        self._Qx.insert(0, self.Qx)
        self._Qx.bind("<Return>", (lambda event: self.changeQ()))
        self._Qx.grid(row=1, column=6, pady=3)
        Label(ptsInfo, text=", ", bg="blue", fg="white", borderwidth=1).grid(row=1, column=7)
        self._Qy = Entry(ptsInfo, width=6)
        self._Qy.insert(0, self.Qy)
        self._Qy.bind("<Return>", (lambda event: self.changeQ()))
        self._Qy.grid(row=1, column=8, pady=3)
        Label(ptsInfo, text="), k = ", bg="blue", fg="white", borderwidth=1).grid(row=1, column=9, pady=3)
        self._k = Entry(ptsInfo, width=6)
        self._k.insert(0, self.k)
        self._k.bind("<Return>", (lambda event: self.changeK()))
        self._k.grid(row=1, column=10, pady=3)

        Button(arithmeticFrame, text="P + Q", bg="blue", fg="white", command=(lambda: self.add())).grid(row=1, column=1, padx=5, pady=3)
        Button(arithmeticFrame, text="kP", bg="blue", fg="white", command=(lambda: self.mult())).grid(row=1, column=2, padx=5, pady=3)
        Button(arithmeticFrame, text="log_G(P)", bg="blue", fg="white", command=(lambda: self.log())).grid(row=1, column=3, padx=5, pady=3)

        Button(orderFrame, text="Order(E)", bg="blue", fg="white", command=(lambda: self.order())).grid(row=1, column=1, padx=5, pady=3)
        Button(orderFrame, text="Order(G)", bg="blue", fg="white", command=(lambda: self.pointOrder())).grid(row=1, column=2, padx=5, pady=3)

        Label(listFrame, text="Generate ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._n = Entry(listFrame, width=3)
        self._n.insert(0, self.n)
        self._n.bind("<Return>", (lambda event: self.changeN()))
        self._n.grid(row=1, column=2, pady=3)
        Button(listFrame, text="Random ECs", bg="orange", fg="black", command=(lambda: self.randomECs())).grid(row=1, column=3, padx=5, pady=3)
        Button(listFrame, text="Random ECs of prime order", bg="orange", fg="black", command=(lambda: self.randomPrimeECs())).grid(row=1, column=4, padx=5, pady=3)

        Label(ptsFrame, text="List ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._m = Entry(ptsFrame, width=3)
        self._m.insert(0, self.m)
        self._m.bind("<Return>", (lambda event: self.changeM()))
        self._m.grid(row=1, column=2, pady=3)
        Button(ptsFrame, text="Random points on E", bg="orange", fg="black", command=(lambda: self.randomPoints())).grid(row=1, column=3, padx=5, pady=3)

        ecInfo.pack(side=TOP)
        ptsInfo.pack(side=TOP)
        arithmeticFrame.pack(side=TOP)
        orderFrame.pack(side=TOP)
        listFrame.pack(side=TOP)
        ptsFrame.pack(side=TOP)
        outputFrame.pack(side=BOTTOM)

    def changeA(self):
        try:
            self.a = int(self._a.get()) % self.p
            self._a.delete(0, END)
            self._a.insert(0, self.a)
            E = EllipticCurve(self.a, self.b, self.p)
            self._output.insert(END, str(E) + "\n")
        except ValueError:
            self._a.delete(0, END)
            self._a.insert(0, self.a)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeB(self):
        try:
            self.b = int(self._b.get()) % self.p
            self._b.delete(0, END)
            self._b.insert(0, self.b)
            E = EllipticCurve(self.a, self.b, self.p)
            self._output.insert(END, str(E) + "\n")
        except ValueError:
            self._b.delete(0, END)
            self._b.insert(0, self.b)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changePrime(self):
        try:
            temp = int(self._p.get())
            if not ECMath.isPrime(temp):
                self._output.insert(END, str(temp) + " is not prime. Please try again.\n")
                self._p.delete(0, END)
                self._p.insert(0, self.p)
            else:
                self.p = temp
                E = EllipticCurve(self.a, self.b, self.p)
                self._output.insert(END, str(E) + "\n")
        except ValueError:
            self._p.delete(0, END)
            self._p.insert(0, self.p)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeG(self):
        try:
            self.Gx = int(self._Gx.get())
            self.Gy = int(self._Gy.get())
            self._Gx.delete(0, END)
            self._Gy.delete(0, END)
            self._Gx.insert(0, self.Gx)
            self._Gy.insert(0, self.Gy)
            self._output.insert(END, "G = " + str(Point(self.Gx, self.Gy, 1)) + "\n")
        except ValueError:
            self._Gx.delete(0, END)
            self._Gy.delete(0, END)
            self._Gx.insert(0, self.Gx)
            self._Gy.insert(0, self.Gy)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeP(self):
        try:
            self.Px = int(self._Px.get())
            self.Py = int(self._Py.get())
            self._Px.delete(0, END)
            self._Py.delete(0, END)
            self._Px.insert(0, self.Px)
            self._Py.insert(0, self.Py)
            self._output.insert(END, "P = " + str(Point(self.Px, self.Py, 1)) + "\n")
        except ValueError:
            self._Px.delete(0, END)
            self._Py.delete(0, END)
            self._Px.insert(0, self.Px)
            self._Py.insert(0, self.Py)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeQ(self):
        try:
            self.Qx = int(self._Qx.get())
            self.Qy = int(self._Qy.get())
            self._Qx.delete(0, END)
            self._Qy.delete(0, END)
            self._Qx.insert(0, self.Qx)
            self._Qy.insert(0, self.Qy)
            self._output.insert(END, "Q = " + str(Point(self.Qx, self.Qy, 1)) + "\n")
        except ValueError:
            self._Qx.delete(0, END)
            self._Qy.delete(0, END)
            self._Qx.insert(0, self.Qx)
            self._Qy.insert(0, self.Qy)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeK(self):
        try:
            self.k = int(self._k.get())
            self._k.delete(0, END)
            self._k.insert(0, self.k)
            self._output.insert(END, "k = " + str(self.k) + "\n")
        except ValueError:
            self._k.delete(0, END)
            self._k.insert(0, self.k)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeN(self):
        try:
            self.n = int(self._n.get())
            self._n.delete(0, END)
            self._n.insert(0, self.n)
            self._output.insert(END, "Random curve selection will now generate " + str(self.n) + " curve")
            if self.n != 1:
                self._output.insert(END, "s")
            self._output.insert(END, ".\n")
        except ValueError:
            self._n.delete(0, END)
            self._n.insert(0, self.n)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeM(self):
        try:
            self.m = int(self._m.get())
            self._m.delete(0, END)
            self._m.insert(0, self.m)
            self._output.insert(END, "Random point selection will now generate " + str(self.m) + " point")
            if self.m != 1:
                self._output.insert(END, "s")
            self._output.insert(END, ".\n")
        except ValueError:
            self._m.delete(0, END)
            self._m.insert(0, self.m)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def add(self):
        P = Point(self.Px, self.Py, 1)
        Q = Point(self.Qx, self.Qy, 1)
        R = P.add(Q, self.a, self.b, self.p)
        self._output.insert(END, str(P) + " + " + str(Q) + " = " + str(R) + "\n")

    def mult(self):
        P = Point(self.Px, self.Py, 1)
        R = P.mult(self.k, self.a, self.b, self.p)
        self._output.insert(END, str(self.k) + str(P) + " = " + str(R) + "\n")

    def log(self):
        E = EllipticCurve(self.a, self.b, self.p)
        P = Point(self.Px, self.Py, 1)
        G = Point(self.Gx, self.Gy, 1)
        R = E.log(P, G)
        self._output.insert(END, "log_G" + str(P) + " = " + str(R) + "\n")

    def order(self):
        order = EllipticCurve(self.a, self.b, self.p).order()
        self._output.insert(END, "|E| = " + str(order) + "\n")

    def pointOrder(self):
        order = EllipticCurve(self.a, self.b, self.p).pointOrder(Point(self.Gx, self.Gy, 1))
        self._output.insert(END, "|G| = " + str(order) + "\n")

    def randomECs(self):
        s = EllipticCurve.listRandomECs(self.n, self.p)
        self._output.insert(END, s + "\n")

    def randomPrimeECs(self):
        s = EllipticCurve.listRandomPrimeECs(self.n, self.p)
        self._output.insert(END, s + "\n")

    def randomPoints(self):
        s = EllipticCurve.listRandomPoints(EllipticCurve(self.a, self.b, self.p), self.m)
        self._output.insert(END, s + "\n")

    def clear(self):
        self._output.delete(1.0, END)


class BinaryTab(Tab):

    def __init__(self, master, name):
        Tab.__init__(self, master, name)

        self.a = Polynomial("z^8 + z") # initially E : y^2 + xy = x^3 + (z^8 + z)x^2 + (z + 1)
        self.b = Polynomial("z + 1")
        self.r = 9 # field is initially GF(2^9)
        self.modulus = Polynomial("z^9 + z^8 + 1") # initial irred poly
        self.Gx = Polynomial("z^8 + z^6 + z^2 + 1") # initially G = (z^8 + z^6 + z^2 + 1, z^7 + z^5 + z^4 + z + 1)
        self.Gy = Polynomial("z^7 + z^5 + z^4 + z + 1")
        self.Px = Polynomial("z^8 + z^5 + z^3 + z") # initially P = (z^8 + z^5 + z^3 + z, z^8 + z^4 + z + 1)
        self.Py = Polynomial("z^8 + z^4 + z + 1")
        self.Qx = Polynomial("z^6 + z^4 + z^3 + z") # initially Q = (z^6 + z^4 + z^3 + z, z^5 + 1)
        self.Qy = Polynomial("z^5 + 1")
        self.k = 179
        self.n = 5 # initially n = 5 random curves
        self.m = 10 # initially m = 10 random points

        outputFrame = Frame(self)
        Button(outputFrame, text="Clear Output", bg="blue", fg="white", command=(lambda: self.clear()), borderwidth=1).pack(side=BOTTOM, pady=3)
        self._output = Text(outputFrame, height=15, width=70)
        self._output.insert(END, "You are responsible for making sure the irreducible polynomial you use is actually irreducible. "
                                 "The default, z^9 + z^8 + 1, is irreducible.\n\n")
        self._output.pack(side=LEFT)
        scrollbar = Scrollbar(outputFrame)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self._output.yview)

        ecInfo = Frame(self)
        polyFrame = Frame(self)
        ptsInfo1 = Frame(self)
        ptsInfo2 = Frame(self)
        arithmeticFrame = Frame(self)
        orderFrame = Frame(self)
        listFrame = Frame(self)
        ptsFrame = Frame(self)

        self.curveString = StringVar()
        self.curveString.set("E : F_(2^" + str(self.r) + ") : y^2 + xy = x^3 + ")
        curveLabel = Label(ecInfo, textvariable=self.curveString, bg="orange", fg="black", borderwidth=1).grid(row=1, column=1)
        self._a = Entry(ecInfo, width=25)
        self._a.insert(0, self.a)
        self._a.bind("<Return>", (lambda event: self.changeA()))
        self._a.grid(row=1, column=2)
        Label(ecInfo, text="x^2 + ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=3)
        self._b = Entry(ecInfo, width=25)
        self._b.insert(0, self.b)
        self._b.bind("<Return>", (lambda event: self.changeB()))
        self._b.grid(row=1, column=4)

        Label(polyFrame, text="Irreducible Polynomial: ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._irred = Entry(polyFrame, width=51)
        self._irred.insert(0, self.modulus)
        self._irred.bind("<Return>", (lambda event: self.changeModulus()))
        self._irred.grid(row=1, column=2, pady=3)

        Label(ptsInfo1, text="Generator G = (", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._Gx = Entry(ptsInfo1, width=15)
        self._Gx.insert(0, self.Gx)
        self._Gx.bind("<Return>", (lambda event: self.changeG()))
        self._Gx.grid(row=1, column=2, pady=3)
        Label(ptsInfo1, text=", ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=3, pady=3)
        self._Gy = Entry(ptsInfo1, width=15)
        self._Gy.insert(0, self.Gy)
        self._Gy.bind("<Return>", (lambda event: self.changeG()))
        self._Gy.grid(row=1, column=4, pady=3)
        Label(ptsInfo1, text="), k = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=5, pady=3)
        self._k = Entry(ptsInfo1, width=5)
        self._k.insert(0, self.k)
        self._k.bind("<Return>", (lambda event: self.changeK()))
        self._k.grid(row=1, column=6, pady=3)

        Label(ptsInfo2, text="P = ", bg="blue", fg="white", borderwidth=1).grid(row=1, column=1, pady=3)
        self._Px = Entry(ptsInfo2, width=15)
        self._Px.insert(0, self.Px)
        self._Px.bind("<Return>", (lambda event: self.changeP()))
        self._Px.grid(row=1, column=2, pady=3)
        Label(ptsInfo2, text=", ", bg="blue", fg="white", borderwidth=1).grid(row=1, column=3, pady=3)
        self._Py = Entry(ptsInfo2, width=15)
        self._Py.insert(0, self.Py)
        self._Py.bind("<Return>", (lambda event: self.changeP()))
        self._Py.grid(row=1, column=4, pady=3)
        Label(ptsInfo2, text="), Q = ", bg="blue", fg="white", borderwidth=1).grid(row=1, column=5, pady=3)
        self._Qx = Entry(ptsInfo2, width=15)
        self._Qx.insert(0, self.Qx)
        self._Qx.bind("<Return>", (lambda event: self.changeQ()))
        self._Qx.grid(row=1, column=6, pady=3)
        Label(ptsInfo2, text=", ", bg="blue", fg="white", borderwidth=1).grid(row=1, column=7, pady=3)
        self._Qy = Entry(ptsInfo2, width=15)
        self._Qy.insert(0, self.Qy)
        self._Qy.bind("<Return>", (lambda event: self.changeQ()))
        self._Qy.grid(row=1, column=8)
        Label(ptsInfo2, text=")", bg="blue", fg="white", borderwidth=1).grid(row=1, column=9, pady=3)

        Button(arithmeticFrame, text="P + Q", bg="blue", fg="white", command=(lambda: self.add())).grid(row=1, column=1, padx=5, pady=3)
        Button(arithmeticFrame, text="kP", bg="blue", fg="white", command=(lambda: self.mult())).grid(row=1, column=2, padx=5, pady=3)
        Button(arithmeticFrame, text="log_G(P)", bg="blue", fg="white", command=(lambda: self.log())).grid(row=1, column=3, padx=5, pady=3)

        Button(orderFrame, text="Order(E)", bg="blue", fg="white", command=(lambda: self.order())).grid(row=1, column=1, padx=5, pady=3)
        Button(orderFrame, text="Order(G)", bg="blue", fg="white", command=(lambda: self.pointOrder())).grid(row=1, column=2, padx=5, pady=3)

        Label(listFrame, text="Generate ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._n = Entry(listFrame, width=3)
        self._n.insert(0, self.n)
        self._n.bind("<Return>", (lambda event: self.changeN()))
        self._n.grid(row=1, column=2, pady=3)
        Button(listFrame, text="Random ECs", bg="orange", fg="black", command=(lambda: self.randomECs())).grid(row=1, column=3, padx=5, pady=3)

        Label(ptsFrame, text="List ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._m = Entry(ptsFrame, width=3)
        self._m.insert(0, self.m)
        self._m.bind("<Return>", (lambda event: self.changeM()))
        self._m.grid(row=1, column=2, pady=3)
        Button(ptsFrame, text="Random points on E", bg="orange", fg="black", command=(lambda: self.randomPoints())).grid(row=1, column=3, padx=5, pady=3)

        ecInfo.pack(side=TOP)
        polyFrame.pack(side=TOP)
        ptsInfo1.pack(side=TOP)
        ptsInfo2.pack(side=TOP)
        arithmeticFrame.pack(side=TOP)
        orderFrame.pack(side=TOP)
        listFrame.pack(side=TOP)
        ptsFrame.pack(side=TOP)
        outputFrame.pack(side=BOTTOM)

    def changeA(self):
        temp = self._a.get()
        if Polynomial.isValid(temp):
            self.a = Polynomial(temp) % self.modulus
            self._a.delete(0, END)
            self._a.insert(0, self.a)
            E = BinaryEllipticCurve(self.a, self.b, self.modulus)
            self._output.insert(END, str(E) + "\n")
        else:
            self._a.delete(0, END)
            self._a.insert(0, self.a)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeB(self):
        temp = self._b.get()
        if Polynomial.isValid(temp):
            self.b = Polynomial(temp) % self.modulus
            self._b.delete(0, END)
            self._b.insert(0, self.b)
            E = BinaryEllipticCurve(self.a, self.b, self.modulus)
            self._output.insert(END, str(E) + "\n")
        else:
            self._b.delete(0, END)
            self._b.insert(0, self.b)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeModulus(self):
        temp = self._irred.get()
        if Polynomial.isValid(temp):
            self.modulus = Polynomial(temp)
            self.r = self.modulus.degree()
            self.curveString.set("E : F_(2^" + str(self.r) + ") : y^2 + xy = x^3 + ")
            self._irred.delete(0, END)
            self._irred.insert(0, self.modulus)
            E = BinaryEllipticCurve(self.a, self.b, self.modulus)
            self._output.insert(END, "The irreducible polynomial is now set to " + str(self.modulus) + ".\n")
        else:
            self._irred.delete(0, END)
            self._irred.insert(0, self.modulus)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeG(self):
        tempx = self._Gx.get()
        tempy = self._Gy.get()
        if Polynomial.isValid(tempx) and Polynomial.isValid(tempy):
            self.Gx = Polynomial(tempx) % self.modulus
            self.Gy = Polynomial(tempy) % self.modulus
            self._Gx.delete(0, END)
            self._Gy.delete(0, END)
            self._Gx.insert(0, self.Gx)
            self._Gy.insert(0, self.Gy)
            self._output.insert(END, "G = " + str(PolynomialPoint(self.Gx, self.Gy, 1)) + "\n")
        else:
            self._Gx.delete(0, END)
            self._Gy.delete(0, END)
            self._Gx.insert(0, self.Gx)
            self._Gy.insert(0, self.Gy)
            self._output.insert(END, "There was an error with your input. Please try again.\n")


    def changeP(self):
        tempx = self._Px.get()
        tempy = self._Py.get()
        if Polynomial.isValid(tempx) and Polynomial.isValid(tempy):
            self.Px = Polynomial(tempx) % self.modulus
            self.Py = Polynomial(tempy) % self.modulus
            self._Px.delete(0, END)
            self._Py.delete(0, END)
            self._Px.insert(0, self.Px)
            self._Py.insert(0, self.Py)
            self._output.insert(END, "P = " + str(PolynomialPoint(self.Px, self.Py, 1)) + "\n")
        else:
            self._Px.delete(0, END)
            self._Py.delete(0, END)
            self._Px.insert(0, self.Px)
            self._Py.insert(0, self.Py)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeQ(self):
        tempx = self._Qx.get()
        tempy = self._Qy.get()
        if Polynomial.isValid(tempx) and Polynomial.isValid(tempy):
            self.Qx = Polynomial(tempx) % self.modulus
            self.Qy = Polynomial(tempy) % self.modulus
            self._Qx.delete(0, END)
            self._Qy.delete(0, END)
            self._Qx.insert(0, self.Qx)
            self._Qy.insert(0, self.Qy)
            self._output.insert(END, "Q = " + str(PolynomialPoint(self.Qx, self.Qy, 1)) + "\n")
        else:
            self._Qx.delete(0, END)
            self._Qy.delete(0, END)
            self._Qx.insert(0, self.Qx)
            self._Qy.insert(0, self.Qy)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeK(self):
        try:
            self.k = int(self._k.get())
            self._k.delete(0, END)
            self._k.insert(0, self.k)
            self._output.insert(END, "k = " + str(self.k) + "\n")
        except ValueError:
            self._k.delete(0, END)
            self._k.insert(0, self.k)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeN(self):
        try:
            self.n = int(self._n.get())
            self._n.delete(0, END)
            self._n.insert(0, self.n)
            self._output.insert(END, "Random curve selection will now generate " + str(self.n) + " curve")
            if self.n != 1:
                self._output.insert(END, "s")
            self._output.insert(END, ".\n")
        except ValueError:
            self._n.delete(0, END)
            self._n.insert(0, self.n)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeM(self):
        try:
            self.m = int(self._m.get())
            self._m.delete(0, END)
            self._m.insert(0, self.m)
            self._output.insert(END, "Random point selection will now generate " + str(self.m) + " point")
            if self.m != 1:
                self._output.insert(END, "s")
            self._output.insert(END, ".\n")
        except ValueError:
            self._m.delete(0, END)
            self._m.insert(0, self.m)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def add(self):
        P = PolynomialPoint(self.Px, self.Py, Polynomial("1"))
        Q = PolynomialPoint(self.Qx, self.Qy, Polynomial("1"))
        R = P.add(Q, self.a, self.b, self.modulus)
        self._output.insert(END, str(P) + " + " + str(Q) + " = " + str(R) + "\n")

    def mult(self):
        P = PolynomialPoint(self.Px, self.Py, Polynomial("1"))
        R = P.mult(self.k, self.a, self.b, self.modulus)
        self._output.insert(END, str(self.k) + str(P) + " = " + str(R) + "\n")

    def log(self):
        E = BinaryEllipticCurve(self.a, self.b, self.modulus)
        P = PolynomialPoint(self.Px, self.Py, Polynomial("1"))
        G = PolynomialPoint(self.Gx, self.Gy, Polynomial("1"))
        R = E.log(P, G)
        self._output.insert(END, "log_G" + str(P) + " = " + str(R) + "\n")

    def order(self):
        ord = BinaryEllipticCurve(self.a, self.b, self.modulus).order()
        self._output.insert(END, "|E| = " + str(ord) + "\n")

    def pointOrder(self):
        ord = BinaryEllipticCurve(self.a, self.b, self.modulus).pointOrder(PolynomialPoint(self.Gx, self.Gy, Polynomial("1")))
        self._output.insert(END, "|G| = " + str(ord) + "\n")

    def randomECs(self):
        s = BinaryEllipticCurve.listRandomECs((1<<self.modulus.degree()), self.modulus, self.n)
        self._output.insert(END, s + "\n")

    def randomPoints(self):
        s = BinaryEllipticCurve.listRandomPoints(BinaryEllipticCurve(self.a, self.b, self.modulus), self.m)
        self._output.insert(END, s + "\n")

    def clear(self):
        self._output.delete(1.0, END)
        self._output.insert(END, "You are responsible for making sure the irreducible polynomial you use is actually irreducible. "
                                 "The default, z^9 + z^8 + 1, is irreducible.\n\n")


class MiscTab(Tab):

    def __init__(self, master, name):
        Tab.__init__(self, master, name)

        self.a = 43827423
        self.b = 8372842
        self.p = 7447344552397
        self.P = Polynomial("z^29 + z^18 + z^3 + 1")
        self.Q = Polynomial("z^17 + z^13 + z^11 + z^7")
        self.k = 473423
        self.R = Polynomial("z^32 + z^26 + z^23 + z^22 + z^16 + z^12 + z^11 + z^10 + z^8 + z^7 + z^5 + z^4 + z^2 + z + 1") # default is crc-32 poly

        outputFrame = Frame(self)
        Button(outputFrame, text="Clear Output", bg="blue", fg="white", command=(lambda: self.clear()), borderwidth=1).pack(side=BOTTOM, pady=3)
        self._output = Text(outputFrame, height=15, width=65)
        self._output.insert(END, "You are responsible for making sure the irreducible polynomial you use is actually irreducible. "
                                 "The default, z^32 + z^26 + z^23 + z^22 + z^16 + z^12 + z^11 + z^10 + z^8 + z^7 + z^5 + z^4 + z^2 + z + 1,"
                                 " is irreducible.\n\n")
        self._output.pack(side=LEFT)
        scrollbar = Scrollbar(outputFrame)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self._output.yview)

        modularInput = Frame(self)
        modularButtons = Frame(self)
        polyInput = Frame(self)
        irredFrame = Frame(self)
        polyOut1 = Frame(self)
        polyOut2 = Frame(self)

        Label(modularInput, text="a = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._a = Entry(modularInput, width=10)
        self._a.insert(0, self.a)
        self._a.bind("<Return>", (lambda event: self.changeA()))
        self._a.grid(row=1, column=2, pady=3)
        Label(modularInput, text=" b = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=3, pady=3)
        self._b = Entry(modularInput, width=10)
        self._b.insert(0, self.b)
        self._b.bind("<Return>", (lambda event: self.changeB()))
        self._b.grid(row=1, column=4, pady=3)
        Label(modularInput, text=" p = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=5, pady=3)
        self._p = Entry(modularInput, width=20)
        self._p.insert(0, self.p)
        self._p.bind("<Return>", (lambda event: self.changePrime()))
        self._p.grid(row=1, column=6, pady=3)
        Button(modularInput, text="Generate Random Prime", bg="blue", fg="white", command=(lambda: self.generatePrime())).grid(row=1, column=7, padx=5, pady=3)

        Button(modularButtons, text="a^b (mod p)", bg="blue", fg="white", command=(lambda: self.modExp())).grid(row=1, column=1, padx=5, pady=3)
        Button(modularButtons, text="1/a (mod p)", bg="blue", fg="white", command=(lambda: self.inverse())).grid(row=1, column=2, padx=5, pady=3)
        Button(modularButtons, text="sqrt(a) (mod p)", bg="blue", fg="white", command=(lambda: self.sqrt())).grid(row=1, column=3, padx=5, pady=3)

        Label(polyInput, text="P(z) = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._P = Entry(polyInput, width=25)
        self._P.insert(0, self.P)
        self._P.bind("<Return>", (lambda event: self.changeP()))
        self._P.grid(row=1, column=2, pady=3)
        Label(polyInput, text=" Q(z) = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=3, pady=3)
        self._Q = Entry(polyInput, width=25)
        self._Q.insert(0, self.Q)
        self._Q.bind("<Return>", (lambda event: self.changeQ()))
        self._Q.grid(row=1, column=4, pady=3)

        Label(irredFrame, text="R(z) = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=1, pady=3)
        self._R = Entry(irredFrame, width=25)
        self._R.insert(0, self.R)
        self._R.bind("<Return>", (lambda event: self.changeR()))
        self._R.grid(row=1, column=2, pady=3)
        Label(irredFrame, text=" k = ", bg="orange", fg="black", borderwidth=1).grid(row=1, column=3, pady=3)
        self._k = Entry(irredFrame, width=10)
        self._k.insert(0, self.k)
        self._k.bind("<Return>", (lambda event: self.changeK()))
        self._k.grid(row=1, column=4, pady=3)

        Button(polyOut1, text="P(z) + Q(z) (mod R(z))", bg="blue", fg="white", command=(lambda: self.polyAdd())).grid(row=1, column=1, padx=5, pady=3)
        Button(polyOut1, text="P(z) * Q(z) (mod R(z))", bg="blue", fg="white", command=(lambda: self.polyMult())).grid(row=1, column=2, padx=5, pady=3)

        Button(polyOut2, text="P(z)^k (mod R(z))", bg="blue", fg="white", command=(lambda: self.polyModExp())).grid(row=1, column=1, padx=5, pady=3)
        Button(polyOut2, text="1/P(z) (mod R(z))", bg="blue", fg="white", command=(lambda: self.polyInverse())).grid(row=1, column=2, padx=5, pady=3)
        Button(polyOut2, text="sqrt(P(z)) (mod R(z))", bg="blue", fg="white", command=(lambda: self.polySqrt())).grid(row=1, column=3, padx=5, pady=3)

        modularInput.pack(side=TOP)
        modularButtons.pack(side=TOP)
        polyInput.pack(side=TOP)
        irredFrame.pack(side=TOP)
        polyOut1.pack(side=TOP)
        polyOut2.pack(side=TOP)
        outputFrame.pack(side=BOTTOM)

    def changeA(self):
        try:
            self.a = int(self._a.get()) % self.p
            self._a.delete(0, END)
            self._a.insert(0, self.a)
            self._output.insert(END, "a = " + str(self.a) + "\n")
        except ValueError:
            self._a.delete(0, END)
            self._a.insert(0, self.a)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeB(self):
        try:
            self.b = int(self._b.get()) % self.p
            self._b.delete(0, END)
            self._b.insert(0, self.b)
            self._output.insert(END, "b = " + str(self.b) + "\n")
        except ValueError:
            self._b.delete(0, END)
            self._b.insert(0, self.b)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changePrime(self):
        try:
            temp = int(self._p.get())
            if ECMath.isPrime(temp):
                self.p = temp
                self._p.delete(0, END)
                self._p.insert(0, self.p)
                self._output.insert(END, "p = " + str(self.p) + "\n")
            else:
                self._output.insert(END, str(temp) + " is not prime. Please try again.\n")
                self._p.delete(0, END)
                self._p.insert(0, self.p)
        except ValueError:
            self._p.delete(0, END)
            self._p.insert(0, self.p)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def generatePrime(self):
        digits = randint(1, 40)
        self.p = ECMath.randomPrime(digits)
        self._p.delete(0, END)
        self._p.insert(0, self.p)
        self._output.insert(END, "p = " + str(self.p) + "\n")

    def modExp(self):
        temp = pow(self.a, self.b, self.p)
        self._output.insert(END, str(self.a) + "^" + str(self.b) + " (mod " + str(self.p) + ") = " + str(temp) + "\n")

    def inverse(self):
        temp = ECMath.inverse(self.a, self.p)
        if temp != -1:
            self._output.insert(END, "1/" + str(self.a) + " (mod " + str(self.p) + ") = " + str(temp) + "\n")
        else:
            self._output.insert(END, "1/" + str(self.a) + " (mod " + str(self.p) + ") = undefined\n")

    def sqrt(self):
        if self.a % self.p == 0:
            self._output.insert(END, "sqrt(" + str(self.a) + ") (mod " + str(self.p) + ") = 0\n")
        elif ECMath.jacobi(self.a, self.p) == 1:
            temp = ECMath.sqrt(self.a, self.p)
            self._output.insert(END, "sqrt(" + str(self.a) + ") (mod " + str(self.p) + ") = " + str(temp) + "\n")
        else:
            self._output.insert(END, str(self.a) + " is not a square (mod " + str(self.p) + ")\n")

    def changeP(self):
        temp = self._P.get()
        if Polynomial.isValid(temp):
            self.P = Polynomial(temp) % self.R
            self._P.delete(0, END)
            self._P.insert(0, self.P)
            self._output.insert(END, "P(z) = " + str(self.P) + "\n")
        else:
            self._P.delete(0, END)
            self._P.insert(0, self.P)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeQ(self):
        temp = self._Q.get()
        if Polynomial.isValid(temp):
            self.Q = Polynomial(temp) % self.R
            self._Q.delete(0, END)
            self._Q.insert(0, self.Q)
            self._output.insert(END, "Q(z) = " + str(self.Q) + "\n")
        else:
            self._Q.delete(0, END)
            self._Q.insert(0, self.Q)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeR(self):
        temp = self._R.get()
        if Polynomial.isValid(temp):
            self.R = Polynomial(temp)
            self._R.delete(0, END)
            self._R.insert(0, self.R)
            self._output.insert(END, "R(z) = " + str(self.R) + "\n")
        else:
            self._R.delete(0, END)
            self._R.insert(0, self.R)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def changeK(self):
        try:
            self.k = int(self._k.get())
            self._k.delete(0, END)
            self._k.insert(0, self.k)
            self._output.insert(END, "k = " + str(self.k) + "\n")
        except ValueError:
            self._k.delete(0, END)
            self._k.insert(0, self.k)
            self._output.insert(END, "There was an error with your input. Please try again.\n")

    def polyAdd(self):
        temp = (self.P + self.Q) % self.R
        self._output.insert(END, "P(z) + Q(z) = (" + str(temp) + ") (mod R(z))\n")

    def polyMult(self):
        temp = (self.P * self.Q) % self.R
        self._output.insert(END, "P(z) * Q(z) = (" + str(temp) + ") (mod R(z))\n")

    def polyModExp(self):
        temp = self.P.modExp(self.k, self.R)
        self._output.insert(END, "P(z)^" + str(self.k) + " = (" + str(temp) + ") (mod R(z))\n")

    def polyInverse(self):
        temp = self.P.inverse(self.R)
        if temp is None:
            self._output.insert(END, "1/(P(z)) = undefined (mod R(z))\n")
        else:
            self._output.insert(END, "1/(P(z)) = (" + str(temp) + ") (mod R(z))\n")

    def polySqrt(self):
        temp = self.P.sqrt(self.R)
        self._output.insert(END, "sqrt(P(z)) = (" + str(temp) + ") (mod R(z))\n")

    def clear(self):
        self._output.delete(1.0, END)
        self._output.insert(END, "You are responsible for making sure the irreducible polynomial you use is actually irreducible. "
                                 "The default, z^32 + z^26 + z^23 + z^22 + z^16 + z^12 + z^11 + z^10 + z^8 + z^7 + z^5 + z^4 + z^2 + z + 1,"
                                 " is irreducible.\n\n")


class TabBar(Frame):

    def __init__(self, master=None, initName=None):
        Frame.__init__(self, master)
        self._tabs = {}
        self._buttons = {}
        self._currentTab = None
        self._initName = initName

    def show(self):
        self.pack(side=TOP, expand=YES, fill=X)
        self.switchTab(self._initName or self._tabs.keys()[-1])# switch the tab to the first tab

    def add(self, tab):
        tab.pack_forget()									# hide the tab on init

        self._tabs[tab._tabName] = tab						# add it to the list of tabs
        b = Button(self, text=tab._tabName, relief=BASE,	# basic button stuff
            command=(lambda name=tab._tabName: self.switchTab(name)))	# set the command to switch tabs
        b.pack(side=LEFT)												# pack the buttont to the left mose of self
        self._buttons[tab._tabName] = b											# add it to the list of buttons

    def delete(self, tabname):

        if tabname == self._currentTab:
            self._currentTab = None
            self._tabs[tabname].pack_forget()
            del self._tabs[tabname]
            self.switchTab(self._tabs.keys()[0])

        else:
            del self._tabs[tabname]

        self._buttons[tabname].pack_forget()
        del self._buttons[tabname]


    def switchTab(self, name):
        if self._currentTab:
            self._buttons[self._currentTab].config(relief=BASE)
            self._tabs[self._currentTab].pack_forget()			# hide the current tab
        self._tabs[name].pack(side=BOTTOM)							# add the new tab to the display
        self._currentTab = name									# set the current tab to itself
        self._buttons[name].config(relief=SELECTED)					# set it to the selected style