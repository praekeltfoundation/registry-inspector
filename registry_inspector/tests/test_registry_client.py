from registry_inspector.registry_client import RegistryClient
import responses


@responses.activate
def test_get_catalog():
    registry = 'http://localhost:5000'
    responses.add(
        responses.GET, registry + '/v2/_catalog/',
        json={"repositories": ["ubuntu"]})
    client = RegistryClient(registry)
    resp = client.get_catalog()
    assert resp == {"repositories": ["ubuntu"]}


@responses.activate
def test_get_tags():
    registry = 'http://localhost:5000'
    responses.add(
        responses.GET, registry + '/v2/%s/tags/list' % ('ubuntu'),
        json={"name": "ubuntu", "tags": ["latest"]}, match_querystring=True)
    client = RegistryClient(registry)
    name = 'ubuntu'
    resp = client.get_tags(name)
    assert resp == {"name": "ubuntu", "tags": ["latest"]}


@responses.activate
def test_get_manifests():
    registry = 'http://localhost:5000'
    client = RegistryClient(registry)
    name = 'ubuntu'
    tag = 'latest'
    responses.add(
        responses.GET, registry + '/v2/%s/manifests/%s' %
        (name, tag,), content_type='application/json',
        json={"fsLayers": [{"blobSum": "sha256:a3ed95caeb02ffe68cdd9fd844066"
                                       "80ae93d633cb1642d00e8a7c22955b46d4"},
                           {"blobSum": "sha256:10fb34ebccea88897d4b570120719"
                                       "b23fcbf3e556abdb79fdba6b2e0e4bad9ab"},
                           {"blobSum": "sha256:4c876570bd7d10c58fc291fa98040"
                                       "4290de01bfc01410daeb57a9dd6b86fac57"},
                           {"blobSum": "sha256:6874f9870f5f8b13aea44707fddf7"
                                       "46825247dda0f3abc9d93438b58c97cdacd"},
                           {"blobSum": "sha256:5ba4f30e5bea63dcc2e7054b8b4f4"
                                       "1ab1e5fcc7db0a88fc7"
                                       "9359b890bcfe2258"}]})
    resp = client.get_manifests(name, tag)['fsLayers']
    assert resp == {"fsLayers": [{"blobSum": "sha256:a3ed95caeb02ffe68cdd9fd"
                                             "84406680ae93d633cb1642d00e8a7c"
                                             "22955b46d4"},
                                 {"blobSum": "sha256:10fb34ebccea88897d4b570"
                                             "120719b23fcbf3e556abdb79fdba6b"
                                             "2e0e4bad9ab"},
                                 {"blobSum": "sha256:4c876570bd7d10c58fc291f"
                                             "a980404290de01bfc01410daeb57a9"
                                             "dd6b86fac57"},
                                 {"blobSum": "sha256:6874f9870f5f8b13aea4470"
                                             "7fddf746825247dda0f3abc9d93438"
                                             "b58c97cdacd"},
                                 {"blobSum": "sha256:5ba4f30e5bea63dcc2e7054"
                                             "b8b4f41ab1e5fcc7db0a88fc79359b"
                                             "890bcfe2258"}]}['fsLayers']


@responses.activate
def test_get_digest_length():
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
    client = RegistryClient(registry)
    name = 'ubuntu'
    digest = ('sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633'
              'cb16422d00e8a7c22955b46d4')

    responses.add_callback(
        responses.HEAD, registry + '/v2/%s/blobs/%s' %
        (name, digest,), callback=headers_callback)

    resp = client.get_digest_length(name, digest)
    assert resp == '32'


def test_log(capsys):
    registry = 'http://localhost:5000'
    client = RegistryClient(registry)
    client.log("log testing")
    out, err = capsys.readouterr()
    assert (out, err) == ("", "log testing\n")
