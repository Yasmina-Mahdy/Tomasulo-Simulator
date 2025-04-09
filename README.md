# Tomasulo-Simulator

A project aiming to simulate the behavior of Tomasulo's algorithm with speculation supporting the ISA of the Ridiculously Simple Computer (RiSC-16) proposed by Bruce Jacob.

# Release Notes

  ## What works
* Support Tomasulo’s algorithm with speculation
* Support a variable hardware organization, where the user can specify the number of reservation stations for each class of instructions and the number of ROB entries, as well, will specify the number of cycles needed by each functional unit type.

  ## What does not work
* When multiple instructions need the writing bus, we do not give priority to the earlier instruction, but instead write according to the order of the reservation units

  ## Issues
* We currently do not implement input validation and error handling.
* Minor issue where the Ret execution cycles are saved greater than their actual value by one (committing is correct, however)

  ## Assumptions
* We assume that the user inputs correct values
* We also assume that we cannot issue in the same cycle that we flush
* We assume that, in case a load was committed and the store becomes the head of the L/S queue that it may start executing in the same cycle
