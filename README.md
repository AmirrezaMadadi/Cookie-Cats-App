# Cookie-Cats-App
# Description
Cookie Cats is a hugely popular mobile puzzle game developed by Tactile Entertainment. It's a classic "connect three" style puzzle game where the player must connect tiles of the same color in order to clear the board and win the level. It also features singing cats.

# Goals
As players progress through the game they will encounter gates that force them to wait some time before they can progress or make an in-app purchase. In this project, we will analyze the result of an A/B test where the first gate in Cookie Cats was moved from level 30 to level 40. In particular, we will analyze the impact on player retention and game rounds.
We divide all the game players between two versions A (gate_30) and B (gate_40).

# Dataset Dictionary
| **Feature** | **Description** |
| ------------| ------------------------------ |
| userid | player ID (int) |
| version | Which version does the player belong to after division? (object) |
| sum_gamerounds | total played rounds (int) |
| retention_1 | retention after a day (bool) |
| retention_7 | retention after a week (bool) |

# Conclusion
According to the significance level as well as A/B testing, we came to the conclusion that if we show the ad in the 40th level, the average number of rounds played by the players will increase compared to when the ad is shown in We were showing the 30th level.

In addition to changing the place where the ad is displayed, it is better to consider a reward related to the game for the person who opens the link in exchange for seeing the ad. In this case, the satisfaction of the players will increase.


