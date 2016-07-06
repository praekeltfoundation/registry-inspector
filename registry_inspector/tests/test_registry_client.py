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
