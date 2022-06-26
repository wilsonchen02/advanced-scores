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
import webbrowser
from tkinter import messagebox as m_box
from typing import List

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

  access_token: tk.StringVar
  auth_username: str
  login_window: tk.Tk
  token_frame: ttk.LabelFrame
  token_label: ttk.Label
  token: str

  def __init__(self) -> None:
    self.login_window = None
    self.token_frame = None
    self.token_label = None
    self.access_token = None
    self.auth_username = None
    self.token = None
    self.setup()

  def setup(self) -> None:
    self.create_user_input_gui()
    self.create_description_box()
    self.create_button()
  
  def run(self) -> None:
    self.login_window.mainloop()


  def create_description_box(self) -> None:
    # Info about the app
    m_box.showinfo("Description", 
    "This program assumes that the user has advanced scores enabled on Anilist "
    "and also has put in scores for said advanced scores. It will only update "
    "anime entries marked as COMPLETED, CURRENTLY WATCHING, and PAUSED.")

  def create_login_window(self) -> None:
    self.login_window = tk.Tk()
    self.login_window.title("Anilist Advanced Scores")
    self.login_window.iconbitmap("./assets/amogus.ico")
    center_window(self.login_window)

  def create_token_frame(self) -> None:
    self.token_frame = ttk.LabelFrame(self.login_window, text = "Access Token")
    self.token_frame.grid(row = 0, column = 0, padx = 10, pady = 10)

  def create_token_label(self) -> None:
    self.token_label = ttk.Label(self.token_frame, text = "Enter token: ")
    self.token_label.grid(row = 0, column = 0)

  def create_input_box(self) -> None:
    self.access_token = tk.StringVar()
    input_box = ttk.Entry(self.token_frame, textvariable=self.access_token)
    input_box.grid(row=0, column=1)
    input_box.focus()

  def create_user_input_gui(self) -> None:
    self.create_login_window()
    self.create_token_frame()
    self.create_token_label()
    self.create_input_box()

  def login_button_callback(self) -> None:
    self.token = self.access_token.get()
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
      status_code = response.status_code
      login_response_parsable = response.json()

      self.auth_username = login_response_parsable["data"]["Viewer"]["name"]
      self.login_window.destroy()
    except:
      m_box.showerror("Error", f"Something went wrong.\n(Error Code: {status_code})")

  def create_button(self) -> None:
    token_button = ttk.Button(self.login_window, 
                              text = "OK",
                              command = self.login_button_callback)
    token_button.grid(row = 1, column = 1, padx = 5, pady = 5)

graphql_url = 'https://graphql.anilist.co'

class WeightsManager():

  category_weights: List[float]
  entries: List[ttk.Entry]
  token: str
  advanced_scores: str

  def __init__(self, token: str, advanced_scores: str, entries: ttk.Entry) -> None:
    self.category_weights = []
    self.entries = entries
    self.token = token
    self.advanced_scores = advanced_scores

  def is_entry_empty(self, entry: ttk.Entry) -> bool:
    return len(entry) == 0

  def is_entry_not_a_valid_decimal(self, entry: ttk.Entry) -> bool:
    return float(entry) < 0 or float(entry) > 1

  def create_category_weights_list(self) -> bool:
    self.category_weights = []
    for raw_entry in self.entries:
      entry = raw_entry.get()
      if self.is_entry_empty(entry):
        m_box.showerror("Error", f"Entry is missing a value.")
        return False
      elif self.is_entry_not_a_valid_decimal(entry):
        m_box.showerror("Error", f"Weights must be between 0 and 1 (inclusive).")
        return False
      else:
        self.category_weights.append(float(entry))
    if sum(self.category_weights) != 1:
        # Error check: total weight must be 1
        m_box.showerror("Error", f"Total weight must be equal to 1.\n"
                                  f"Your total weight: {sum(self.category_weights)}")
        return False
    return True

  def calculate_weighted_score(self, entry: ttk.Entry) -> float:
    advanced_scores = list(entry["advancedScores"].values())
    weighted_score = 0
    for j in range(len(self.category_weights)):
      weighted_score += advanced_scores[j] * self.category_weights[j]
    weighted_score = round(weighted_score, 1)
    return weighted_score

  def is_entry_not_scored(self, entry: ttk.Entry) -> bool:
    return entry["score"] == 0

  def weights_button_callback(self) -> None:
    try:    
      success = self.create_category_weights_list()
      if not success:
        return
      # Parse through media query and do the math (round to nearest hundredth)
      # Loop through lists (in this order): CURRENTLY WATCHING, COMPLETED, PAUSED, DROPPED
      # Prep strings for concatenation for final mutation request
      args_str = """mutation("""
      data_str = ""
      variables = {}
      entry_counter = 0

      for status_lists in self.advanced_scores["data"]["MediaListCollection"]["lists"]:
        entries = status_lists["entries"]

        for entry in entries:
          # Only get entries already scored by the user
          if(self.is_entry_not_scored(entry)):
            continue
          weighted_score = self.calculate_weighted_score(entry)
          # Variable names for the GraphQL query
          entry_counter += 1
          id_str = f"id_{entry_counter}"
          score_str = f"score_{entry_counter}"
          entry_str = f"entry_{entry_counter}"
          # Add mediaId and score to the mutation
          variables[id_str] = entry["mediaId"]
          variables[score_str] = weighted_score

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
          'Authorization': f'Bearer ' + str(self.token)
      }
      response = requests.post(graphql_url, json={'query': query, 'variables': variables}, headers=header)
      status_code = response.status_code
      # Result alert
      if int(status_code) == 200:
        m_box.showinfo("Alert", "Success!")
      else:
        m_box.showerror("Error", f"Something went wrong.\nError Code: {status_code}")
    except ValueError:
      m_box.showerror("Error", f"Value must be numeric.")
    except Exception as e:
      m_box.showerror("Error", f"Something went wrong." + str(e))

