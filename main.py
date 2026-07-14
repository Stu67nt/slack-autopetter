import string

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os
import urllib
from PIL import Image, ImageSequence
import requests
import time

load_dotenv(override=True)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
avatar_cache = {}
def upload_emoji(name):
	token = os.environ.get("UPLOAD_TOKEN")
	headers = {
		"Authorization": f"Bearer {token}"}
	args = {
		"name": name
			}
	with open("output.gif", "rb") as f:
		x=requests.post("https://hackclub-slack-emoji-proxy.vercel.app/api/emoji/upload",
						data = args, headers=headers, files={"file":f})
	print(x.text)


def find_valid():
	client = app.client
	lst = client.conversations_members(
		channel="C0BH4B8HZ3K",
		limit=1000
	)
	print(lst)
	valids = []
	for id in lst["members"]:
		print(id)
		info = client.users_info(user=id)
		print(info)
		if info["ok"] and info["user"]["is_bot"] == False:
			valids.append(id)
	return valids

@app.event("app_mention")
def handle_mention(event, client, say):
	print("triggered")
	say(channel="C0AV9NMSN9L", text="Hai bean!")

@app.event("user_change")
def handle_user_change(event, client, say):
	with open("valid_ids.txt", "r") as f:
		valid_ids = f.readlines()
		for i, id in enumerate(valid_ids):
			valid_ids[i] = id[:-1]
		f.close()
	user_id = event["user"]["id"]
	display_name = event["user"]["profile"]["display_name"].translate(str.maketrans('', '', string.punctuation)).lower()
	if user_id in valid_ids:
		print(event)
		url = event["user"]["profile"]["image_original"]
		hash = event["user"]["profile"]["avatar_hash"]

		with open("cache.txt", "r+") as f:
			if f"{hash}\n" not in f.readlines():
				print("new hash detected")
				image = urllib.request.urlopen(url).read()
				with open("temp.png", 'wb') as file:
					file.write(image)
				pfp = Image.open("temp.png").resize((150, 150)).convert("RGBA")
				pet = Image.open("pet.gif")
				final_frames = []
				for frame in ImageSequence.Iterator(pet):
					frame = frame.resize((100, 100)).convert("RGBA")
					pfp_copy = pfp.copy()
					pfp_copy.paste(frame, mask=frame)
					final_frames.append(pfp_copy)
				final_frames[0].save("output.gif", save_all=True, append_images=final_frames[1:], loop=0)
				upload_emoji(f"pet-{display_name}{int(time.time())}")
				f.write(f"{hash}\n")
				f.close()
				os.remove("temp.png")
				os.remove("output.gif")



if __name__ == "__main__":
	print("starting")
	# SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()