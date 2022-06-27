# WC 2022

# This program assumes that the user has advanced scores enabled on Anilist
# and also has put in scores for said advanced scores. It will only update
# anime entries marked as COMPLETED, CURRENTLY WATCHING, PAUSED, and DROPPED.

# 1. Request user login credentials to allow changes in profile
# 2. Fetch advanced score names from user
# 3. Take in user inputs for weights
# 4. Compute weighted score of title based on advanced scores from site
# 5. Mutate entry score in the server

import json
import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from tkinter import messagebox as m_box
from typing import List
from typing import Dict

import requests
from oauthlib.oauth2 import WebApplicationClient


def center_window(window_name: tk.Tk) -> None:
  win_width = window_name.winfo_reqwidth()
  win_height = window_name.winfo_reqheight()
  horiz_center = int(window_name.winfo_screenwidth()/2 - win_width/2)
  vert_center = int(window_name.winfo_screenheight()/2 - win_height/2)
  window_name.geometry("+{}+{}".format(horiz_center, vert_center))


class MyApplication():

  def __init__(self) -> None:
    pass

  def run(self) -> None:
    app_web_link = ApplicationWebsiteLink()
    app_web_link.run()
    login_window = LoginWindow()
    login_window.run()
    auth_username = login_window.auth_username
    token = login_window.token
    weights_window = WeightsWindow(auth_username, token)
    weights_window.run()


class ApplicationWebsiteLink():

  client_id: str
  authorization_url: str

  def __init__(self) -> None:
    self.client_id = '8459'
    self.authorization_url = f'https://anilist.co/api/v2/oauth/authorize?client_id={self.client_id}&response_type=token'

  def run(self) -> None:
    self.connect_app_to_api()
    self.open_anilist_website()

  def connect_app_to_api(self) -> None:
      client_secret = 'QvOHYXJT3J5sq88cdOMXPEI1uGKQj01ARoQ780tc'
      redirect_url = 'https://anilist.co/api/v2/oauth/pin'
      client = WebApplicationClient(self.client_id)
      client.prepare_request_uri(
        self.authorization_url,
        redirect_url
      )
      client.prepare_request_body(
        redirect_url,
        self.client_id,
        client_secret
      )

  def open_anilist_website(self) -> None:
    webbrowser.open(self.authorization_url)

class LoginWindow():

  auth_username: str
  token: str
  _access_token: tk.StringVar
  _login_window: tk.Tk
  _status_code: int
  _token_frame: ttk.LabelFrame
  _token_label: ttk.Label

  def __init__(self) -> None:
    self.auth_username = None
    self.token = None
    self._access_token = None
    self._login_window = None
    self._status_code = -1
    self._token_frame = None
    self._token_label = None
    self.setup()

  def setup(self) -> None:
    self._create_user_input_gui()
    self._create_description_box()
    self._create_button()
  
  def run(self) -> None:
    self._login_window.mainloop()

  def _create_description_box(self) -> None:
    # Info about the app
    m_box.showinfo("Description", 
    "This program assumes that the user has advanced scores enabled on Anilist "
    "and also has put in scores for said advanced scores. It will only update "
    "anime entries marked as COMPLETED, CURRENTLY WATCHING, and PAUSED.")

  def _create_login_window(self) -> None:
    self._login_window = tk.Tk()
    self._login_window.title("Anilist Advanced Scores")
    self._login_window.iconbitmap("./assets/amogus.ico")
    center_window(self._login_window)

  def _create_token_frame(self) -> None:
    self._token_frame = ttk.LabelFrame(self._login_window, text = "Access Token")
    self._token_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

  def _create_token_label(self) -> None:
    self._token_label = ttk.Label(self._token_frame, text = "Enter token: ")
    self._token_label.grid(row = 0, column = 0)

  def _create_input_box(self) -> None:
    self._access_token = tk.StringVar()
    input_box = ttk.Entry(self._token_frame, textvariable=self._access_token)
    input_box.grid(row=0, column=1)
    input_box.focus()

  def _create_user_input_gui(self) -> None:
    self._create_login_window()
    self._create_token_frame()
    self._create_token_label()
    self._create_input_box()

  def _login_button_callback(self) -> None:
    self.token = self._access_token.get()
    try:
      query = '''
      query {
        Viewer {
          name
        }
      }
      '''
      header = {
          'Authorization': f'Bearer ' + self.token
      }

      response = requests.post(graphql_url, json={'query': query}, headers=header)
      self._status_code = response.status_code
      login_response_parsable = response.json()

      self.auth_username = login_response_parsable["data"]["Viewer"]["name"]
      self._login_window.destroy()
    except:
      m_box.showerror("Error", f"Something went wrong.\n(Error Code: {self._status_code})")

  def _create_button(self) -> None:
    token_button = ttk.Button(self._login_window, 
                              text = "OK",
                              command = self._login_button_callback)
    token_button.grid(row = 1, column = 1, padx = 5, pady = 5)

