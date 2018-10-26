# PredictingNBAPlayerGrowth

Every NBA team, fan, and analyst wants to know how well a players will play together. The first step is to understand how well a player will do in the future. Recognizing the complexities of player performance, this project aims to predict player performance and tendencies in key aspects of the game.

I began the project with data collection, and continued it time there was a need for more statistics. Hundreds of statistics of individual player data was taken from the NBA’s website and some data required to evaluate different plays was taken from Basketball-Reference.

To determine a clear target, I explored non-overlapping play types that were tracked and helped define a player’s game. To calculate the expected value of the different play types, I had to determine the value of all possible outcomes using a number of different stats. Next, I analyzed the targets through their correlation with team performance in win, offense, and defense.

Using the NBA player statistics, I created weighted features that took a player’s accounted for a player’s past performance and per minute stats that separated minutes played from performance. For each target, I closely examined the most related features using graphs, functions I created, and feature selection tools from scikit-learn.

For each target, multiple models were tested and optimized. In the end, linear regression or a form of regularized regression was used due to model performance and maximum interpretability.

The models determining rates were able to explain around 70% of the target variance, while models determining expected value were able to explain around 15% of the target variance. When the model were compared to baseline predictions, the expected value models had the greater value by improving on the baselines by 14 - 26%. 

In the future, these predictions could be used to determine optimal lineups, player signings, and areas for players to improve. Still, to better understand the model, it would help to understand how much of the variance of year to year performance is due to random chance. Also, it is important to make predictions for defense to create a more complete picture.
