from registry_inspector.registry_client import RegistryClient


class RegistryInspector(object):
    def __init__(self, registry):
        self.registry = registry

    def get_layer_dict(self, image, manifest):
        client = RegistryClient(self.registry)
        layer_dict = {}
        blobSumValues = [layer['blobSum'] for layer in manifest['fsLayers']]
        for value in blobSumValues:
            layer_dict[value] = int(client.get_digest_length(image, value))
        return layer_dict
