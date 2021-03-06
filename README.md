### Automate-Project-Setup


### Features

- Create New Github Repository
- Create Local Directory in specified Location
- Initialise git in local repo
- Add README.md file / Initialise custom README.md
- Do the initial commit
- Add remote origin 
- Push the Inital commit to the Github repo
- Initialise new branch and push the same

### Contents 
- `automate.py` (Python Script)
- `dist/automate` (Executable)

### Requirements :

- Create **Github Personal Access Token** from [here](https://github.com/settings/tokens).

    Read [this](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) for reference.

    Set the scope of token such that it can create and read repos.
- Set environment variables `GIT_ACESS_TOKEN="Personal_Acess_Token"` , 

    - How to set up environment variables :
        - [Windows](https://www.youtube.com/watch?v=IolxqkL7cD8) 
        -   [Linux/Mac](https://www.youtube.com/watch?v=5iWhQWVXosU)


Such that 
```python
import os

#Returns Github's Personl Acess Token
acess_token = os.environ.get("GIT_ACESS_TOKEN",None) 

print("Environment Variable set properly : ",acess_token is not None or acess_token !="")
### >>> Environment Variable set properly : True    # Should be True
```

### Dependencies
> `pip install -r requirements.txt`

### How to run
- Defaults:
    - Creates **public** repo
    - Creates local folder in the current directory "."
    - Add remote origin via **HTTP**.
    - `python automate.py repo_name`
    
- To create a **private** repo via HTTP:
    - `python automate.py repo_name --private`
- To add remote origin via **SSH** (default : HTTP) (Setup [**SSH keys.**](https://help.github.com/en/enterprise/2.15/user/articles/adding-a-new-ssh-key-to-your-github-account) )
    - `python automate.py repo_name --ssh`
- To create a **private** repo and add remote origin via **SSH** 
    - `python automate.py repo_name --ssh --private`
- To initialise project with Branch :
    - `python automate.py repo_name --branch branch_name` (Creates new branch)
- To Initialise with custom README.md
    - `python automate.py repo_name --readme` (Later takes user input)
- To create local folder at specified location
    - `python automate.py repo_name --dir "complete/path/to/folder"`
- To authenticate via basic username and password instead of __*PERSONAL_ACESS_TOKEN*__ :
    - `python automate.py repo_name --oauth` (**Warning** can be deprecated anytime , Not Preferred)
- To Know More
    - `python automate.py --help`
    
    
#### Pyinstaller

**To create exec file** 

> `pip install --upgrade 'setuptools<45.0.0'`

> `pyinstaller --onefile automate.py`

This creates a exec `./dist/automate`

Now you can execute without having python installed :

(Note : You should set the personal acess token as environment variable )

> `automate repo_name`

To Know more : `automate -h`or `automate --help`

( Tip : Set the path of dist/automate in your environment variable and run the executable from anywhere)



