import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
from math import sqrt
from tqdm import tqdm

# Home team, formatted as tracked in Trackman
HOME_TEAM = 'SHE_UNI'  # Shenandoah University
# Dots Per Inch: describes how detailed the charts are | Increased DPI -> Increased detail/resolution -> Larger images
DPI = 200

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

    try:
        annual_df = pd.read_csv('all_data.csv')
    except FileNotFoundError:
        annual_df = pd.DataFrame()
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

    plt.plot(fence_x, fence_y, c=fence_color)
    plt.plot(base_x, base_y, c=base_color, marker='s')


def plot_strike_zone(color='black'):
    x_marks = [-0.71, -0.24, 0.24, 0.71]
    y_marks = [1.65, 2.32, 2.99, 3.65]

    for x, y in zip(x_marks, y_marks):
        plt.plot([x, x], [y_marks[0], y_marks[-1]], c=color)
        plt.plot([x_marks[0], x_marks[-1]], [y, y], c=color)


def pitches_and_hue(data: pd.DataFrame) -> (pd.DataFrame, str):
    hue = 'TaggedPitchType'
    pitches = data[data[hue] != 'Undefined']
    if len(pitches) == 0 and 'AutoPitchType' in data.columns:
        hue = 'AutoPitchType'
        pitches = data[data[hue] != 'Undefined']
    return pitches, hue


# Building the Horizontal vs Vertical Break of each pitch scatter plot
def horz_vert_break_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    pitches, hue = pitches_and_hue(data)
    if len(pitches) == 0:
        return

    sns.scatterplot(pitches, x='HorzBreak', y='InducedVertBreak', hue=hue)
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
    pitches, hue = pitches_and_hue(data)
    if len(pitches) == 0:
        return

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 7))
    for i in range(len(data_points)):
        dp = data_points[i]
        ax = axes[i // 2, i % 2]
        sns.violinplot(data=pitches, y=dp, hue=hue, ax=ax)
        ax.set_ylabel(units[dp])
        ax.set_title(translation[dp])
        ax.legend()
        ax.set_xticklabels([])

    fig.suptitle(f'Pitch Arsenal Summary - {name}')
    plt.subplots_adjust(wspace=0.2, hspace=0.2)
    plt.savefig(fname=f'{file_name}_arsenal_summary.png', dpi=DPI)


def spray_chart(name: str, data: pd.DataFrame, file_name: str) -> None:
    results = data[data['PlayResult'] != 'Undefined']
    results = results.dropna(axis=0, subset=['Distance', 'Direction'])
    if len(results) == 0:
        return

    results['Distance*sin(Direction)'] = results['Distance'] * np.sin(np.radians(results['Direction']))
    results['Distance*cos(Direction)'] = results['Distance'] * np.cos(np.radians(results['Direction']))

    sns.scatterplot(data=results, x='Distance*sin(Direction)', y='Distance*cos(Direction)', hue='PlayResult')
    plot_field()
    plt.xlabel('Hit Location (ft)')
    plt.ylabel('Hit Location (ft)')
    plt.title(f'Spray Chart - {name}')
    plt.legend()
    plt.savefig(fname=f'{file_name}_spray_chart.png', dpi=DPI)


def create_charts(name: str, date: str, pitcher_data: pd.DataFrame, save_file: str) -> None:
    date = date.replace('-', '_')
    name = name.replace(', ', '_')

    # Create the new save folder to place all .png images in
    path = os.path.join(save_file, name, date)
    if pitcher_data['PitcherTeam'].values[0] != HOME_TEAM:
        path = os.path.join(save_file, '_OPPONENTS', date, name)

    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    file_name = '_'.join((name, date))
    full_path = os.path.join(path, file_name)
    name = ' '.join(name.split('_')[::-1])

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
        date = str(date).strip()
        create_charts(name, date, pitcher_data, save_file)

    os.startfile(save_file)


if __name__ == '__main__':
    main()
