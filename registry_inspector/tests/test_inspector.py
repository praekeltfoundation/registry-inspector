from registry_inspector.inspector import RegistryInspector
import responses
import json


def layer_callback(sha256, content_length):
    def cb(request):
        headers = {
                "Docker-Content-Digest": "sha256:%s" % (sha256,),
                "Etag": "sha256: %s" % (sha256,),
                "Content-Length": content_length,
        }
        return 200, headers, ""
    return cb


@responses.activate
def test_get_layer_dict():
    BLOB1 = 'a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4'
    BLOB2 = '10fb34ebccea88897d4b570120719b23fcbf3e556abdb79fdba6b2e0e4bad9ab'
    registry = 'http://localhost:5000'
    image = 'ubuntu'
    digest = {BLOB1: '32', BLOB2: '680'}

    for digest_value in digest:
        responses.add_callback(
            responses.HEAD, registry + '/v2/%s/blobs/%s' %
            (image, 'sha256:'+digest_value,),
            callback=layer_callback(digest_value, digest[digest_value]))

    manifest = {"fsLayers": [{"blobSum": "sha256:"+BLOB1},
                             {"blobSum": "sha256:"+BLOB2}]}
    inspector = RegistryInspector(registry)
    resp = inspector.get_layer_dict('ubuntu', manifest)
    assert resp == {"sha256:"+BLOB1: 32, "sha256:"+BLOB2: 680}

def manifest_callback(name, tag):
    def cb(request):
        body = {
                "schemaVersion": 1,
                "name": name,
                "tag": tag,
        }
        return 200, "", json.dumps(body)
    return cb


@responses.activate
def test_get_tag_manifests():
    registry = 'http://localhost:5000'
    image = 'ubuntu'
    tag_list = ['xenial','latest']
    for tag in tag_list:
        responses.add_callback(
            responses.GET, registry + '/v2/%s/manifests/%s' %
            (image, tag,), callback=manifest_callback(image, tag))
    manifest_dic = {"xenial":{"schemaVersion": 1, "name": "ubuntu", "tag": "xenial"},
                    "latest":{"schemaVersion": 1, "name": "ubuntu", "tag": "latest"}} 
    inspector = RegistryInspector(registry)
    resp = inspector.get_tag_manifests(image, tag_list)
    assert resp == manifest_dic
