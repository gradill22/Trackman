import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
from math import sin, cos, radians, sqrt
from tqdm import tqdm

# Home team, formatted as tracked in Trackman
HOME_TEAM = 'SHE_UNI'  # Shenandoah University
# Dots Per Inch: describes how detailed the charts are | Increased DPI -> Increased detail/resolution -> Larger images
DPI = 200

# Colors and markers for plotting pitch types
colors = {'Fastball': 'red', 'Curveball': 'blue', 'ChangeUp': 'green', 'Changeup': 'green', 'Slider': 'yellow',
          'Cutter': 'brown', 'Sinker': 'purple', 'Splitter': 'silver', 'TwoSeamFastBall': 'navy',
          'Knuckleball': 'black'}
markers = {'Fastball': 'o', 'Curveball': 'v', 'ChangeUp': 'd', 'Changeup': 'd', 'Cutter': 'x', 'Slider': 's',
           'Sinker': '1', 'Splitter': '*', 'TwoSeamFastBall': '>', 'Knuckleball': '8'}

hit_color = {'Out': 'red', 'FieldersChoice': 'navy', 'Single': 'orange', 'Sacrifice': 'blue', 'Double': 'yellow',
             'Triple': 'purple', 'HomeRun': 'green', 'Error': 'cyan'}

result_color = {'StrikeCalled': 'red', 'StrikeSwinging': 'orange', 'FoulBall': 'yellow', 'InPlay': 'green',
                'BallCalled': 'blue', 'BallinDirt': 'brown', 'HitByPitch': 'purple'}

data_points = ['RelSpeed', 'SpinRate', 'Extension', 'RelHeight']
translation = {'RelSpeed': 'Velocity', 'SpinRate': 'Spin Rate', 'Extension': 'Extension', 'RelHeight': 'Release Height'}
units = {'RelSpeed': 'mph', 'SpinRate': 'rpm', 'Extension': 'ft', 'RelHeight': 'ft'}


def get_select_data():
    # Select the Trackman files to visualize
    csv_files = fd.askopenfilenames(filetypes=[('Trackman CSV Files', '*.csv')], title="Select Trackman Files")
    # Select the folder the visualizations will be saved in (saved as .png images)
    save_file = fd.askdirectory(mustexist=True, title="Select Save Folder") if len(csv_files) > 0 else None

    if len(csv_files) == 0 or len(save_file) == 0:
        print('Both the *.csv files and a save folder are required')
        quit(1)

    # Change file path to Windows compatible separator if running on Windows
    if os.name == 'nt':
        save_file = save_file.replace('/', '\\')

    annual_df = pd.read_csv('all_data.csv')
    total_df = pd.DataFrame()

    for csv_file in tqdm(csv_files, desc='Compiling data'):
        df = pd.read_csv(csv_file)
        annual_df = pd.concat([annual_df, df])
        df = df[['PitchNo', 'Date', 'Time', 'Pitcher', 'PitcherTeam', 'TaggedPitchType', 'RelSpeed', 'SpinRate',
                 'Extension', 'RelHeight', 'RelSide', 'VertRelAngle', 'HorzRelAngle', 'VertBreak', 'HorzBreak',
                 'InducedVertBreak', 'VertApprAngle', 'HorzApprAngle', 'PitchCall', 'PlateLocHeight', 'PlateLocSide',
                 'PlayResult', 'Distance', 'Direction']]
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.date
        total_df = pd.concat([df, total_df])

    annual_df.drop_duplicates(inplace=True)  # We can't have duplicate pitches
    annual_df.to_csv('all_data.csv', index=False)

    return save_file, total_df


def plot_field(fence_color='black', base_color='black'):
    # Kevin Anderson Field at Bridgeforth Stadium field dimensions
    fence_x = [0, -226.98, -130.8461, 0, 130.8461, 226.98, 0]
    fence_y = [0, 226.98, 346.0915, 395, 346.0915, 226.98, 0]

    base_x = [0, -90 / sqrt(2), 0, 90 / sqrt(2), 0]
    base_y = [0, 90 / sqrt(2), 90 * sqrt(2), 90 / sqrt(2), 0]

    plt.plot(fence_x, fence_y, color=fence_color)
    plt.plot(base_x, base_y, color=base_color, marker='s')


def plot_strike_zone(color='black'):
    x_marks = [-0.71, -0.24, 0.24, 0.71]
    y_marks = [1.65, 2.32, 2.99, 3.65]

    for x in x_marks:
        plt.plot([x, x], [y_marks[0], y_marks[-1]], c=color)
    for y in y_marks:
        plt.plot([x_marks[0], x_marks[-1]], [y, y], c=color)


