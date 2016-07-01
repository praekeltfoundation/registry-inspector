class RegistryClient(object):
    def __init__(self, registry):
        self.registry = registry

    def get_catalog(self):
        # TODO: Replace this with a real implementation
        x = {'repositories': 'cool'}
        return x

    def get_tags(self, name):
        x = {'tags': 'cool'}
        return x

    def get_manifests(self, name, tag):
        x = {'fsLayers': 'cool'}
        return x
