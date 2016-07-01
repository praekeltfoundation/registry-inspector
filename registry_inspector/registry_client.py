import requests


class RegistryClient(object):
    def __init__(self, registry):
        self.registry = registry

    def _call_registry(self, method, path):
        return requests.request(method, self.registry + path, verify=False)

    def get_catalog(self):
        # TODO: Replace this with a real implementation
        return self._call_registry('GET', '/v2/_catalog/').json()

    def get_tags(self, name):
        x = {'tags': 'cool'}
        return x

    def get_manifests(self, name, tag):
        x = {'fsLayers': 'cool'}
        return x
