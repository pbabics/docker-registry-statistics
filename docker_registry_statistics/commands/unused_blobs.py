from typing import Dict, Any

import logging



def unused_blobs(ctx: Dict[str, Any]) -> None:
	'''
	Lists images which are no longer bound to any image 
	'''
	tag_storage = ctx.obj['tag_storage']
	blob_loader = ctx.obj['blob_loader']
	image_storage = ctx.obj['image_storage']

	used_blobs = set()
	for repository, tags in tag_storage.per_repository_tags.items():
		for tag in tags:
			for image_hash in tag.images:
				logging.debug('Processing image %s@%s', repository, image_hash)
				try:
					image = image_storage.images[image_hash]
				except KeyError:
					pass
				else:
					used_blobs.add(image.hash_)
					used_blobs.add(image.config_blob)
					for layer in image.data_layers:
						used_blobs.add(layer)

	for blob_hash in blob_loader.available_blobs - used_blobs:
		print(blob_hash)
