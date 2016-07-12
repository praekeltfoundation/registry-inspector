from registry_inspector.registry_client import RegistryClient
from registry_inspector.inspector import RegistryInspector
import argparse
import math

def main():
    # Create parser to take commandline arguments
    parser = argparse.ArgumentParser()
    # registry arg
    parser.add_argument("registry_URL", help="The URL of the appropriate registry")

    args = parser.parse_args()

    client = RegistryClient(args.registry_URL)
    inspector = RegistryInspector(args.registry_URL)

    client.log('Fetching catalog...')
    catalog = client.get_catalog()
    catalog_size = len(catalog['repositories'])
    client.log('Found %d repositories in catalog' % (catalog_size))
    for i, repository in enumerate(catalog['repositories']):
        client.log()
        client.log('Working on repository "%s" (%d/%d)...' % (
        repository, i + 1, catalog_size,))

        client.log('Getting tags...')
        tags = client.get_tags(repository)
        repo_size = 0 
        # dictionary containing manifests values for each tag
        manifest_dict = inspector.get_tag_manifests(repository, tags['tags'])
        for manifest in manifest_dict:
            # dictionary containing size of each layer
            layer_dict = inspector.get_layer_dict(repository, manifest_dict[manifest])
            for layer in layer_dict:
                repo_size = repo_size + int(layer_dict[layer])

    # convert repo_size to MB
    repo_size_MB = math.ceil((float(repo_size)/1048576)*100)/100
    client.log('Size of repository: %s was found to be: %dMB' % (repository, repo_size_MB,))

if __name__ == "__main__":
    main()