graphql_url = 'https://graphql.anilist.co'

class WeightsManager():

  _advanced_scores: str
  _category_weights: List[float]
  _entries: List[ttk.Entry]
  _max_query_counter: int
  _status_code: int
  _token: str
  _variables: Dict

  def __init__(self, token: str, advanced_scores: str, entries: ttk.Entry) -> None:
    self._advanced_scores = advanced_scores
    self._category_weights = []
    self._entries = entries
    self._max_query_counter = 200
    self._status_code = -1
    self._token = token
    self._variables = {}

  # For debugging purposes
  def jprint(self, obj):
    text = json.dumps(obj, indent=4)
    print(text)

  def send_mutation_request(self, num_entries_to_send: int) -> None:
    args_str = """mutation("""
    data_str = ""

    # Loop through all the items in the dictionary
    for i in range(1, num_entries_to_send + 1):
      id_str = f"id_{i}"
      score_str = f"score_{i}"
      entry_str = f"entry_{i}"

      # Add new variables as arguments of the query
      args_str += f"\n${id_str}: Int,\n${score_str}: Float,"

      # Use aliases to add a new media entry to the request
      data_str += f"\n{entry_str}: SaveMediaListEntry(mediaId: ${id_str}, score: ${score_str}) " + "{score}"

    # Add ") {" after args_str is done (and also remove extra comma)
    args_str = args_str[:-1]
    args_str += ") {\n" 
    # Avengers assemble the full request
    query = f"{args_str}{data_str}" + "}" 

    # 3. THIRD PART IS SUBMITTING THE REQUEST
    # Header is used to make authenticated requests
    header = {
        'Authorization': f'Bearer ' + str(self._token)
    }

    response = requests.post(graphql_url, json={'query': query, 'variables': self._variables}, headers=header)
    self._status_code = response.status_code

    # Reset dictionary and counter 
    self._variables = {}
    num_entries_to_send = 0   # Should reset entry_counter 

  def weights_button_callback(self) -> None:
    try:    
      success = self._create_category_weights_list()
      if not success:
        return

      # Parse through media query and do the math (round to nearest tenth)
      # Loop through lists (in this order): CURRENTLY WATCHING, COMPLETED, PAUSED, DROPPED
      # Prep strings for concatenation for final mutation request
      
      self._variables = {}
      entry_counter = 0

      for status_lists in self._advanced_scores["data"]["MediaListCollection"]["lists"]:
        entries = status_lists["entries"]

        # TODO: query complexity should be set to limited, max cap is 500. Split into multiple requests
        for entry in entries:
          # Only get entries already scored by the user
          if(self._is_entry_not_scored(entry)):
            continue
          
          entry_counter += 1
          weighted_score = self._calculate_weighted_score(entry)

          # Load up entry's mediaId and score for the next request
          self._variables[f"id_{entry_counter}"] = entry["mediaId"]
          self._variables[f"score_{entry_counter}"] = weighted_score

          # Once it hits the max, send off what's in the dictionary
          if entry_counter >= self._max_query_counter:
            self.send_mutation_request(entry_counter)
            continue

      # Send out request for remaining changes
      self.send_mutation_request(entry_counter)
      
      # Result alert
      if int(self._status_code) == 200:
        m_box.showinfo("Alert", "Success!")
      else:
        m_box.showerror("Error", f"Something went wrong.\nError Code: {self._status_code}")
        # TODO: print error in message box
        
      
    except ValueError:
      m_box.showerror("Error", f"Value must be numeric.")
    except Exception as e:
      m_box.showerror("Error", f"Something went wrong." + str(e))

  def _calculate_weighted_score(self, entry: ttk.Entry) -> float:
    advanced_scores = list(entry["advancedScores"].values())
    weighted_score = 0
    for j in range(len(self._category_weights)):
      weighted_score += advanced_scores[j] * self._category_weights[j]
    weighted_score = round(weighted_score, 1)
    return weighted_score

  def _create_category_weights_list(self) -> bool:
    self._category_weights = []
    for raw_entry in self._entries:
      entry = raw_entry.get()
      if self._is_entry_empty(entry):
        m_box.showerror("Error", f"Entry is missing a value.")
        return False
      elif self._is_entry_not_a_valid_decimal(entry):
        m_box.showerror("Error", f"Weights must be between 0 and 1 (inclusive).")
        return False
      else:
        self._category_weights.append(float(entry))
    if sum(self._category_weights) != 1:
        # Error check: total weight must be 1
        m_box.showerror("Error", f"Total weight must be equal to 1.\n"
                                  f"Your total weight: {sum(self._category_weights)}")
        return False
    return True

  def _is_entry_empty(self, entry: ttk.Entry) -> bool:
    return len(entry) == 0

  def _is_entry_not_a_valid_decimal(self, entry: ttk.Entry) -> bool:
    return float(entry) < 0 or float(entry) > 1

  def _is_entry_not_scored(self, entry: ttk.Entry) -> bool:
    return entry["score"] == 0

