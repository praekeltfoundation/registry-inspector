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


def test_get_tags():
    registry = 'http://localhost:5000'
    responses.add(
        responses.GET, registry + '/v2/%s/tags/list/' % ('ubuntu'),
        json={"name": "ubuntu", "tags": ["latest"]})
    client = RegistryClient(registry)
    name = 'ubuntu'
    resp = client.get_tags(name)
    assert resp == {"name": "ubuntu", "tags": ["latest"]}


def test_get_manifests():
    registry = 'http://localhost:5000'

    client = RegistryClient(registry)
    name = 'ubuntu'
    tag = 'latest'
    responses.add(
        responses.GET, registry + '/v2/%s/manifests/%s' %
        (name, tag,),
        body=[{'blobSum': 'sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633'
                          'cb16422d00e8a7c22955b46d4'},
              {'blobSum': 'sha256:10fb34ebccea88897d4b570120719b23fcbf3e5'
                          '56abdb79fdba6b2e0e4bad9ab'},
              {'blobSum': 'sha256:4c876570bd7d10c58fc291fa980404290de01bf'
                          'c01410daeb57a9dd6b86fac57'},
              {'blobSum': 'sha256:6874f9870f5f8b13aea44707fddf746825247dd'
                          'a0f3abc9d93438b58c97cdacd'},
              {'blobSum': 'sha256:5ba4f30e5bea63dcc2e7054b8b4f41ab1e5fcc7'
                          'db0a88fc79359b890bcfe2258'}])
    resp = client.get_manifests(name, tag)['fsLayers']
    assert resp == [{'blobSum': 'sha256:a3ed95caeb02ffe68cdd9fd84406680ae'
                                '93d633cb16422d00e8a7c22955b46d4'},
                    {'blobSum': 'sha256:10fb34ebccea88897d4b570120719b23f'
                                'cbf3e556abdb79fdba6b2e0e4bad9ab'},
                    {'blobSum': 'sha256:4c876570bd7d10c58fc291fa980404290'
                                'de01bfc01410daeb57a9dd6b86fac57'},
                    {'blobSum': 'sha256:6874f9870f5f8b13aea44707fddf74682'
                                '5247dda0f3abc9d93438b58c97cdacd'},
                    {'blobSum': 'sha256:5ba4f30e5bea63dcc2e7054b8b4f41ab1'
                                'e5fcc7db0a88fc79359b890bcfe2258'}]
