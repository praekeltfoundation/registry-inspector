from registry_inspector.registry_client import get_catalog

def test_get_catalog():
	registry = 'https://my.registry.local:5000'
	assert ('repositories' in get_catalog(registry))