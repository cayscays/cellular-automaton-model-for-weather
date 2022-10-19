#
# Creates the GUI, the display, initiates the stats file and controls the GUI
#
# Author:       cayscays
# Date:         November 2021
# Version:      1
#

import tkinter as tk

from model.world import *
from stats_handling import generate_stats_file

MAIN_WINDOW_TITLE = 'Cellular Automaton World Model by Cayscays'
TOOLBAR_WINDOW_TITLE = 'Toolbar'

stats_file = generate_stats_file.StatsFile()

# Set the main display window
window = tk.Tk()
window.title(MAIN_WINDOW_TITLE)
# window.state('zoomed')

# Set the toolbar window
toolbar = tk.Toplevel(window)
toolbar.title(TOOLBAR_WINDOW_TITLE)
toolbar.attributes('-topmost', True)  # always on top
toolbar.grab_set()

# Set the buttons on the toolbar:
instructions = tk.Label(toolbar, text='Displaying: ', font=("Arial", 15))
instructions.pack()
v = tk.StringVar(toolbar, "Choose a datatype:")
label1 = tk.Label(toolbar, text='123', textvariable=v, font=("Arial", 15))
label1.pack()
counter = 0


# Updates the display according to the chosen parameter to be displayed and the current state of the World
def update_display():
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            text_vals = world.grid[i][j].get_text(v.get())
            draw_cell(landscape=world.grid[i][j].landscape,
                      text=text_vals[0],
                      text_color=text_vals[1],
                      font_size=text_vals[2],
                      row=i + 1, col=j)

    window.update()
    window.after(500)


# Creates the buttons of the parameters to be displayed
for param in PARAMS:
    tk.Radiobutton(toolbar, text=param, variable=v,
                   value=param, indicator=0,
                   command=update_display,
                   height=2, width=15,
                   background="alice blue").pack()


# Next day
def next_generation():
    world.update(stats_file)
    update_display()


# Run for a week
def week():
    for i in range(7):
        next_generation()
        window.after(1)


# Run for a year
def year():
    for i in range(365):
        next_generation()
        window.after(1)
    print('year file ready')


# Run for a year without updating the display
def year_only_to_file():
    for i in range(365):
        world.update(stats_file)
    print('year file ready')


# Closes the stats file and both windows.
def exit_the_program():
    stats_file.close()
    toolbar.destroy()
    window.destroy()


# Action buttons
toolbar.geometry("200x600")
tk.Button(toolbar, text="Next day", height=2, width=15, command=next_generation).pack()
tk.Button(toolbar, text="run for a week", height=2, width=15, command=week).pack()
tk.Button(toolbar, text="run for a year", height=2, width=15, command=year).pack()
tk.Button(toolbar, text="year to file", height=2, width=15, command=year_only_to_file).pack()
tk.Button(toolbar, text="exit", height=2, width=15, command=exit_the_program, background="red").pack()

# Loads the landscape images:
empty_sea = tk.PhotoImage(file="Resources/images/royalty free sea.gif")
iceberg = tk.PhotoImage(file="Resources/images/royalty free iceberg.gif")
empty_land = tk.PhotoImage(file="Resources/images/royalty free empty_land.gif")
city = tk.PhotoImage(file="Resources/images/royalty free city.gif")
forest = tk.PhotoImage(file="Resources/images/royalty free forest.gif")


def get_cell_image(landscape):
    return {
        'Sea': empty_sea,
        'Ice': iceberg,
        'Land': empty_land,
        'City': city,
        'Forest': forest
    }.get(landscape, 'Error - landscape not found')


def draw_cell(landscape, text, text_color, font_size, row, col):
    img = get_cell_image(landscape)
    tk.Label(window, height=65, width=65, image=img, borderwidth=1, relief="raised", text=text,
             font=("Ariel", font_size, 'bold'),
             foreground=text_color, compound="center").grid(row=row, column=col)
