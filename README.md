### Automate-Project-Setup


### Features

- Create New Github Repository
- Create Local Directory in specified Location
- Initialise git in local repo
- Add README.md file
- Do the initial commit
- Add remote origin 
- Push the Inital commit to the Github repo

### Requirements :

- Create **Github Personal Acess Token** from [here](https://github.com/settings/tokens) .Read [this](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) for reference.
- Set environment variables `GIT_ACESS_TOKEN="Personal_Acess_Token"` , 

    - How to set up environment variables :
        - [Windows](https://www.youtube.com/watch?v=IolxqkL7cD8) 
        -   [Linux/Mac](https://www.youtube.com/watch?v=5iWhQWVXosU)


Such that 
```python
import os

#Returns Github's Personl Acess Token
acess_token = os.environ.get("GIT_ACESS_TOKEN",None) 

print("Environment Variable set properly : ",acess_token is not None)
### >>> Environment Variable set properly : True ###Should be True
```

### Dependencies
> pip install -r requirements.txt

### How to run

#### Pyinstaller

**To create exec file** 

> pip install --upgrade 'setuptools<45.0.0'

> pyinstaller --onefile automate.py

This creates a exec `./dist/automate`
