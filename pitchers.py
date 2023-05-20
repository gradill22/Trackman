import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog as fd
from math import sin, cos, radians, sqrt
import os

# User's home team, formatted as tracked in Trackman
HOME_TEAM = 'SHE_UNI'

# Get the folder the user wants to save the data visualizations in (saved as .png images)
SAVE_FILE = fd.askdirectory(mustexist=True)
# Select the Trackman files that the user wants to visualize
CSV_FILES = fd.askopenfilenames(filetypes=[('Trackman CSV Files', '*.csv')]) if len(SAVE_FILE) > 0 else []

# Colors and markers for plotting pitch types
colors = {'Fastball': 'red', 'Curveball': 'blue', 'ChangeUp': 'green', 'Slider': 'yellow', 'Cutter': 'brown',
          'Sinker': 'purple', 'Splitter': 'silver', 'TwoSeamFastBall': 'navy', 'Knuckleball': 'black'}
markers = {'Fastball': 'o', 'Curveball': 'v', 'ChangeUp': 'd', 'Cutter': 'x', 'Slider': 's', 'Sinker': '1',
           'Splitter': '*', 'TwoSeamFastBall': '>', 'Knuckleball': '8'}

yTikMarks = [1.65, 2.32, 2.99, 3.65]
xTikMarks = [-0.71, -0.24, 0.24, 0.71]
strike_zone_color = 'black'

fence_x = [0, -226.98, -130.8461, 0, 130.8461, 226.98, 0]
fence_y = [0, 226.98, 346.0915, 395, 346.0915, 226.98, 0]

base_x = [0, -90 / sqrt(2), 0, 90 / sqrt(2), 0]
base_y = [0, 90 / sqrt(2), 90 * sqrt(2), 90 / sqrt(2), 0]

hit_color = {'Out': 'red', 'FieldersChoice': 'navy', 'Single': 'orange', 'Sacrifice': 'blue', 'Double': 'yellow',
             'Triple': 'purple', 'HomeRun': 'green', 'Error': 'cyan'}

result_color = {'StrikeCalled': 'red', 'StrikeSwinging': 'orange', 'FoulBall': 'yellow', 'InPlay': 'green',
                'BallCalled': 'blue', 'BallinDirt': 'brown', 'HitByPitch': 'purple'}

data_points = ['RelSpeed', 'SpinRate', 'Extension', 'RelHeight']
translation = {'RelSpeed': 'Velocity', 'SpinRate': 'Spin Rate', 'Extension': 'Extension', 'RelHeight': 'Release Height'}
units = {'RelSpeed': 'mph', 'SpinRate': 'rpm', 'Extension': 'ft', 'RelHeight': 'ft'}

for csv_file in CSV_FILES:
    df = pd.read_csv(csv_file)
    df = df[['Pitcher', 'PitcherTeam', 'TaggedPitchType', 'RelSpeed', 'SpinRate', 'Extension', 'RelHeight', 'HorzBreak',
             'InducedVertBreak', 'PitchCall', 'PlateLocHeight', 'PlateLocSide', 'PlayResult', 'Distance', 'Direction']]

    # Format the date this Trackman data was tabulated on
    date_index = len(csv_file) - csv_file[::-1].index('/')
    date = csv_file[date_index:date_index + 8]
    DATE = f'{date[4:6]}_{date[6:8]}_{date[:4]}'

    for name, pitcher in df.groupby(['Pitcher']):
        name = name[0].strip()

        # Create the new save folder to place all .png images in
        path = os.path.join(SAVE_FILE, name.replace(', ', '_'), DATE) if HOME_TEAM == pitcher['PitcherTeam'].values[0] \
            else os.path.join(SAVE_FILE, '_OPPONENTS', DATE, name.replace(', ', '_'))
        try:
            os.makedirs(path)
        except FileExistsError:
            path = path  # to skip to the rest of the program

        file_name = rf"{path}/{name.replace(', ', '_')}_{DATE}"

        # Building the Horizontal vs Vertical Break of each pitch scatter plot
        pitches = pitcher.groupby(['TaggedPitchType'])
        chart_made = False
        for pitch, g in pitches:
            pitch = pitch[0]
            if pitch != 'Undefined':
                plt.scatter(g['HorzBreak'], g['InducedVertBreak'], c=colors[pitch], marker=markers[pitch], label=pitch)
                chart_made = True

        if chart_made:
            plt.axvline(x=0, color='black', linestyle=':')
            plt.axhline(y=0, color='black', linestyle=':')
            plt.xlabel('Horizontal Break (in)')
            plt.ylabel('Vertical Break (in)')
            plt.title(f'Vertical and Horizontal Break by Pitch Type - {name}')
            plt.legend()
            plt.savefig(fname=f"{file_name}_pitch_breaks.png")
            plt.close()

        # Building the strike zone and pitch calls scatter plot
        results = pitcher.groupby(['PitchCall'])
        chart_made = False
        for call, g in results:
            call = call[0]
            if call != 'Undefined':
                plt.scatter(g['PlateLocSide'], g['PlateLocHeight'], c=result_color[call], marker='o', label=call)
                chart_made = True

        if chart_made:
            for x in xTikMarks:
                plt.plot([x, x], [yTikMarks[0], yTikMarks[-1]], color=strike_zone_color)
            for y in yTikMarks:
                plt.plot([xTikMarks[0], xTikMarks[-1]], [y, y], color=strike_zone_color)

            plt.xlabel('Horizontal Location (ft)')
            plt.ylabel('Vertical Location (ft)')
            plt.title(f'Pitch Location - {name}')
            plt.legend()
            plt.savefig(fname=f"{file_name}_strike_zone.png")
            plt.close()

        for d in data_points:
            fig, ax = plt.subplots()
            total_data, col_labels = [], []
            for pitch, group in pitches:
                pitch = pitch[0]
                if pitch != 'Undefined':
                    total_data.append(group[d])
                    col_labels.append(pitch)
            if len(total_data) > 0:
                ax.boxplot(total_data)
                ax.set_xticklabels(col_labels)
                ax.set_ylabel(f'{translation[d]} ({units[d]})')
                ax.set_title(f'{translation[d]} by Pitch - {name}')
                plt.savefig(fname=rf"{file_name}_{translation[d].replace(' ', '_')}.png")
            plt.close()

        plt.plot(fence_x, fence_y, color='black')
        plt.plot(base_x, base_y, color='black', marker='s')

        chart_made = False

        for result, r_data in pitcher.groupby(['PlayResult']):
            if 'Undefined' in result or 'Strikeout' in result:
                continue
            result = result[0]
            x_cords, y_cords = [], []
            for dis, dir in zip(r_data['Distance'].values, r_data['Direction'].values):
                if str(dis) == 'nan' or str(dir) == 'nan':
                    continue
                x_cords.append(dis * sin(radians(dir)))
                y_cords.append(dis * cos(radians(dir)))
            if len(x_cords) > 0:
                plt.scatter(x_cords, y_cords, color=hit_color[result], label=result, linewidths=0.5)
                chart_made = True

        if chart_made:
            plt.xlabel('Hit Location (ft)')
            plt.ylabel('Hit Location (ft)')
            plt.title(f'Spray Chart - {name}')
            plt.legend()
            plt.savefig(f'{file_name}_spray_chart.png')

        plt.close()

    print('Finished parsing:', csv_file)

if len(CSV_FILES) > 0:
    os.startfile(SAVE_FILE)
