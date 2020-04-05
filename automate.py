import requests
import sys
import argparse
import os
import subprocess
import pathlib
import getpass
from github import Github



def repoCreate(username , passwrd , repo,private ,oauth,acess_token):

    """
        desc : Create new github repository
        params:
            username (str): Github Username
            passwrd (str): Github Password
            repo (str): Repo Name
            private (bool): Whether repo is private

    """

    print()
    
    
    url = 'https://api.github.com/user/repos'  #Github's Endpoint


    if(oauth):

        if(private):
            print(f"Creating new github private repository : {repo}")
            print()
            data= {"name":repo,"homepage": "https://github.com","private":True}
        else:
            print(f"Creating new github repository : {repo}")
            print()
            data= {"name":repo,"homepage": "https://github.com"}

        ## Make POST request
        
        r = requests.post(url, json=data , auth =(username,passwrd))

        print("Request Status : ",r.ok)
        res = r.json()

        if(not r.ok ):
            print("Cannot create New Repository")
            try :
                print("Error Message : ",f"\"{r.json()['errors'][0]['message']}\"")
            except :
                print(r.json())
                
        else : 
            print(f"Success: '{repo}' Github Repository created")
            # print(r.json())

            try :

                http_url = str(res['clone_url'])
                ssh_url = str(res['ssh_url'])
                # print(http_url , ssh_url)

                return http_url , ssh_url , True
            except Exception as e:
                print("Error occured while getting git_url")
                print(e)


    else :
        try:

            ##Authenticate User
            if(acess_token == "" or acess_token  is None):
                print("NO ACESS TOKEN FOUND")
                return None,None,False

            g = Github(acess_token)
            user = g.get_user()
            print("Sucess: User Authenticated\n")

            
            try:

                ##Create Repo
                if(private):
                    repoObj = user.create_repo(repo,private=True)
                else:
                    repoObj = user.create_repo(repo,private=False)
                print(f"Sucess: {repo} created")

                try:

                    ##GET Links
                    http_url = repoObj.clone_url
                    ssh_url = repoObj.ssh_url
                    
                    return http_url,ssh_url,True
                except:
                    print("Error: Cannot get http/ssh url")

                
                
            except Exception as e:
                print("Error : Cannot create repo")
                print(e)
                print()

            
        except Exception as e :
            print("Error: Authentication Failure")
            print(e)
            print()
    return None,None,False








def makeProj(parent_dir , repo):

    """
        desc : Create Local Folder in the given directory
        params :
            parent_dir (str): Parent Directory (default = ".")
            repo (str): Name of the Local Directory to be created
    """

    print()
    dir_path = parent_dir + '/' + repo
    try :
        pathlib.Path(dir_path).mkdir(parents=True, exist_ok=False) 
        print("Success: Created Local Folder")
        try :
            os.chdir(dir_path)
            return True
        except Exception as e:
            print(e)
    except Exception as e :
        print("Error occured during local Folder creation ")
        print(e)
    return False

def initGit(ssh_url,http_url,ssh,repo):

    """
        desc: Initialise git , 
                Add README.md , 
                Add remote origin ,
                Push Initial Commit 
        params :
            ssh_url (str): via SSH  (only if ssh is True)
            http_url (str): via  HTTP  (default)
            ssh (bool): To add remote origin via SSH (default : False)
            repo (str): Repo's name  
    """

    print()
    p1 = subprocess.run(['git init'] , shell=True)

    with open("README.md","w+") as f:
        f.write(f"### {repo}")

    subprocess.run(['git' ,'add', 'README.md'])
    subprocess.run(['git commit -m "init"'],shell=True)

    if(ssh):
        cmd = f"git remote add origin {ssh_url}"
        
        print(cmd)
        subprocess.run(cmd,shell=True)
    else : 
        cmd = f"git remote add origin {http_url}"
        print(cmd)
        subprocess.run([cmd],shell=True)
    subprocess.run('git push -u origin master',shell=True)

    # git remote add origin git@github.com:arnabaghorai/New-Repo.git





parser = argparse.ArgumentParser(description='Automate Project Setup\n> Creates new repository in Github.\n> Makes a folder in the current directory\n> git init and add README.md in local setup\n> Add remote origin')
parser.add_argument('repo', type=str,help='Github repo Name')
parser.add_argument('-d','--dir', type=str, default=".",help='Path where local folder is created, default : (Current Folder) ')
parser.add_argument('--ssh', action='store_true',
                                 default=False,
                                help='add new repo through cli via SSH')
parser.add_argument('--private', action='store_true',
                                 default=False,
                                help='Initialise Private Repo')

parser.add_argument('--oauth', action='store_true',
                                 default=False,
                                help='Access via oauth instead of Acess Token ("WARNING OAuth is going to be deprecated')









def main():

    args = parser.parse_args()

    user = None
    passwrd = None
    oauth = args.oauth

    repo = args.repo
    parent_dir = args.dir
    ssh = args.ssh
    private = args.private

    personal_acess_token = os.environ.get("GIT_ACESS_TOKEN",None)

    if(not oauth):
        if(personal_acess_token is None or personal_acess_token == ""):
            print("!!!! NO PERSONAL ACESS TOKEN FOUND !!!!!")
            print()
            print(f"SET 'GIT_ACESS_TOKEN' as environment variable")
            print(f"GIT_ACESS_TOKEN='PERSONAL_ACESS_TOKEN")

            return
    else :
        print()
        print("Basic username - password based auth may get deprecate anytime.It's not reliable")
        print("GET PERSONAL ACESS TOKEN")
        print()
        if(user is None):
            user = str(input("Enter Github Username: "))
        if (passwrd is None):
                passwrd = str(getpass.getpass("Enter Github Password: "))

    http_url , ssh_url , flag = repoCreate(user,passwrd,repo,private,oauth,personal_acess_token)

    if(flag):

        if(makeProj(parent_dir,repo)):
            initGit(ssh_url,http_url,ssh,repo)
    print()


if __name__ == "__main__":
    main()


