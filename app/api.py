#%% imports
import requests
import json

#%%variables that you might want to change on different runs
user_name = 'nico_NTtW_25'  #put name of person whose info/clan you want to explore
user_platform = 'psn'  #either 'psn' or 'ps4' or 'xbone' or 'xbox'  (pc is busted)
save_to_file = 0  #flag: set to 1 if you want certain bits saved to file to peruse

#%% fixed parameters
my_api_key = "9dfbe83d70da4ce49a92768e39571715"
baseurl = 'https://bungie.net/Platform/Destiny2/'
baseurl_groupv2 = 'https://bungie.net/Platform/GroupV2/'
membership_types = {'xbox': '1',  'xbone': '1', 'psn': '2', 'pc': '4', 'ps4': '2'}

#%% main function
def destiny2_api_public(url,api_key):
    my_headers = {"X-API-Key":api_key}
    response = requests.get(url, headers = my_headers)
    return ResponseSummary(response)

#%% player url
def search_destiny_player_url(user_name, user_platform):
    """Main point is to get the user's id from their username.
        https://bungie-net.github.io/multi/operation_get_Destiny2-SearchDestinyPlayer.html
    """
    membership_type = membership_types[user_platform]
    return baseurl + 'SearchDestinyPlayer/' + membership_type + '/' + user_name + '/'

def search_destiny_vendor_url(member_shipType, member_shipID, character_id):
    ''' ベンダー
        https://bungie-net.github.io/#Destiny2.GetVendors
    '''
    slash = '/'
    vendor_url = "{0}{1}/Profile/{2}/Character/{3}/Vendor/".format(baseurl, member_shipType, member_shipID, character_id)
    return vendor_url

def get_vendor_url():
    return "{0}{1}/".format(baseurl, "Vendor")

def get_profile_url(user_name, user_platform,  components, my_api_key):
    """Get information about different aspects of user's character like equipped items.
        https://bungie-net.github.io/multi/operation_get_Destiny2-GetProfile.html
    Note components are just strings: '200,300' : you need at least one component."""
    user_id = get_user_id(user_name, user_platform, my_api_key)
    membership_type = membership_types[user_platform]
    return baseurl + membership_type + '/' + 'Profile/' + user_id + '/?components=' + components


def get_user_id(user_name, user_platform, my_api_key):
    """Uses search_destiny_player end point to get user id. Returns None if there is a problem."""
    player_summary = destiny2_api_public(search_destiny_player_url(user_name, user_platform), my_api_key)
    if player_summary.error_code == 1:
        if player_summary.data:
            return player_summary.data[0]['membershipId']
        else:
            print('There is no data for {0} on {1}'.format(user_name, user_platform))
            return None
    else:
        print('There was an error getting id for {0}. Status: {1}'.format(user_name, player_summary.status))
        return None



class ResponseSummary:
    """ 取得情報を格納 """
    def __init__(self, response):
        self.status = response.status_code
        self.url = response.url
        self.data = None
        self.message = None
        self.error_code = None
        self.error_status = None
        self.exception = None
        if self.status == 200:
            result = response.json()
            self.data = result["Response"]
            self.message = result["Message"]
            self.error_code = result["ErrorCode"]
            self.error_status = result["ErrorStatus"]


#%%###########################################
#    END FUNCTIONS AND CLASS DEFINITIONS     #
##############################################

if __name__ == '__main__':
    #%%SearchDestinyPlayer to get user id
    player_url = search_destiny_player_url(user_name, user_platform)
    player_summary = destiny2_api_public(player_url, my_api_key)
    user_id = player_summary.data[0]['membershipId']
    user_name = player_summary.data[0]["displayName"]
    # print("ユーザーID:{0}".format(user_id))
    # print("ユーザー名:{0}".format(user_name))
    
    #%%GetProfile
    #Component types include: 100 profiles; 200 characters; 201 non-equipped items (need oauth);
    #205: CharacterEquipment: what they currently have equipped. All can see this
    # components = '200,205'
    # profile_url = get_profile_url(user_name, user_platform, components, my_api_key)
    # user_profile_summary = destiny2_api_public(profile_url, my_api_key)
    # # print(user_profile_summary)

    # #%%extract character id's from profile
    # user_characters = user_profile_summary.data['characters']['data']
    # character_ids = list(user_characters.keys())
    # user_character_0 = user_characters[character_ids[0]]
    # print(user_character_0)

    vendor_url = get_vendor_url()
    vendor_profile_summary = destiny2_api_public(vendor_url, my_api_key)
    print(vendor_profile_summary.data[0]['components']['data'])




# %%
