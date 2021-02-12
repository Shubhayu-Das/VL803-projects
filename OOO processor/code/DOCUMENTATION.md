Structure of registers in code:

Register(Parent) ----> RATRegister, ARFRegister

Linking Heirarchy
ARFRegister ---> RATRegister ---> ROBEntry

Calling (ARFRegister/RATRegister).<register>.getValue() gets the value from the parent in above heirarchy. So after links are set, I can still call ARF.<register>.getValue() to get the right value. The linking is extremely crucial here.