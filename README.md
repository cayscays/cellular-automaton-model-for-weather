# cellular-automaton-model-for-weather
A cellular automaton that models the earth and the interactions between weather elements.
Alongside a visual representation, the program also saves each run's [data](#data) for analysis.

![photo](https://user-images.githubusercontent.com/116169018/196721106-de1f141a-17d4-4747-83da-4ffe3cb62463.gif)

## Links:
1.1 [Setup: Versions of resources](#versions-of-resources)

1.2 [Setup: Ubuntu](#on-ubuntu)

1.3 [Setup: Windows](#on-windows)

2.1 [Use](#use)

3.1 [Data](#data)


## Setup
### Resources
* Python 3.9
* Tkinter
* XlsxWriter 3.0.2

### On Ubuntu
In the terminal:
```bash
$ sudo apt-get install python3-tk
python -m pip install --upgrade pip
pip install tk
pip install XlsxWriter
```
Clone the cellular-automaton-model-for-weather repository and run main.py.

### On Windows
In the terminal:
```bash
python -m pip install --upgrade pip
pip install tk
pip install XlsxWriter
```
Clone the cellular-automaton-model-for-weather repository and run main.py.

## Use
Choose a datatype to display:

![image](https://user-images.githubusercontent.com/116169018/196721199-4ddd6a9a-e100-47ff-b398-f665d174bf1e.png)

All datatypes will be saved to the stats.xlsx file.

Choose a period of time for the model to run:

![image](https://user-images.githubusercontent.com/116169018/196721276-8d4ca8d6-8706-436b-bd2e-2f28e294326b.png)

## Data
After clicking "exit" the run's data will be saved to a file named stats.xlsx in the project's folder. The stats file of a previous run is deleted on the next run, it is advised to copy your stats file to a location outside the project's directory when needed for future use.

![image](https://user-images.githubusercontent.com/116169018/196721323-5d814a8e-bc5d-41ea-8131-94d2f5907d49.png)

Each row stands for a cell of the model.
Boolean datatypes, like rain and pollution, use 1 for true and 0 for false.
***
Thank you for reading and using my cellular automaton model.
