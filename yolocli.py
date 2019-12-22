import argparse
import requests
import re
import random
import base36

api_endpoint = "http://onyolo.com"
cookie = "87shdyes4hsl6tps2stu4"

# We need cookies
r_session = requests.Session()


def isValidUser(uid: str) -> bool:
    """ Check if a user is valid """

    # Read page data
    status = r_session.get(f"{api_endpoint}/m/{uid}").text

    return status != "Not Found"


def getRealName(uid: str) -> str:
    """ Gets a user's 'real' name """

    # Read page data
    data = r_session.get(f"{api_endpoint}/m/{uid}").text

    names = re.findall(r"Send anonymous messages to (.*)", data)

    # Handle no name
    if len(names) == 0:
        return "Unknown User"
    else:
        return names[0][:-2]


def sendMessage(uid: str, message: str, name: str):

    # Determine session cookie
    cookie = base36.dumps(random.randint(10000000000000000, 99999999999999999)) + \
        base36.dumps(random.randint(10000000000000000, 99999999999999999))

    # Send post to server
    data = r_session.post(f"{api_endpoint}/{uid}/message", data={
        "text": message,
        "cookie": cookie,
        "wording": f"Send anonymous messages to {name}"
    }).text

    print(data)


# Handle args
ap = argparse.ArgumentParser()
ap.add_argument(
    "userid", help="OnYOLO user ID (can be found in the submit URL)")
ap.add_argument("message", help="Message to send")
args = ap.parse_args()

# Read to strings
user: str = args.userid
message: str = args.message

# Handle invalid users
if not isValidUser(user):
    print(f"{user} is not a valid user")
    exit(1)

# Read the user's real name
real_name = getRealName(user)

print(f"This user's name is: {real_name}")

# Send the message
print("Sending message...")
sendMessage(user, message, real_name)

# Clean up, and finish
print("Message sent")
exit(0)
