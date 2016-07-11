from registry_inspector.inspector import RegistryInspector
import responses


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

    registry = 'http://localhost:5000'
    name = 'ubuntu'
    digest = {('a3ed95caeb02ffe68cdd9fd84406680ae93d633'
              'cb16422d00e8a7c22955b46d4'): '32', ('10fb34ebccea88897d4b5701'
              '20719b23fcbf3e556abdb79fdba6b2e0e4bad9ab'): '680'}

    for digest_value in digest:
        responses.add_callback(
            responses.HEAD, registry + '/v2/%s/blobs/%s' %
            (name, 'sha256:'+digest_value,),
            callback=layer_callback(digest_value, digest[digest_value]))

    manifest = {"fsLayers": [{"blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84"
                                         "406680ae93d633cb16422d00e8a7c229"
                                         "55b46d4"},
                             {"blobSum": "sha256:10fb34ebccea88897d4b57012"
                                         "0719b23fcbf3e556abdb79fdba6b2e0e"
                                         "4bad9ab"}]}
    inspector = RegistryInspector(registry)
    resp = inspector.get_layer_dict('ubuntu', manifest)
    assert resp == {"sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422"
                    "d00e8a7c22955b46d4": 32, "sha256:10fb34ebccea88897d4b57"
                    "0120719b23fcbf3e556abdb79fdba6b2e0e4bad9ab": 680}
