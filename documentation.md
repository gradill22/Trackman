# Required Files and Directories

This script is strictly designed to take `.csv` Trackman data. Do _not_ tamper with the data, remove data, delete or clear any rows or columns, or anything else to falsely manipulate the data. Let the script to the work for you.

If the `.csv` Trackman files don't contain the proper headers or rows, it will either fail and not generate any visualizations or the visualizations it does create will be inaccurate to the pitcher's true pitching.

There is no default location to save all the visualizations. Therefore, select a folder or directory to save the visualizations.

# Parameters

There are two parameters at the start of the Python script: `HOME_TEAM` and `DPI`.

## `HOME_TEAM`

This variable stores the home team as formatted in Trackman. This will determine where a pitcher's visualizations will be saved.
* EX: Shenandoah University -> "SHE_UNI"

To insert a different team name, insert the Trackman formatted name between the quotation (") marks. You can find this code within the data at the top of the `HomeTeam` column if you are the home team or the `AwayTeam` column if you are the away team.

## `DPI` (*optional*)

**DPI = Dots Per Inch**

This optional parameter describes how detailed the visualizations will be. The more dots, the better the visualization. However, this could cause memory issues as it would require larger `.png` files to save the visualiztions in. The default is 200 DPI. To change the DPI, replace 200 with a positive integer.

# File organization

Visualizations will be saved in a location based on what the program's `HOME_TEAM` parameter is set to. If a pitcher is part of the `HOME_TEAM`, the visualizations will be saved at:
* `../Given-Save-Directory/Last_First/YYYY_MM_DD/Last_First_YYYY_MM_DD_..._.png`

If a pitcher is not part of the `HOME_TEAM`, the visualizations will be saved at:
* `../Given-Save-Directory/_OPPONENTS/Last_First/YYYY_MM_DD/Last_First_YYYY_MM_DD_..._.png`

The rest of the file's name will be named in accordance with the visualization that it saves.

# Data Visualizations

There are four visualizations that are generated for every pitcher and every one of their outings.

## Arsenal Summary

**Saved as: `Last_First_YYYY_MM_DD_arsenal_summary.png`**

This chart visualizes the velocity, spin rate, extension, and release height of each pitcher's pitch. The data is presented across four different violin plot graphs, each visualizing one of the listed measurements above. The pitches are presented side-by-side in each of the violin plots.

### Why Violin Plots?

Violin plots are very similar to box and whisker plots in nature. They show maximum, minimum, and mean. The advantage of violin plots is that they better show the spread and frequency of data. Box and whisker plots have very straight edges because they only care about showing the spread of the data. Violin plots show just that and the data's frequency. This better shows where a pitcher's tendencies are with their pitches at release than a standard box plot.

### What to look for

The first thing to look for overall is the variance between a pitcher's arsenal. For example, if all the heights of the violin plots in a pither's velocity chart are different, that shows they have good speed variance. If all the velocity violin plots are similar in height, the pitcher's speed variance is a weak point. This can be applied to velocity and spin rate. The opposite should be applied to extension and release height to create the tunnel effect of pitching.

The second thing to look for is the frequency visualized in the violin plots. Is there one consistent bubble around the middle? Or are there two bubbles? Are there three? Multiple bubbles in the violin plots can be attributed to inconsistent arm path, pitching fatigue, and many other factors. The less bubbles, the better.

### Example
![ex1](Sample%20Visualizations/Dillon_Grady/2023_04_25/Dillon_Grady_2023_04_25_arsenal_summary.png)

#### Overall

In this chart, the pitcher throws a changeup, fastball, and slider. Generally speaking, it looks like all the violin plots are at different heights. For velocity and spin rate, this is good. For extension and release height, this is poor.

#### Velocity

The pitcher has good speed variance. There are three pitches that go at three different speeds. The fastball is the fastest, the changeup is slightly but significantly slower, and the slider is the slowest. The fastball has one large bubble and a slight second bubble at the bottom of the violin plot. This might be attributed to arm fatigue. The slider has three bubbles, which can more than likely be attributed to a combination of arm fatigue and inconsistent arm path. The changeup looks optimal with one consistent bubble.

#### Spin Rate

The spin rate chart shows exceptional spin on the slider and fastball. The slider peaked north of 2600 rpm while the fastball sat between 2200 and 2300 rpm. The changeup was consistently slower than the fastball and slider. This could be both advantageous and a weakness. Less spin could mean more vertical drop on the pitch, but it could also set it so far apart from the other pitches that hitters could easily pick up on it. The bubbles of data across all three violin charts are pretty conistent, showing consistent spin on the pitches.

#### Extension

The extension chart shows the fastball and changeup being thrown from a consistent distance while the slider is thrown much further back. All the violin plots have multiple bubbles, showing signs of an inconsistent arm path between pitches and general arm fatigue. This is most pronounced with the fastball.

#### Release Height

The release height chart shows the fastball and slider were thrown from mostly consistent heights while the changeup was significantly lower. The disparity between the changeup's release height and the rest of the pitches' release heights could make it easy for hitters to pick up. The fastball and changeup both have multiple bubbles while the slider has a mostly consistent release height.

### Conclusion

According to this visualization, the pitcher needs to work more on a consistent arm path with all three of his pitches. He has good speed variance and mostly good spin on each pitch. The pitcher does not tunnel his pitches well, especially with the changeup. Once a more consistent arm path is found across his arsenal, this pitcher will be much more effective.

## Pitch Breaks

**Saved as: `Last_First_YYYY_MM_DD_pitch_breaks.png`**

The pitch breaks chart shows each pitch’s horizontal and vertical breaks. The breaks are visualized to show how the pitches break from the pitcher’s perspective facing home plate.

### What to look for

The less overlap between pitches, the better. If pitches are overlapping, that means they move in a similar way. If they move the same way, the only difference is their speed. If they’re at the same speed, it’s just the same pitch. Look for each pitch to be in their own area of the chart.

### Example
![ex2](Sample%20Visualizations/Dillon_Grady/2023_04_25/Dillon_Grady_2023_04_25_pitch_breaks.png)

#### Overall

This pitcher has unique movement with each of his pitches. The fastball and slider are pretty scattered while the changeup is more concentrated and consistent.

#### Fastball

The fastball runs horizontally anywhere from 0 to 16 inches. The movement itself isn’t too consistent, but it’s unique enough to be effective. The same can be said for its vertical movement, running anywhere from 10 to 18 inches.

#### Slider

The slider very consistently breaks between 20 and 30 inches horizontally. It looks like there’s a fair concentration of vertical movement just below the 0-inch mark, adding some drop to the pitch. Like the fastball, the vertical movement is pretty scattered from -3 to 11 inches of vertical break.

#### Changeup

The changeup consistently moves horizontally by about 20 inches or so. It has a consistent vertical movement of about -3 inches with the exception of an outlier. Overall, the movement on the changeup is consistent both horizontally and vertically.

### Conclusion

The fastball and slider need to have more consistent movement. The fastball needs more consistent vertical and horizontal movement while the slider needs to have more consistent vertical movement. The changeup is mostly consistent. To be a more effective pitcher, find a more consistent finish with each pitch at release.

## Spray Chart

**Saved as: `Last_First_YYYY_MM_DD_spray_chart.png`**

The spray chart shows where balls in play were hit and the results of each fielding opportunity. This chart helps visualize how an opposing offense hits against a pitcher. This specific spray chart visualizes where balls are put in play at Kevin Anderson Field at Bridgeforth Stadium. The outfield fence dimensions from point to point are as follows: 321, 370, 395, 370, and 321 feet.

### What to look for

This is a great chart to show offensive tendencies against a pitcher. Look for where there is a concentration of balls in play, or if the balls in play are spread out. Concentrations of balls in play show that hitters can track a pitcher’s pitches (or one of the pitcher’s pitches) pretty consistently and put it in play. Spread-out balls in play may not be very helpful to analyze, as each hitter is unique and each one could be hitting to their strengths in each of their at-bats and spreading the team’s balls in play across the field. When the balls in play are spread out, it’s best to look at the result of each ball in play.

### Example
![ex3](Sample%20Visualizations/Dillon_Grady/2023_04_25/Dillon_Grady_2023_04_25_spray_chart.png)

#### Overall

Generally speaking, the balls that were put in play were pretty spread out. There was a strong tendency to hit balls in the outfield and drive it up the middle of the field. All balls beyond the infield were hit within the gaps.

### Conclusion

Compared to the two groundballs that were put in play, most contact was barreled up. This is a good indication that the pitcher has a tendency to miss his spots over the plate. This pitcher will be much more effective when he begins to consistently hit more of his spots and not leave any balls over the plate.

## Strike Zone

**Saved as: `Last_First_YYYY_MM_DD_strike_zone.png`**

The Strike Zone chart visualizes the coordinates of every pitch and their results. The strike zone is visualized from the perspective of the pitcher facing home plate. A batter’s box is drawn in the chart to show where the strike zone is. The horizontal dimensions of the strike zone are correct, but the vertical dimensions of the strike zone are based on the average hitter. The bottom of the strike zone is 1.65ft above the ground, and the top of the strike zone is 3.65ft above the ground.

### What to look for

Where are the pitches hitters putting in play? Where are the pitches hitters are taking? Where are the pitches they swing and miss at? There are a lot of things someone can analyze in charts like this, and it’s very open to interpretation. This chart visualizes four factors: pitch location, hitting tendencies, catching tendencies, and umpire tendencies. There is a balance between all four.

### Example
![ex4](Sample%20Visualizations/Dillon_Grady/2023_04_25/Dillon_Grady_2023_04_25_strike_zone.png)

#### Overall

There were a lot of pitches that were missed outside the zone low and away. In fact, it looks like that’s where most of the pitches were. There was hardly any foul ball contact or pitches swung at. Most of the pitches were called or put in play.

### Conclusion

The umpire was calling a lot of pitches low and off the plate. This is a good reason for missing so much out there as well. A couple of those strike calls were nearly a foot off the plate. It makes sense to throw pitches there a whole lot. Most of the balls put in play were low in the zone with only a few up in the zone. This could be because most of the pitches were low in the zone anyway. Pitches fouled away were very scattered throughout the strike zone, so it’s hard to tell if they were well-executed pitches or not. Overall, the pitcher did a good job of pitching low in the zone and taking advantage of the umpire’s low and away strike zone. To improve, he needs to be more competitive with his pitching and not throw balls over two feet off the plate.
