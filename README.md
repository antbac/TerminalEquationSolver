# Terminal Equation Solver

Terminal Equation Solver is a python script runnable in the a terminal-window that will solve equations passed as arguments to the script. The solver supports all commonly used math operations including those found in the python math/cmath libraries. It also handles complex numbers and will provide a decimal precision down to 10 decimals.


### Installation

The solver requires python v3+ in order to run, if you do not have the proper version of python installed it can be downloaded from [python.org](https://www.python.org/downloads/).

Once python has been poperly installed, all you have to do is to download the tes.py script and save it anywhere you like on your local system.


If you are running the script on a Linux system, you might want to consider adding an alias for the script in case you use it often. This is easily done by adding the following in the file ~/.bashrc
```sh
$ alias tes='python3 /path/to/script/tes.py'
```
The .bashrc has to be reloaded upon modification in order for the alias to be usable, this can either be done by restarting the computer or typing
```sh
$ . ~/.bashrc
```


### Usage

The program evaluates equations entered as terminal arguments.
Different statements are separated by spaces, i.e.
```
python3 tes.py A=1 B=2 A+B
```
This call would generate the following output
```
A+B = 3
```
The script will not print lines containing assignment (equal sign) unless the first argument is either '-V' or '--verbose'.

If you wish to use an equation containing parantheses, the entire equation must be encapsulated in quotation-marks. This would look like this
```
python3 tes.py A=42 B=1336 "A*(B+1)"
```
Notice that encapsulating all equations in the same pair of quotation-marks would yield an error as all the equations would be treated as only one equation.
```
python3 tes.py "A=42 B=1336 A*(B+1)" --> Error
```

Variables are one or more capital letters ranging from A-Z.
Assignment of variables is done using an equal sign like this
```
python3 tes.py FOO=1
```
Variables must be assigned before they are referenced.
Meaning, this would not work
```
python3 tes.py A=B B=1 2*A --> Error
```
While this would
```
python3 tes.py B=1 A=B 2*A
```
Variables will be substituted for their values and not their references.
Which means that
```
python3 tes.py A=1 B=A A=2 B
```
would yield the output 1 and not 2 as A contains the value 1 when B gets assigned its value.

Lastly, variables are directly translated into their values, so AB would be the concatination of A and B rather than the multiplication.
This means that
```
python3 tes.py A=4 B=2 AB
```
would yield the output 42 rather than 8

### Todos

 - Implement matrix operations
 - Allow the script to solve equation-systems

License
----

MIT
