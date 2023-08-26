import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog as fd
from math import sin, cos, radians, sqrt
import os
from tqdm import tqdm

# Colors and markers for plotting pitch types
colors = {'Fastball': 'red', 'Curveball': 'blue', 'ChangeUp': 'green', 'Slider': 'yellow', 'Cutter': 'brown',
          'Sinker': 'purple', 'Splitter': 'silver', 'TwoSeamFastBall': 'navy', 'Knuckleball': 'black'}
markers = {'Fastball': 'o', 'Curveball': 'v', 'ChangeUp': 'd', 'Cutter': 'x', 'Slider': 's', 'Sinker': '1',
           'Splitter': '*', 'TwoSeamFastBall': '>', 'Knuckleball': '8'}

xTikMarks = [-0.71, -0.24, 0.24, 0.71]
yTikMarks = [1.65, 2.32, 2.99, 3.65]
strike_zone_color = 'black'

fence_x = [0, -226.98, -130.8461, 0, 130.8461, 226.98, 0]
fence_y = [0, 226.98, 346.0915, 395, 346.0915, 226.98, 0]
fence_color = 'black'

base_x = [0, -90 / sqrt(2), 0, 90 / sqrt(2), 0]
base_y = [0, 90 / sqrt(2), 90 * sqrt(2), 90 / sqrt(2), 0]
base_color = 'black'

hit_color = {'Out': 'red', 'FieldersChoice': 'navy', 'Single': 'orange', 'Sacrifice': 'blue', 'Double': 'yellow',
             'Triple': 'purple', 'HomeRun': 'green', 'Error': 'cyan'}

result_color = {'StrikeCalled': 'red', 'StrikeSwinging': 'orange', 'FoulBall': 'yellow', 'InPlay': 'green',
                'BallCalled': 'blue', 'BallinDirt': 'brown', 'HitByPitch': 'purple'}

data_points = ['RelSpeed', 'SpinRate', 'Extension', 'RelHeight']
translation = {'RelSpeed': 'Velocity', 'SpinRate': 'Spin Rate', 'Extension': 'Extension', 'RelHeight': 'Release Height'}
units = {'RelSpeed': 'mph', 'SpinRate': 'rpm', 'Extension': 'ft', 'RelHeight': 'ft'}


def horz_vert_break_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    # Building the Horizontal vs Vertical Break of each pitch scatter plot
    pitches = data.groupby(['TaggedPitchType'])
    if len(pitches) == 0:
        pitches = data.groupby(['AutoPitchType'])

    chart_made = False
    for pitch, pitch_data in pitches:
        pitch = pitch[0]
        if pitch == 'Undefined':
            continue
        pitch_data.dropna(axis=0, subset=['HorzBreak', 'InducedVertBreak'], inplace=True)
        chart_made = chart_made or len(pitch_data) > 0
        plt.scatter(pitch_data['HorzBreak'], pitch_data['InducedVertBreak'], c=colors[pitch], marker=markers[pitch],
                    label=pitch)

    if not chart_made:
        return

    plt.axvline(x=0, color='black', linestyle=':')
    plt.axhline(y=0, color='black', linestyle=':')
    plt.xlabel('Horizontal Break (in)')
    plt.ylabel('Vertical Break (in)')
    plt.title(f'Vertical and Horizontal Break by Pitch Type - {name}')
    plt.legend()
    plt.savefig(fname=f"{file_name}_pitch_breaks.png")


def pitch_calls_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    # Building the strike zone and pitch calls scatter plot
    results = data.groupby(['PitchCall'])
    chart_made = False
    for call, pitch_data in results:
        call = call[0]
        if call == 'Undefined':
            continue
        pitch_data.dropna(axis=0, subset=['HorzBreak', 'InducedVertBreak'], inplace=True)
        chart_made = chart_made or len(pitch_data) > 0
        plt.scatter(pitch_data['PlateLocSide'], pitch_data['PlateLocHeight'], c=result_color[call], marker='o',
                    label=call)

    if not chart_made:
        return

    for x in xTikMarks:
        plt.plot([x, x], [yTikMarks[0], yTikMarks[-1]], color=strike_zone_color)
    for y in yTikMarks:
        plt.plot([xTikMarks[0], xTikMarks[-1]], [y, y], color=strike_zone_color)

    plt.xlabel('Horizontal Location (ft)')
    plt.ylabel('Vertical Location (ft)')
    plt.title(f'Pitch Location - {name}')
    plt.legend()
    plt.savefig(fname=f"{file_name}_strike_zone.png")


