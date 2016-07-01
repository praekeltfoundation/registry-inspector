from registry_inspector.registry_client import get_catalog
from registry_inspector.registry_client import get_tags

def test_get_catalog():
	registry = 'https://my.registry.local:5000'
	assert ('repositories' in get_catalog(registry))

def test_get_tags():
	registry = 'https://my.registry.local:5000'
	name = 'ubuntu'
	assert ('tags' in get_tags(registry, name))