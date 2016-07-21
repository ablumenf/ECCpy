from TabbedGUI import *

__author__ = 'Aaron Blumenfeld'

# This is the driver program. TabbedGUI.py has all the GUI details

def main():
    root = Tk()
    root.title("ECC Toolkit")

    bar = TabBar(root, "GF(p)")

    tab1 = PrimeTab(root, "GF(p)")
    tab2 = BinaryTab(root, "GF(2^r)")
    tab3 = MiscTab(root, "Misc.")

    bar.add(tab1)
    bar.add(tab2)
    bar.add(tab3)

    bar.config(bd=2, relief=RIDGE)
    bar.show()
    root.mainloop()

main()