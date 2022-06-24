# Anilist Advanced Scores: Make changes by the bulk
This program assumes that the user has advanced scores enabled on Anilist
and also has put in scores for said advanced scores. It will only update
anime entries marked as COMPLETED, CURRENTLY WATCHING, PAUSED, and DROPPED.

1. Request user login credentials to allow changes in profile
2. Fetch advanced score names from user
3. Take in user inputs for weights
4. Compute weighted score of title based on advanced scores from site
5. Mutate entry score in the server

note: if you recently changed some advanced scores of an entry and the program is still open, 
please close and reopen the program before trying to update your weighted scores.
