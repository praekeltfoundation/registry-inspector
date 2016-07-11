from registry_inspector.inspector import RegistryInspector
import responses

def test_get_layer_dict():
    def headers_callback(request):
        headers = {
            "Accept-Ranges": "bytes",
            "Cache-Control": "max-age=31536000",
            "Content-Length": "32",
            "Content-Type": "application/octet-stream",
            "Docker-Content-Digest": "sha256:a3ed95caeb02ffe68cdd9fd84406680a"
                                     "e93d633cb16422d00e8a7c22955b46d4",
            "Docker-Distribution-Api-Version": "registry/2.0",
            "Etag": "sha256: a3ed95caeb02ffe68cdd9fd84406680a"
                    "e93d633cb16422d00e8a7c22955b46d4",
            "X-Content-Type-Options": "nosniff",
            "Date": "Thu, 07 Jul 2016 13:14:44 GMT"}
        body = ""
        return 200, headers, body

    registry = 'http://localhost:5000'
    name = 'ubuntu'
    digest = ('sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633'
              'cb16422d00e8a7c22955b46d4')

    responses.add_callback(
        responses.HEAD, registry + '/v2/%s/blobs/%s' %
        (name, digest,), callback=headers_callback)

    manifest = {"fsLayers": [{"blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"}]}
    inspector = RegistryInspector(registry)
    resp = inspector.get_layer_dict('ubuntu', manifest)
    assert resp == {"sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4": 32}
