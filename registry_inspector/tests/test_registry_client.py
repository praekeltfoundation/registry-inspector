from registry_inspector.registry_client import get_catalog
from registry_inspector.registry_client import get_tags
from registry_inspector.registry_client import get_manifests


def test_get_catalog():
    registry = 'https://my.registry.local:5000'
    assert ('repositories' in get_catalog(registry))


def test_get_tags():
    registry = 'https://my.registry.local:5000'
    name = 'ubuntu'
    assert ('tags' in get_tags(registry, name))


def test_get_manifests():
    registry = 'https://my.registry.local:5000'
    name = 'ubuntu'
    tag = 'latest'
    assert ('fsLayers' in get_manifests(registry, name, tag))
