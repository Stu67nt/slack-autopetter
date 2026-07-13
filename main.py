from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os
import urllib
from PIL import Image, ImageSequence
from playwright.sync_api import sync_playwright

load_dotenv(override=True)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
"""
def upload_emoji():
	
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=True)
		page = browser.new_page()"""



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
	if user_id in valid_ids:
		print(event)
		url = event["user"]["profile"]["image_original"]
		image = urllib.request.urlopen(url).read()
		with open("temp.png", 'wb') as file:
			file.write(image)
		pfp = Image.open("temp.png").convert("RGBA")
		pet = Image.open("pet.gif")
		final_frames = []
		for frame in ImageSequence.Iterator(pet):
			frame = frame.resize((int(pfp.size[0]*0.75), int(pfp.size[1]*0.75))).convert("RGBA")
			pfp_copy = pfp.copy()
			pfp_copy.paste(frame, mask=frame)
			final_frames.append(pfp_copy)
		final_frames[0].save("output.gif", save_all=True, append_images=final_frames[1:], loop=0)



if __name__ == "__main__":
	print("starting")
	SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
