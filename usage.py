from universe import *



# This is an object of the universe class which is extended from Tk
u1=Life()
u1.mainloop()

# Click on an individual cell to change its state.
# Click "Simulate" to simulate the universe. 
# Click "Step" to change generation one by one.
# Click "Stop" to stop the simulation, and then close the winodw.

# EXAMPLES: These are a few examples taken from Wikipedia

u2=Life("Examples/glider")
u2.mainloop()

# Other examples:

# u3=Life("Examples/pentadecathlon")
# u3.mainloop()

# u3=Life("Examples/blinker")
# u3.mainloop()

# u3=Life("Examples/block")
# u3.mainloop()

# u3=Life("Examples/beacon")
# u3.mainloop()

# u3=Life("Examples/toad")
# u3.mainloop()
