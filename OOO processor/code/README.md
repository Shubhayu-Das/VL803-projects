# Tomasulo OOO Processor
-------------------------

This is my attempt to make an interactive simulation of the Tomasulo out of order processor, as part of the VL803 course.

-------------------
### Student
Name: Shubhayu Das

Roll number: IMT2018523

-----------------------------

### Progress
1. GUI - semi-complete; to be updated, linked
2. Instruction data structure - initially complete. Might have to add on features later
3. Reservation Station - needs simplification
4. ROB - complete
5. Load/Store buffer - incomplete
6. ARF - Done, registers must ALWAYS be called from ARF. It will take care if it is marked busy, and supply value from the RAT
7. RAT - Done

IMPORTANT: Connect registers in instructions to their values

1. Connect components together - Pending
2. Connect system to GUI
------------------------------

### Software libraries

The GUI needs the ```tkinter``` and ```pysimplegui```. These can be installed using the following commands:

On Linux/Ubuntu:
```bash
$ sudo apt install python3-tk
$ pip install pysimplegui
```

On Windows:
```
$ pip install pysimplegui
```

I have tested the code on Python 3.8.7 on both the OS (Windows 1903 build and Ubuntu 20.04.01 LTS), if there are any issues, please raise an Issue on Github. The GUI might appear very different in different OSes. That's just Python, I can't do anything about it.