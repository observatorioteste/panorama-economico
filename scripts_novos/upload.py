from github import Github
import util as util
from util import *

def upload_files_to_github(name_json):
    path_save_json = util.config['path_save_json']['path']

    user = util.config['user-name']['user']
    branch_name = util.config['branch-name']['branch']
    repositorio_name = util.config['repositorio-name']['repositorio']
    token = util.config['token-github']['token']
    pasta_repositorio_to_save = util.config['pasta-repositorio-save']['pasta']

    g = Github(user, token)

    repo = g.get_user().get_repo('automatizacao_panorama_economico')

    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))


    with open(path_save_json + name_json +'.json', 'r', encoding='utf-8') as file:
        content = file.read()
        
    # content = content.encode("windows-1252").decode("utf-8")

    # Upload to github
    git_file = 'panorama-economico/' + name_json +'.json'
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch=branch_name)
        print('- ' + name_json + '.json ATUALIZADO')
    else:
        repo.create_file(git_file, "committing files", content, branch=branch_name)
        print('- ' + name_json + '.json CRIADO')