# Building the Horizontal vs Vertical Break of each pitch scatter plot
def horz_vert_break_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    sns.scatterplot(data, x='HorzBreak', y='InducedVertBreak', hue='TaggedPitchType')
    plt.axvline(x=0, color='black', linestyle=':')
    plt.axhline(y=0, color='black', linestyle=':')
    plt.xlabel('Horizontal Break (in)')
    plt.ylabel('Vertical Break (in)')
    plt.title(f'Vertical and Horizontal Break by Pitch Type - {name}')
    plt.legend()
    plt.savefig(fname=f"{file_name}_pitch_breaks.png", dpi=DPI)


# Building the strike zone and pitch calls scatter plot
def pitch_calls_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    sns.scatterplot(data, x='PlateLocSide', y='PlateLocHeight', hue='PitchCall')
    plot_strike_zone()
    plt.xlabel('Horizontal Location (ft)')
    plt.ylabel('Vertical Location (ft)')
    plt.title(f'Pitch Location - {name}')
    plt.legend()
    plt.savefig(fname=f"{file_name}_strike_zone.png", dpi=DPI)


def pitch_summaries(name: str, data: pd.DataFrame, file_name: str) -> None:
    pitches = data.groupby(['TaggedPitchType'])
    if len(pitches) == 0:
        pitches = data.groupby(['AutoPitchType'])

    n_datasets_per_plot = int(pitches.ngroups)
    data_sets = []
    pitch_names = []

    for pitch, group in pitches:
        pitch = pitch[0].strip()
        if pitch == 'Undefined':
            continue
        data_sets.append([])
        pitch_names.append(pitch)
        for dp in data_points:
            d = group[dp]
            d.dropna(axis=0, inplace=True)
            data_sets[-1].append(d)

    if len(data_sets) == 0:
        return

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(7 + int(pitches.ngroups), 7))
    axes = axes.flatten()

    width = 0.2
    legend_artists_dict = {}

    # Plot multiple violin plots in each subplot
    try:
        for i, ax in enumerate(axes):
            for j in range(n_datasets_per_plot):
                dataset = data_sets[j][i]
                color = colors[pitch_names[j]]

                # Calculate the position for the current violin
                pos = i + j * width - (n_datasets_per_plot - 1) * width / 2

                parts = ax.violinplot(dataset, positions=[pos], widths=width, showmeans=True)

                # Change all line colors to black
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
        return

    fig.suptitle(f'Pitch Arsenal Summary - {name}')
    fig.legend(handles=list(legend_artists_dict.values()), loc='right')
    plt.subplots_adjust(wspace=0.2, hspace=0.2)
    plt.savefig(f'{file_name}_arsenal_summary.png', dpi=DPI)


def spray_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    results = data.groupby(['PlayResult'])

    chart_made = False
    for result, r_data in results:
        result = result[0].strip()
        if result == 'Undefined':
            continue
        r_data.dropna(axis=0, subset=['Distance', 'Direction'], inplace=True)
        if len(r_data) == 0:
            continue
        x_cords, y_cords = [], []
        for distance, direction in zip(r_data['Distance'].values, r_data['Direction'].values):
            x_cords.append(distance * sin(radians(direction)))
            y_cords.append(distance * cos(radians(direction)))
        plt.scatter(x_cords, y_cords, color=hit_color[result], label=result)
        chart_made = True

    if not chart_made:
        return

    plot_field()
    plt.xlabel('Hit Location (ft)')
    plt.ylabel('Hit Location (ft)')
    plt.title(f'Spray Chart - {name}')
    plt.legend()
    plt.savefig(f'{file_name}_spray_chart.png', dpi=DPI)


def create_charts(name: str, date: str, pitcher_data: pd.DataFrame, save_file: str) -> None:
    # Create the new save folder to place all .png images in
    path = os.path.join(save_file, name.replace(', ', '_'), date)
    if pitcher_data['PitcherTeam'].values[0] != HOME_TEAM:
        path = os.path.join(save_file, '_OPPONENTS', date, name.replace(', ', '_'))

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


def main():
    save_file, df = get_select_data()

    pitchers = df.groupby(['Pitcher', 'Date'])
    for name_and_date, pitcher_data in tqdm(pitchers, desc='Generating visualizations'):
        name, date = name_and_date
        name = str(name).strip()
        date = str(date).replace('-', '_').strip()
        create_charts(name, date, pitcher_data, save_file)

    os.startfile(save_file)


if __name__ == '__main__':
    main()
