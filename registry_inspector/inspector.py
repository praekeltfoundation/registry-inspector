from registry_inspector.registry_client import RegistryClient


class RegistryInspector(object):
    def __init__(self, registry):
        self.registry = registry

    # function returns a dict with blob digests as keys and their
    # lengths as values
    def get_layer_dict(self, image, manifest):
        client = RegistryClient(self.registry)
        layer_dict = {}
        blobSumValues = [layer['blobSum'] for layer in manifest['fsLayers']]
        for value in blobSumValues:
            layer_dict[value] = int(client.get_digest_length(image, value))
        return layer_dict

    # function returns a dict with tags as keys and their
    # manifests as values
    def get_tag_manifests(self, image, tag_list):
        client = RegistryClient(self.registry)
        manifest_dict = {}
        for tag in tag_list:
            manifest_dict[tag] = client.get_manifest(image, tag)
        return manifest_dict
