from gui import *
from Asset import *
from bank import *
from finance_tools import *


# saving sessions...

root = Tk()
my_gui = Budget_GUI(root, name_app="Budget Tracking")
my_gui.home_screen(title='Welcome to Budget Tracking', start_txt='Start Budget Monitoring')

my_gui.run()