# ProbabilitySim
Calculate value of effect procs over a fight with a given set of events and parameters

**Usage**
Install following instructions at [https://docs.python.org/3/using/windows.html](https://docs.python.org/3/using/windows.html)  
in a cli, navigate to the directory and run the file with some parameters. 

-h will output the possible parameters: 

>--ac (ActivationChance) --cps (Casts Per Second) --ed (EffectDuration) --cd (CoolDown) --ep (EffectPower) --fl (FightLength) --i (Iterations)

Example input:

>\>python3 .\ProbabilitySim.py --ac .05 --cps .42 --ed 15 --cd 0 --ep 135 --fl 300 --i 10000