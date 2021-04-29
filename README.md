# Projects for Processor Architecture course

This repo contains all my work for the VL803 course on Processor Architecture, by Prof. Nanditha Rao.

-------------------

### First assignment
Design a 7 stage pipelined OOO processor OR a Tomasulo machine, using any programming language. I am using Python over iVerilog, because I wanted to make a nice GUI. I partly get lost in the complexity of signals on GTKWave.

### Second assignment
Second assignment involved simulating various cache algorithms used for branch prediction, prefetching and cache
replacement. We had a choice between the ChampSim/gem5 simulators. This was a group project, so the code files are
present in a submodule repo. We chose to use ChampSim, because we deemed it to be enough for testing the algorithms that
we implemented.

### Third assignment
The third assignment builds on top of the first one, by optionally adding caches/branch predictors/prefetchers. We could
work on designing a brand new vector processor, but I intend to make my existing program a finished product, which can
be used for a lot of things. I did this project in a group. For more details, take a look at the relevant folder.
