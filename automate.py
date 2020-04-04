import requests
import sys
import argparse
import os
import subprocess
import pathlib
import getpass



def repoCreate(username , passwrd , repo,private):

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
parser.add_argument('-u','--username', type=str, default=None,help='Github Username')
parser.add_argument('-p','--password', type=str, default=None, help='Github Password')
parser.add_argument('--ssh', action='store_true',
                                 default=False,
                                help='add new repo through cli via SSH')
parser.add_argument('--private', action='store_true',
                                 default=False,
                                help='Initialise Private Repo')
args = parser.parse_args()

user = args.username
passwrd = args.password

if(user is None):
    user = str(input("Enter Github Username: "))
if (passwrd is None):
    passwrd = str(getpass.getpass("Enter Github Password: "))


repo = args.repo
parent_dir = args.dir
ssh = args.ssh
private = args.private

def main():
    http_url , ssh_url , flag = repoCreate(user,passwrd,repo,private)
    if(flag):

        if(makeProj(parent_dir,repo)):
            initGit(ssh_url,http_url,ssh,repo)
    print()


if __name__ == "__main__":
    main()


