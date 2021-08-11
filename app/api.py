#%% imports
import requests
import json

#%%variables that you might want to change on different runs
# user_name = 'nico_nttw_25'  #put name of person whose info/clan you want to explore
user_name = 'nico_abcd'  #put name of person whose info/clan you want to explore
user_platform = 'pc'  #either 'psn' or 'ps4' or 'xbone' or 'xbox'  (pc is busted)
save_to_file = 0  #flag: set to 1 if you want certain bits saved to file to peruse
membership_types = {'xbox': '1', 'psn': '2', 'pc': '3'}
user_id = ""
membership_id = ""

#%% fixed parameters
my_api_key = "9dfbe83d70da4ce49a92768e39571715"
baseurl = 'https://bungie.net/Platform/Destiny2/'
baseurl_groupv2 = 'https://bungie.net/Platform/GroupV2/'

#%% main function
def destiny2_api_public(url,api_key):
    my_headers = {"X-API-Key":api_key}
    response = requests.get(url, headers = my_headers)
    return response

def get_search_player_url():
    memType = membership_types[user_platform]
    url = "{0}{1}/{2}/{3}/".format(baseurl,'SearchDestinyPlayer',memType, user_name)
    return url
#%%###########################################
#    END FUNCTIONS AND CLASS DEFINITIONS     #
##############################################

if __name__ == '__main__':
    search_player_url = get_search_player_url()
    player_summary = destiny2_api_public(search_player_url, my_api_key).json()
    membership_id = player_summary["Response"][0]["membershipId"]
    print(membership_id)

# %%
