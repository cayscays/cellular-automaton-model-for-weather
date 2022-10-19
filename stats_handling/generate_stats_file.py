#
# Generate an Excel file with the world's stats.
# Writes over previous file with the same name if exists!
#
# Author:       cayscays
# Date:         November 2021
# Version:      1
#

import xlsxwriter


class StatsFile:
    def __init__(self):
        raw_titles = ['day', 'landscape', 'wind_direction', 'wind_speed', 'temp', 'pollution', 'clouds', 'height',
                      'rain']
        self.workbook = xlsxwriter.Workbook('stats.xlsx')
        self.worksheet_raw = self.workbook.add_worksheet('raw data')
        self.raw_row = 0

        col = 0
        for title in raw_titles:
            self.worksheet_raw.write(self.raw_row, col, title)
            col += 1
        self.raw_row += 1

    def close(self):
        self.workbook.close()

    def update_raw(self, day, cell_state):
        col = 0
        # raw cell values
        self.worksheet_raw.write(self.raw_row, col, day + 1)
        col += 1
        for param in cell_state:
            if param == True:
                val = 1
            elif param == False:
                val = 0
            else:
                val = param

            self.worksheet_raw.write(self.raw_row, col, val)
            col += 1
        self.raw_row += 1
