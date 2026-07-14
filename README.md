# Slack Autopetter

---
### Example


![660416.gif](660416.gif)

---

### So what are you exactly?

This is a Slack Bot which automatically tracks updates to your profile picture and will create a pet emoji whenever you change profile picture. So now your pets can always be up to date with no extra effort!

---

### How do I use it?

Join the channel #pfp-petter to consent to your pfp being tracked and then change your profile picture as you would normally on slack. When you change the bot will make the emoji and ping you in the channel with the new pet emoji!

---

### Who tf needs this? 

Well, I made it because a friend wanted me to make new pet emojis for them whenever they changed profile picture (which was a bit too frequently) so I decided to make a bot to automate it.

---

### Hosting instructions (Why would you do this?)

Long story short here is how u run it

- clone the repo 
- install the requirements.txt
- change to the src directory
- add in the .env variable setup as shown below
- run main.py

Exact commands on Debain Linux (not including .env setup)

    git clone https://github.com/Stu67nt/slack-autopetter
    cd slack-autopetter
    python3 -m venv prod
    source prod/bin/activate
    pip install -r requirements.txt

.env file setup
    
    SLACK_BOT_TOKEN=[PASTE TOKEN HERE]
    SLACK_APP_TOKEN=[PASTE TOKEN HERE]
    UPLOAD_TOKEN=[PASTE TOKEN HERE]

To get the Slack bot and app token get them from the Slack developer dashboard.  
To get the upload token visit #slack-emoji-proxy on the Hack Club Slack and read the pinned message the auth key you get there should be the one pasted to UPLOAD TOKEN.

---

### Credits

Huge thanks to @Devarsh on Slack for making the slack emoji proxy which makes uploading slack emoji's automatically INFINITELY EASIER. Genuine lifesaver.

Also thanks to my friend for the inital suggestion!

---

### Future improvemnts (they won't happen)

The petting is just a shitty pet gif overlay so imporving it to be more lively and animated would be a good next step.  