import os
import sys
import json

def main():
    arg = sys.argv[1]
    print ('=' * 100)
    json_to_python = json.loads(arg)
    try:
        state = json_to_python['state']
        html_url = json_to_python['html_url']
        head_branch = json_to_python['head_branch']
        head_repo = json_to_python['head_repo']['html_url']
        base_branch = json_to_python['base_branch']
        base_repo = json_to_python['base_repo']['html_url']
    except:
        print ('json file error')
    print ('state:::::::::::::::::::%s' %state)    
    return html_url, head_branch, head_repo, base_branch, base_repo, 

if __name__ == "__main__":
    comments_url, head_repo_url, head_branch, base_repo_url, base_branch = main()
    print ("comments_url: %s" %comments_url)
    print ("head_repo_url: %s" %head_repo_url)
    print ("head_branch: %s" %head_branch)