class WeightsWindow():

  _advanced_scores: str
  _auth_username: str
  _category_frame: ttk.LabelFrame
  _entries: List[ttk.Entry]
  _token: str
  _user_label: ttk.Label
  _weights_button: ttk.Button
  _weights_description: ttk.Label
  _weights_manager: WeightsManager
  _weights_window: tk.Tk

  def __init__(self, auth_username: str, token: str) -> None:
    self._advanced_scores = None
    self._auth_username = auth_username
    self._category_frame = None
    self._entries = []
    self._token = token
    self._user_label = None
    self._weights_button = None
    self._weights_description = None
    self._weights_manager = None
    self._weights_window = None
    self._setup()

  def run(self) -> None:
    self._weights_window.mainloop()

  def _create_category_inputs(self) -> None:
    category_names = self._get_category_names()
    self._entries = []
    # Make an entry for each category
    for i in range(len(category_names)):
      new_label = ttk.Label(self._category_frame, text = category_names[i])
      new_entry = ttk.Entry(self._category_frame)
      new_label.grid(row = i, column = 0, padx = 5, pady = 5)
      new_entry.grid(row = i, column = 1, padx = 5, pady = 5)

      # Add to lists as references
      self._entries.append(new_entry)

    self._entries[0].focus()

  def _create_category_frame(self) -> None:
    self._category_frame = ttk.LabelFrame(self._weights_window, text = "Categories")
    self._category_frame.grid(row = 2, column = 0, padx = 10, pady = 10)

  def _create_user_label(self) -> None:
    self._user_label = ttk.Label(self._weights_window, text = f"User: {self._auth_username}")
    self._user_label.grid(row = 1, column = 0, padx = 10, pady = 0)

  def _create_weights_button(self) -> None:
    self._weights_button = ttk.Button(
      self._weights_window, text = "OK",
      command = self._weights_manager.weights_button_callback
    )
    self._weights_button.grid(row = 3, column = 0, padx = 5, pady = 5)

  def _create_weights_description(self) -> None:
    self._weights_description = ttk.Label(self._weights_window, text = \
      "Please insert the weight of each scoring section, with the total weight = 1")
    self._weights_description.grid(row = 0, column = 0, padx = 10, pady = 5)

  def _create_weights_window(self) -> None:
    self._weights_window = tk.Tk()
    self._weights_window.title("Anilist Advanced Scores")
    self._weights_window.iconbitmap("./assets/amogus.ico")
    center_window(self._weights_window)
    self._create_category_frame()

  def _get_category_names(self) -> List[str]:
    # Parse names of scoring categories and store in list
    return self._advanced_scores["data"]["User"]["mediaListOptions"]["animeList"]["advancedScoring"]

  def _load_advanced_scores(self) -> None:
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
      "username": self._auth_username
    }
    # Make the HTTP API request
    response = requests.post(graphql_url, json={'query': query, 'variables': variables})
    self._advanced_scores = response.json()

  def _setup(self) -> None:
    self._load_advanced_scores()  #creates self.advanced_scores
    self._create_weights_window()
    self._create_weights_description()
    self._create_category_inputs()  # creates self.entries
    self._weights_manager = WeightsManager(self._token, self._advanced_scores, self._entries)
    self._create_user_label()
    self._create_weights_button()


def main():
    my_application = MyApplication()
    my_application.run()


if __name__ == "__main__":
  main()