def pitch_summaries(name: str, data: pd.DataFrame, file_name: str) -> None:
    pitches = data.groupby(['TaggedPitchType'])
    if len(pitches) == 0:
        pitches = data.groupby(['AutoPitchType'])

    n_datasets_per_plot = int(pitches.ngroups)
    data_sets = []
    pitch_names = []

    for pitch, group in pitches:
        if 'Undefined' in pitch:
            continue
        data_sets.append([])
        pitch_names.append(pitch[0])
        for dp in data_points:
            d = group[dp]
            d.dropna(axis=0, inplace=True)
            data_sets[-1].append(d)

    if len(data_sets) == 0:
        return

    # Create subplots vertically
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9 + int(pitches.ngroups), 8))
    axes = axes.flatten()

    # Width of each violin plot
    width = 0.2

    # Keep track of unique legend artists
    legend_artists_dict = {}

    # Plot multiple violin plots in each subplot
    try:
        for i, ax in enumerate(axes):
            for j in range(n_datasets_per_plot):
                dataset = data_sets[j][i]
                color = colors[pitch_names[j]]

                # Calculate the position for the current violin
                pos = i + j * width - (n_datasets_per_plot - 1) * width / 2

                # Plot violin plot
                parts = ax.violinplot(dataset, positions=[pos], widths=width, showmeans=True)

                # Set properties for all lines
                for pc in parts['bodies']:
                    pc.set_facecolor(color)
                    pc.set_edgecolor('black')
                    pc.set_alpha(0.6)
                for part_name in ('cbars', 'cmaxes', 'cmins', 'cmeans'):
                    vp = parts[part_name]
                    vp.set_edgecolor('black')

                # Create an artist for the legend
                legend_key = (color, pitch_names[j])
                if legend_key not in legend_artists_dict:
                    legend_artists_dict[legend_key] = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color,
                                                                 markersize=10, label=pitch_names[j])

            ax.set_title(translation[data_points[i]])
            ax.set_xticklabels([])  # Hide the x-ticks bar
            ax.set_ylabel(units[data_points[i]])
    except IndexError:
        print(f'Error for {name} {data["Date"].values[0]}')
        return

    fig.suptitle(f'Pitch Arsenal Summary - {name}')
    fig.legend(handles=list(legend_artists_dict.values()), loc='center')
    plt.subplots_adjust(wspace=0.3, hspace=0.35)
    plt.savefig(f'{file_name}_arsenal_summary.png')


def spray_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    plt.plot(fence_x, fence_y, color=fence_color)
    plt.plot(base_x, base_y, color=base_color, marker='s')

    chart_made = False
    for result, r_data in data.groupby(['PlayResult']):
        result = result[0]
        if result in ['Undefined', 'Strikeout']:
            continue
        r_data.dropna(axis=0, subset=['Distance', 'Direction'], inplace=True)
        chart_made = chart_made or len(r_data) > 0
        x_cords, y_cords = [], []
        for distance, direction in zip(r_data['Distance'].values, r_data['Direction'].values):
            x_cords.append(distance * sin(radians(direction)))
            y_cords.append(distance * cos(radians(direction)))
        if len(x_cords) == 0:
            continue
        plt.scatter(x_cords, y_cords, color=hit_color[result], label=result)

    if not chart_made:
        return

    plt.xlabel('Hit Location (ft)')
    plt.ylabel('Hit Location (ft)')
    plt.title(f'Spray Chart - {name}')
    plt.legend()
    plt.savefig(f'{file_name}_spray_chart.png')


def create_charts(name: str, pitcher_data: pd.DataFrame) -> None:
    # Get the date of when the pitcher pitched
    date = pitcher_data['Date'].values[0]
    if '-' in date:
        date = date.replace('-', '_')
    if '/' in date:
        date = date.replace('/', '_')

    # Create the new save folder to place all .png images in
    path = os.path.join(SAVE_FILE, name.replace(', ', '_'), date) if HOME_TEAM == pitcher['PitcherTeam'].values[0] \
        else os.path.join(SAVE_FILE, '_OPPONENTS', date, name.replace(', ', '_'))
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    file_name = f"{name.replace(', ', '_')}_{date}"
    full_path = os.path.join(path, file_name)

    pitch_summaries(name, pitcher_data, full_path)
    plt.close()
    horz_vert_break_chart(name, pitcher_data, full_path)
    plt.close()
    pitch_calls_chart(name, pitcher_data, full_path)
    plt.close()
    spray_chart(name, pitcher_data, full_path)
    plt.close()


if __name__ == '__main__':
    # User's home team, formatted as tracked in Trackman
    HOME_TEAM = 'SHE_UNI'

    # Select the Trackman files that the user wants to visualize
    CSV_FILES = fd.askopenfilenames(filetypes=[('Trackman CSV Files', '*.csv')], title="Select Trackman Files")
    # Get the folder the user wants to save the data visualizations in (saved as .png images)
    SAVE_FILE = fd.askdirectory(mustexist=True, title="Select Save Folder") if len(CSV_FILES) > 0 else None

    if len(CSV_FILES) == 0 or len(SAVE_FILE) == 0:
        print('CSV files and a save folder are required')
        quit(1)

    if os.name == 'nt':
        SAVE_FILE = SAVE_FILE.replace('/', '\\')

    with tqdm(total=len(CSV_FILES), desc='Iterating through Trackman CSV Files') as bar:
        for csv_file in CSV_FILES:
            df = pd.read_csv(csv_file)

            # Add to the annual data pool
            df2 = pd.read_csv('year_long_data.csv')
            df2 = pd.concat([df, df2])
            df2.drop_duplicates(inplace=True)  # We can't have duplicate pitches
            df2.to_csv('year_long_data.csv', index=False)

            df = df[['Date', 'Time', 'Pitcher', 'PitcherTeam', 'TaggedPitchType', 'RelSpeed', 'SpinRate', 'Extension',
                     'RelHeight', 'HorzBreak', 'InducedVertBreak', 'PitchCall', 'PlateLocHeight', 'PlateLocSide',
                     'PlayResult', 'Distance', 'Direction']]

            for pitcher_name, pitcher in df.groupby(['Pitcher']):
                pitcher_name = pitcher_name[0].strip()
                create_charts(pitcher_name, pitcher)

            bar.update(1)

    os.startfile(SAVE_FILE)
