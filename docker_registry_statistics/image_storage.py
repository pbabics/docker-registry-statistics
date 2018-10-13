from typing import Iterator, Dict, List

import logging

from . import types, blob_loader



class ImageStorage:

	def __init__(self, available_tags: List[types.RegistryTag], blob_loader: blob_loader.BlobLoader) -> None:
		self._blob_loader = blob_loader
		self.images: Dict[str, types.ImageObject] = {
			image.hash_: image
			for image in self.load_images(available_tags, blob_loader)
		}
	

	@staticmethod
	def load_images(available_tags: List[types.RegistryTag], blob_loader: blob_loader.BlobLoader) -> Iterator[types.ImageObject]:
		for tag in available_tags:
			for image_hash in tag.images:
				try:
					image_manifest_blob = blob_loader.blobs[image_hash]
				except KeyError:
					logging.error('Missing image manifest for %s@%s pushed under tag %s', tag.repository, image_hash, tag.name)
				else:
					image_manifest = image_manifest_blob.data

					yield types.ImageObject(
						hash_ = image_hash,
						config_blob = image_manifest['config']['digest'],
						data_layers = [
							layer['digest']
							for layer in image_manifest['layers']
						]
					)