class WeightsWindow():

  weights_window: tk.Tk
  weights_description: ttk.Label
  user_label: ttk.Label
  weights_button: ttk.Button
  advanced_scores: str
  weights_manager: WeightsManager
  category_frame: ttk.LabelFrame
  auth_username: str
  token: str
  entries: List[ttk.Entry]

  def __init__(self, auth_username: str, token: str) -> None:
    self.weights_window = None
    self.weights_description = None
    self.user_label = None
    self.weights_button = None
    self.advanced_scores = None
    self.weights_manager = None
    self.category_frame = None
    self.auth_username = auth_username
    self.token = token
    self.entries = []
    self.setup()

  def setup(self) -> None:
    self.load_advanced_scores()  #creates self.advanced_scores
    self.create_weights_window()
    self.create_weights_description()
    self.create_category_inputs()  # creates self.entries
    self.weights_manager = WeightsManager(self.token, self.advanced_scores, self.entries)
    self.create_user_label()
    self.create_weights_button()

  def run(self) -> None:
    self.weights_window.mainloop()

  def create_category_inputs(self) -> None:
    category_names = self.get_category_names()
    self.entries = []
    # Make an entry for each category
    for i in range(len(category_names)):
      new_label = ttk.Label(self.category_frame, text = category_names[i])
      new_entry = ttk.Entry(self.category_frame)
      new_label.grid(row = i, column = 0, padx = 5, pady = 5)
      new_entry.grid(row = i, column = 1, padx = 5, pady = 5)

      # Add to lists as references
      self.entries.append(new_entry)

    self.entries[0].focus()

  def create_weights_button(self) -> None:
    self.weights_button = ttk.Button(
      self.weights_window, text = "OK",
      command = self.weights_manager.weights_button_callback
    )
    self.weights_button.grid(row = 3, column = 0, padx = 5, pady = 5)

  def create_weights_window(self) -> None:
    self.weights_window = tk.Tk()
    self.weights_window.title("Anilist Advanced Scores")
    self.weights_window.iconbitmap("./assets/amogus.ico")
    center_window(self.weights_window)
    self.create_category_frame()

  def create_weights_description(self) -> None:
    self.weights_description = ttk.Label(self.weights_window, text = \
      "Please insert the weight of each scoring section, with the total weight = 1")
    self.weights_description.grid(row = 0, column = 0, padx = 10, pady = 5)

  def create_user_label(self) -> None:
    self.user_label = ttk.Label(self.weights_window, text = f"User: {self.auth_username}")
    self.user_label.grid(row = 1, column = 0, padx = 10, pady = 0)

  def create_category_frame(self) -> None:
    self.category_frame = ttk.LabelFrame(self.weights_window, text = "Categories")
    self.category_frame.grid(row = 2, column = 0, padx = 10, pady = 10)


  def load_advanced_scores(self) -> None:
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
      "username": self.auth_username
    }
    # Make the HTTP API request
    response = requests.post(graphql_url, json={'query': query, 'variables': variables})
    self.advanced_scores = response.json()

  def get_category_names(self) -> List[str]:
    # Parse names of scoring categories and store in list
    return self.advanced_scores["data"]["User"]["mediaListOptions"]["animeList"]["advancedScoring"]


def main():
    my_application = MyApplication()
    my_application.run()


if __name__ == "__main__":
  main()