# WC 2022

# This program assumes that the user has advanced scores enabled on Anilist
# and also has put in scores for said advanced scores. It will only update
# anime entries marked as COMPLETED, CURRENTLY WATCHING, PAUSED, and DROPPED.

# 1. Request user login credentials to allow changes in profile
# 2. Fetch advanced score names from user
# 3. Take in user inputs for weights
# 4. Compute weighted score of title based on advanced scores from site
# 5. Mutate entry score in the server

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as m_box
import json
from unicodedata import category
import requests
import webbrowser
import math
from oauthlib.oauth2 import WebApplicationClient
from math import log10, floor

# -- VARIABLES --
# List holding the names of the scoring categories
category_names = []
# List holding the user assigned weights of the scoring categories
category_weights = []
label_list = []
entry_list = []
# Authenticated user's name
auth_username = ""
status_code = 0
global token

# Create a formatted string of the Python JSON object
def jprint(obj):
  text = json.dumps(obj, indent=4)
  print(text)

# Rounds number to specified sigfig
def rounder(num, sigfig):
  return round(num, sigfig-int(floor(log10(abs(num))))-1)

def center_window(window_name):
  win_width = window_name.winfo_reqwidth()
  win_height = window_name.winfo_reqheight()
  horiz_center = int(window_name.winfo_screenwidth()/2 - win_width/2)
  vert_center = int(window_name.winfo_screenheight()/2 - win_height/2)
  window_name.geometry("+{}+{}".format(horiz_center, vert_center))

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
# token = input("Insert token: ")

graphql_url = 'https://graphql.anilist.co'

# User input GUI
login_window = tk.Tk()
login_window.title("Anilist Advanced Scores")
login_window.iconbitmap("./assets/amogus.ico")

# Center the window
center_window(login_window)

token_frame = ttk.LabelFrame(login_window, text = "Access Token")
token_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
token_label = ttk.Label(token_frame, text = "Enter token: ")
token_label.grid(row = 0, column = 0)
access_token = tk.StringVar()
input_box = ttk.Entry(token_frame, textvariable=access_token)
input_box.grid(row=0, column=1)
input_box.focus()

# Info about the app
m_box.showinfo("Description", 
      "This program assumes that the user has advanced scores enabled on Anilist "
      "and also has put in scores for said advanced scores. It will only update "
      "anime entries marked as COMPLETED, CURRENTLY WATCHING, and PAUSED.")

# Attempt login button
def login_ok_btn():
  token = access_token.get()
  try:
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
    status_code = response.status_code
    response_parsable = response.json()
    global auth_username
    auth_username = response_parsable["data"]["Viewer"]["name"]
    print("User: " + auth_username)
    login_window.destroy()
  except:
    m_box.showerror("Error", f"Something went wrong.\n(Error Code: {status_code})")


token_button = ttk.Button(login_window, 
                          text = "OK",
                          command = login_ok_btn)
token_button.grid(column=1, row=1, padx = 5, pady = 5)

# Run login GUI
login_window.mainloop()

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

# Weights GUI
category_window = tk.Tk()
weights_description = ttk.Label(category_window, text = \
  "Please insert the weight of each scoring section, with the total weight = 1")
weights_description.grid(row = 0, column = 0, padx = 10, pady = 5)
category_frame = ttk.LabelFrame(category_window, text = "Categories")
category_frame.grid(row = 1, column = 0, padx = 10, pady = 10)

# Submit weight values button
def weights_ok_btn():
  try:
    # Add up the weights and see if = 1
    # Error check: make sure values are between 0 and 1
    temp_sum_weights = 0
    for i in range(len(entry_list)):
      temp = float(entry_list[i].get())
      if temp < 0 or temp > 1:
        m_box.showerror("Error", f"Weights must be between 0 and 1 (inclusive).")
      temp_sum_weights += temp
    
    # Error check: total weight must be 1
    if temp_sum_weights != 1:
      m_box.showerror("Error", f"Total weight must be equal to 1.")
    
    # TODO: OK button and the mutation
  except:
    m_box.showerror("Error", f"Something went wrong.\n(Error Code: {status_code})")

# Make an entry for each category
for i in range(len(category_names)):
  new_label = ttk.Label(category_frame, text = category_names[i])
  new_entry = ttk.Entry(category_frame)
  new_label.grid(row = i, column = 0, padx = 5, pady = 5)
  new_entry.grid(row = i, column = 1, padx = 5, pady = 5)

  # Add to lists as references
  label_list.append(new_label)
  entry_list.append(new_entry)

# Run weights GUI
category_window.title("Anilist Advanced Scores")
category_window.iconbitmap("./assets/amogus.ico")
center_window(category_window)
entry_list[0].focus()
category_window.mainloop()

# while True:
#   print("Please insert the weight of each scoring section, with the total weight = 1")
#   i = 0
#   while i < len(category_names):
#     temp = float(input(category_names[i] + ': '))
#     # Error checking
#     if temp < 0 or temp > 1:
#       print("Invalid weight. Must be greater than 0 and less than\n"
#             "or equal to 1")
#       continue
#     category_weights.append(temp)
#     i += 1
  
#   temp_sum_weights = sum(category_weights)
#   if temp_sum_weights == 1.0:
#     break
#   else:
#     # Error checking
#     print("\nTotal weight is not equal to 1\n"
#           "Your total weight: " + str(temp_sum_weights) + "\n")
#     category_weights = []

# # Parse through media query and do the math (round to nearest hundredth)
# # Loop through lists (in this order): CURRENTLY WATCHING, COMPLETED, PAUSED, DROPPED
# # Prep strings for concatenation for final mutation request
# args_str = '''mutation('''
# data_str = ""
# variables = {}
# entry_counter = 0
# for x in response_parsable["data"]["MediaListCollection"]["lists"]:
#   # Loop through each media entry in each media watch status list ["entries"]
#   status_category = x["entries"]
#   for y in status_category:
#     temp_adv_score_list = []
#     weighted_score = 0
#     # Only get entries already scored by the user
#     if(y["score"] != 0):
#       temp_adv_score_list = list(y["advancedScores"].values())
#       # Calculate weighted score
#       for j in range(len(category_names)):
#         weighted_score += temp_adv_score_list[j] * category_weights[j]
#       weighted_score = rounder(weighted_score, 2)

#       entry_counter += 1
#       id_str = "id_" + str(entry_counter)
#       score_str = "score_" + str(entry_counter)
#       entry_str = "entry_" + str(entry_counter)
#       # Add mediaId and score to the mutation
#       variables[id_str] = y["mediaId"]
#       variables[score_str] = weighted_score
#       args_str += '''
#       ''' + "$" + id_str + ": Int,"
#       args_str += '''
#       ''' + "$" + score_str + ": Float,"
#       # Use aliases to add a new media entry to the request
#       data_str += '''
#       ''' + entry_str + ": SaveMediaListEntry(mediaId: $" + id_str + ", score: $" + score_str \
#       + ") {score}"

# # Add ") {" after args_str is done (and also remove extra comma)
# args_str = args_str[:-1]
# args_str += ''') {
# '''

# # Avengers assemble the full request
# query = args_str + data_str + '''
# }'''

# # Header is used to make authenticated requests
# header = {
#     'Authorization': f'Bearer ' + str(token)
# }
# response = requests.post(graphql_url, json={'query': query, 'variables': variables}, headers=header)
# print(response.status_code)