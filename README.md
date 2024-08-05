# Visualizing Trackman Pitching Data
This python script ``pitchers.py`` visualizes given Trackman data for every pitcher of every game.

## How to use
Below are the instructions for how to use the Python script to visualize the pitching data from Trackman.

### 1) Configure home team
Before executing the program, you need to change the ``HOME_TEAM`` variable at the top of the script with the Trackman code for your team. To find this code, go to the ``HomeTeam`` column of your Trackman data. Assuming you are the home team, your code will be the first one listed. If you are the away team, find the ``AwayTeam`` column of the Trackman data and your code should be the first one listed. This will make sure your pitchers have priority when saving to your system.
#### Optional
You may also change the ``DPI`` variable to change the resolution of your visualizations. A larger DPI means larger files and visualizations, and a lower DPI means smaller files and visualizations. By default, ``DPI`` is set to 200.

### 2) Execute the program
### 3) Select all Trackman ``.csv`` files for visualization
Your file manager will open asking for all the data you need to visualize. The script strictly requires ``.csv`` files (for now).

### 4) Select destination folder
Your file manager will open once more asking where you would like to save these visualizations. Choose any folder at your convenience.

## Results
Once the program has finished, it will automatically open your destination folder (see step 4 in "How to use") where all of your visualizations will be saved. The folder's will be organized as such:

```
Home team pitcher -> Game day -> Visualizations
Opponents -> Game day -> Opponent pitchers -> Visualizations
```

## See Also
|                                                Link                                                |                                    Description                                   |
|:---------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|
| [Sample Visualizations](https://github.com/gradill22/Trackman/tree/master/Sample%20Visualizations) | See ``Sample Visualizations/Dillon_Grady/2023_04_25`` for the best examples      |
| [Visualization Documentation](https://github.com/gradill22/Trackman/blob/master/Documentation.pdf) | Everything you need to know about each type of visualization the script produces |
