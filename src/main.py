import string
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os
import urllib
from PIL import Image, ImageSequence
import requests
import time
import random

load_dotenv(override=True)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def upload_emoji(name, filename):
	token = os.environ.get("UPLOAD_TOKEN")
	headers = {"Authorization": f"Bearer {token}"}
	args = {"name": name}
	with open(filename, "rb") as gif:
		x=requests.post("https://hackclub-slack-emoji-proxy.vercel.app/api/emoji/upload",
						data = args, headers=headers, files={"file":gif})
		gif.close()
	print(x.text)


def find_valid():
	client = app.client
	# Known bug where technicaly if more than 1000 users & bots join the channel it could cause issues but idc tbh.
	lst = client.conversations_members(
		channel="C0BH4B8HZ3K",
		limit=1000
	)
	valids = []
	for id in lst["members"]:
		info = client.users_info(user=id)
		if info["ok"] and info["user"]["is_bot"] == False:
			valids.append(id)
	return valids

@app.event("app_mention")
def handle_mention(event, client, say):
	print("triggered")

@app.event("user_change")
def handle_user_change(event, client, say):
	valid_ids = find_valid()
	user_id = event["user"]["id"]
	display_name = event["user"]["profile"]["display_name"].translate(str.maketrans('', '', string.punctuation)).lower()

	if user_id in valid_ids:
		print(event)
		url = event["user"]["profile"]["image_original"]
		pfp_hash = event["user"]["profile"]["avatar_hash"]

		with open("cache.txt", "r+") as cache:
			if f"{pfp_hash}\n" not in cache.readlines():
				print("new hash detected")
				file_num = random.randint(100000, 999999)
				image = urllib.request.urlopen(url).read()
				with open(f"{file_num}.png", 'wb') as f:
					f.write(image)

				pfp = Image.open(f"{file_num}.png").resize((150, 150)).convert("RGBA")
				pet = Image.open("pet.gif")

				final_frames = []
				for frame in ImageSequence.Iterator(pet):
					frame = frame.resize((100, 100)).convert("RGBA")
					pfp_copy = pfp.copy()
					pfp_copy.paste(frame, mask=frame)
					final_frames.append(pfp_copy)
				final_frames[0].save(f"{file_num}.gif", save_all=True, append_images=final_frames[1:], loop=0)
				emoji_name = f"pet-{display_name}{int(time.time())}"
				upload_emoji(emoji_name, f"{file_num}.gif")

				cache.write(f"{pfp_hash}\n")

				os.remove(f"{file_num}.png")
				os.remove(f"{file_num}.gif")
				print("uplaoded")
				app.client.chat_postMessage(channel="C0BH4B8HZ3K", text=f"<@{user_id}> :{emoji_name}:")
			else:
				print("found in cache")
			f.close()

if __name__ == "__main__":
	print("starting")
	SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
