from __future__ import print_function

import sys
import re
import math

import requests

#use http instead of https if self-signed certificates have not been created
BASE_URL = 'http://localhost:5000'
#BASE_URL = 'https://localhost:5000'
SSL_VERIFY = False

DRY_RUN = '--dry-run' in sys.argv[1:]

def registry_api_call(method, path):
    return requests.request(method, BASE_URL + path, verify=SSL_VERIFY)

def get_catalog():
    return registry_api_call('GET', '/v2/_catalog').json()

def get_tags(name):
    return registry_api_call('GET', '/v2/%s/tags/list' % (name,)).json()

def get_manifests(name, tag):
    return registry_api_call('GET', '/v2/%s/manifests/%s' % (name, tag,)).json()

def get_digest_length(name, digest):
    r = registry_api_call('HEAD', '/v2/%s/blobs/%s' % (name, digest,))
    return r.headers['Content-Length']

def log(*args):
    print(*args, file=sys.stderr)

log('Fetching catalog...')
catalog = get_catalog()
catalog_size = len(catalog['repositories'])
log('Found %d repositories in catalog' % (catalog_size))
known_layers = {}
image_info = {}

for i, repository in enumerate(catalog['repositories']):
    log()
    log('Working on repository "%s" (%d/%d)...' % (
    repository, i + 1, catalog_size,))

    log('Getting tags...')
    tags = get_tags(repository)
    if tags['tags'] is None:
        log('No tags found, skipping...')
        continue
    log('Found %d tags' % (len(tags['tags'])))
    repo_size = 0

    for tag in tags['tags']:
        log('Getting manifests for %s' % (tag))
        manifest = get_manifests(repository, tag)
        log('Got manifests')
        if manifest['fsLayers'] is None:
            log('No blobSum values found, skipping...')
            continue
        log('Found %d blobSum fields' % (len(manifest['fsLayers'])))
        blobSumValues = [layer['blobSum'] for layer in manifest['fsLayers']]
        log('Adding to repository size...')
        for value in blobSumValues:
            #Want to know how many images reference a certain layer
            if value in known_layers:
                known_layers[value] += 1
            else:
       	        known_layers[value] = 1
            repo_size = repo_size + int(get_digest_length(repository, value))

    repo_size_MB = math.ceil((float(repo_size)/1048576)*100)/100
    #Sizes of different images
    image_info[repository] = repo_size_MB
    log('Size of repository: %s was found to be: %dMB' % (repository, repo_size_MB,))

log('opening layerUsage.txt to write layering reference info')
f = open('layerUsage.txt', 'w')
f.write("This file contains a record of how many images referenced a particular layer"\
	+" at the time of last run\n\n")
log('writing...')
for k in known_layers.keys():
    f.write("The layer: %s was referenced by %d images\n" % (k, known_layers[k]))
f.close()
log('write complete')

#Sorting according to top 10 largest files
f2 = open('top10Largest.txt', 'w')
f2.write("This file contains the top 10 Largest images\n\n")
#Get the repository names sorted from smallest size value to largest
sorted_image_keys = sorted(image_info.keys(), key=lambda y:(image_info[y]))
#From largest size value to smallest
sorted_image_keys.reverse()
count = 0
for k in sorted_image_keys:
    if count == 10:
        break
    f2.write("- {} : {}MB\n".format(k, image_info[k]))
    count = count + 1
f2.close()

log('Done')
