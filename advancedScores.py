# WC 2022

# This program assumes that the user has advanced scores enabled on Anilist
# and also has put in scores for said advanced scores. It will only update
# anime entries marked as COMPLETED, CURRENTLY WATCHING, PAUSED, and DROPPED.

# 1. Request user login credentials to allow changes in profile
# 2. Fetch advanced score names from user
# 3. Take in user inputs for weights
# 4. Compute weighted score of title based on advanced scores from site
# 5. Mutate entry score in the server

# import tkinter as tk
# import tkinter.ttk as ttk
import json
import requests
import webbrowser
import math
from oauthlib.oauth2 import WebApplicationClient
from math import log10, floor

print("This program assumes that the user has advanced scores enabled on Anilist\n"
      "and also has put in scores for said advanced scores. It will only update\n"
      "anime entries marked as COMPLETED, CURRENTLY WATCHING, and PAUSED.")

# Create a formatted string of the Python JSON object
def jprint(obj):
  text = json.dumps(obj, indent=4)
  print(text)

# Rounds number to specified sigfig
def rounder(num, sigfig):
  return round(num, sigfig-int(floor(log10(abs(num))))-1)

# User Authentication

client_id = '8459'
client_secret = 'QvOHYXJT3J5sq88cdOMXPEI1uGKQj01ARoQ780tc'
redirect_uri = 'https://anilist.co/api/v2/oauth/pin'
client = WebApplicationClient(client_id)
authorization_url = 'https://anilist.co/api/v2/oauth/authorize?client_id=' \
                    + client_id + '&response_type=token'

url = client.prepare_request_uri(
  authorization_url,
  redirect_uri
)

data = client.prepare_request_body(
  redirect_uri,
  client_id,
  client_secret
)

webbrowser.open(authorization_url)
# Read in received token from user manually
token = input("Insert token: ")

graphql_url = 'https://graphql.anilist.co'

# -- VARIABLES --
# List holding the names of the scoring categories
category_names = []
# List holding the user assigned weights of the scoring categories
category_weights = []
# Authenticated user's name
auth_username = ""

# Obtain user's Username
query = '''
query {
  Viewer {
    name
  }
}
'''
# Header is used to make authenticated requests
header = {
    'Authorization': f'Bearer ' + str(token)
}
response = requests.post(graphql_url, json={'query': query}, headers=header)
response_parsable = response.json()
auth_username = response_parsable["data"]["Viewer"]["name"]
print("User: " + auth_username)

# Query to obtain names of advanced scoring sections and advanced
# scores of media (assuming the user's advanced scores are on)
query = '''
query($username: String) {
  User(name: $username) {
    mediaListOptions {
      animeList {
        advancedScoringEnabled
        advancedScoring
      }
    }
  }
  MediaListCollection(userName: $username, type: ANIME, status_not_in:[PLANNING]) {
    lists {
      entries {
        mediaId
        score
        advancedScores
      }
    }
  }
}
'''
variables = {
  "username": auth_username
}
# Make the HTTP API request
response = requests.post(graphql_url, json={'query': query, 'variables': variables})
response_parsable = response.json()

# Parse names of scoring categories and store in list
category_names = response_parsable["data"]["User"]["mediaListOptions"] \
                                  ["animeList"]["advancedScoring"]

while True:
  print("Please insert the weight of each scoring section, with the total weight = 1")
  i = 0
  while i < len(category_names):
    temp = float(input(category_names[i] + ': '))
    # Error checking
    if temp < 0 or temp > 1:
      print("Invalid weight. Must be greater than 0 and less than\n"
            "or equal to 1")
      continue
    category_weights.append(temp)
    i += 1
  
  temp_sum_weights = sum(category_weights)
  if temp_sum_weights == 1.0:
    break
  else:
    # Error checking
    print("\nTotal weight is not equal to 1\n"
          "Your total weight: " + str(temp_sum_weights) + "\n")
    category_weights = []

# TODO: Parse through media query and do the math (round to nearest hundredth)
# Loop through lists (in this order): CURRENTLY WATCHING, COMPLETED, PAUSED, DROPPED
# Prep strings for concatenation for final mutation request
args_str = '''mutation('''
data_str = ""
variables = {}
entry_counter = 0
for x in response_parsable["data"]["MediaListCollection"]["lists"]:
  # Loop through each media entry in each media watch status list ["entries"]
  status_category = x["entries"]
  for y in status_category:
    temp_adv_score_list = []
    weighted_score = 0
    # Only get entries already scored by the user
    if(y["score"] != 0):
      temp_adv_score_list = list(y["advancedScores"].values())
      # Calculate weighted score
      for j in range(len(category_names)):
        weighted_score += temp_adv_score_list[j] * category_weights[j]
      weighted_score = rounder(weighted_score, 2)

      entry_counter += 1
      id_str = "id_" + str(entry_counter)
      score_str = "score_" + str(entry_counter)
      entry_str = "entry_" + str(entry_counter)
      # Add mediaId and score to the mutation
      variables[id_str] = y["mediaId"]
      variables[score_str] = weighted_score
      args_str += '''
      ''' + "$" + id_str + ": Int,"
      args_str += '''
      ''' + "$" + score_str + ": Float,"
      # Use aliases to add a new media entry to the request
      data_str += '''
      ''' + entry_str + ": SaveMediaListEntry(mediaId: $" + id_str + ", score: $" + score_str \
      + ") {score}"

# Add ") {" after args_str is done (and also remove extra comma)
args_str = args_str[:-1]
args_str += ''') {
'''

# Avengers assemble the full request
query = args_str + data_str + '''
}'''
# print(variables)
# print(query)

# # Alternate between mediaID and score
# variables = {
#   "temp_id1": 131681,
#   "temp_score1": 9.56,
#   "temp_id2": 21519,
#   "temp_score2": 8.9
# }

# query = '''
# mutation(
#   $temp_id1: Int, 
#   $temp_score1: Float,
#   $temp_id2: Int,
#   $temp_score2: Float
# ) {
#   data1: SaveMediaListEntry(mediaId: $temp_id1, score: $temp_score1) {
#     score
#   }
#   data2: SaveMediaListEntry(mediaId: $temp_id2, score: $temp_score2) {
#     score
#   }
# }
# '''
# Header is used to make authenticated requests
header = {
    'Authorization': f'Bearer ' + str(token)
}
response = requests.post(graphql_url, json={'query': query, 'variables': variables}, headers=header)
print(response.status_code)

# # User input GUI
# root = tk.Tk()
# root.title("Anilist Advanced Scores")
# # Center the window
# window_width = 1000
# window_height = 800
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# center_x = int(screen_width / 2 - window_width / 2)
# center_y = int(screen_height / 2 - window_height / 2)
# root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
# root.resizable(False, False)
# root.iconbitmap("./images/amogus.ico")

# # UI

# # Ask user for inputs

# # Button to onfirm user inputs for scoring weights
# # and perform calculations
# def weights_button_clicked():
#     # TODO
#     print("fard")

# weights_button = ttk.Button(root, text="Done", command=weights_button_clicked)
# weights_button.pack(
#     ipadx = 10,
#     ipady = 10,
#     expand = True
# )

# # Start the GUI event loop
# root.mainloop()