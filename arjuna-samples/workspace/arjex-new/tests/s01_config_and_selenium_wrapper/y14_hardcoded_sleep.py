from commons import *
from arjuna.core.audit import HardCoded

init_arjuna()

# You are stage 1
# You put a static wait for reasons best known to you at that time or sheer laziness :-)
import time
time.sleep(2)

def abc():
    HardCoded.sleep("abc I am being lazy", 2)

# Atleast do this
HardCoded.sleep("I am being lazy", 2)
HardCoded.sleep("I don't know what to do.", 2)
HardCoded.sleep("Temporary fix for 5 years.", 2)
	
abc()