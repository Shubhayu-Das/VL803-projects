# Tomasulo OOO Processor
-------------------------

This is my attempt to make an interactive simulation of the Tomasulo out of order processor, as part of the VL803 course.

-------------------
### Student
Name: Shubhayu Das

Roll number: IMT2018523

-----------------------------

### Progress
Completed mostly, apart from few doubts.

PENDING:
1. Convert main.py into a Tomasulo class?
2. Additional GUI features
3. Document the code base and improve this README
4. See if anything can be done about the resolution scaling

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

I have tested the code on Python 3.8.7 on both the OS (Windows 1903 build and Ubuntu 20.04.01 LTS), if there are any issues, please raise an Issue on Github. The GUI might appear very different in different OSes. That's just Python, I can't do anything about it. PySimpleGUI restricts me in dynamically setting the positions, depending on the screen resolution. I can only guarantee proper working on a 1920x1080 screen. On smaller screens, you really need to reduce the ```GUI_FONTSIZE``` variable in ```constants.py```.

--------------------

### Instructions for running

This simulator supports LW/SW, ADD/SUB from RISC-V RV32I, and MUL/DIV from RISC-V RV32M. 

- Place your ```asm``` program in the src folder.
- Open a terminal and navigate to the ```code/``` folder. Execute: ```python assembler.py src/<filename.asm>```.
- This will generate the ```elf``` file in ```build/<filename.elf>```.
- Now run: ```python main.py build/<filename.elf>``` to launch the simulation
- The simulation supports pausing, stepping back and forward - one step at a time.
- To stop the simulation, simply close the window

- To change the duration spent on each cycle, open ```constants.py``` and adjust the ```CYCLE_DURATION``` in *milliseconds* to your desired value.

-----

### Known issues

The graphics library that I am using is not documented too well and is a bit troublesome to use. As a result, all the tables in the GUI might not fit properly on different screen sizes. It works properly on a 15.6 inch laptop screen, running Ubuntu 20.04.2 LTS. In case it isn't fitting in your screen:

- Open ```constants.py``` and adjust the value of ```GUI_FONTSIZE``` until it works for you.