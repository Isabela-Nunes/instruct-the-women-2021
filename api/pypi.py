import requests

def version_exists(package_name, version):
    
    repository = f"https://pypi.org/pypi/{package_name}/{version}/json"
    response = requests.get(repository)
    if response.status_code == 200:
        return True
    else:
        return False


def latest_version(package_name):
    
    repository = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(repository)
    if response.status_code == 404:
        return None
    else:
        response = response.json()
        version = response['info']['version']
        return version