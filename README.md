# Anilist Advanced Scores: Make changes by the bulk
This program assumes that the user has advanced scores enabled on Anilist
and also has put in scores for said advanced scores. **It will only update
anime entries marked as COMPLETED, CURRENTLY WATCHING, PAUSED, and DROPPED.**

1. Request user login credentials to allow changes in profile
2. Fetch advanced score names from user
3. Take in user inputs for weights
4. Compute weighted score of title based on advanced scores from site
5. Mutate entry score in the server

# How to use it
1. Download files from this repository.

![image](https://user-images.githubusercontent.com/77934980/175571622-4f8b246c-5dd4-4541-8c4e-a1c705baebfd.png)

**Don't move the ```.exe``` file outside of the folder!**

2. Open the ```.exe``` file. A small window will pop up and you will also be redirected to an Anilist login.

![image](https://user-images.githubusercontent.com/77934980/175572852-cc6af3c3-1328-491b-b202-e87d2736b68f.png)

![image](https://user-images.githubusercontent.com/77934980/175572903-cd8ab6de-51dd-4a6a-9f08-69f7538d886b.png)

3. Log in and copy paste the key into the entry on the window.

![image](https://user-images.githubusercontent.com/77934980/175572981-84d3b1a6-80c0-4a27-a9f4-84f8e506bcb9.png)

![image](https://user-images.githubusercontent.com/77934980/175573196-1b565962-3250-4369-94ab-37b65a8a0190.png)

4. You're logged into your account now. Put in your weights for your categories and press OK when you're done.

![image](https://user-images.githubusercontent.com/77934980/175573433-33f38f1f-79e2-4464-825b-7d4c8d1ce91a.png)

5. Done! You can view your changes when you refresh your Anilist page. You can change your weights while the application window is still open.

*Note: If you recently changed some advanced scores of an entry and the program is still open, 
please close and reopen the program before trying to update your weighted scores.*

# Building the ```.exe```

For those who want to build the application itself, type this into Command Prompt:

```python3 -m PyInstaller --onefile advanced_scores.py```
