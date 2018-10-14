from typing import Iterator, Dict, List

import logging

from . import types, blob_loader



class ImageStorage:

	def __init__(self, blob_loader: blob_loader.BlobLoader) -> None:
		self._blob_loader = blob_loader
		self.images: Dict[str, types.ImageObject] = {
			image.hash_: image
			for image in self.load_images(blob_loader)
		}
	

	@staticmethod
	def load_images(blob_loader: blob_loader.BlobLoader) -> Iterator[types.ImageObject]:
		for blob in blob_loader.blobs.values():
			if blob.type_ is types.BlobTypes.IMAGE_MANIFEST:
				image_manifest = blob.data
				yield types.ImageObject(
					hash_ = blob.hash_,
					config_blob = image_manifest['config']['digest'],
					data_layers = [
						layer['digest']
						for layer in image_manifest['layers']
					]
				)
