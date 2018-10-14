from typing import Dict, Any

import logging

import click

import docker_registry_statistics.types



@click.option('--only-manifests', is_flag = True, default = False, type = bool)
def unused_blobs(ctx: Dict[str, Any], only_manifests: bool) -> None:
	'''
	Lists images which are no longer bound to any image 
	'''
	blob_loader = ctx.obj['blob_loader']
	image_storage = ctx.obj['image_storage']
	revision_storage = ctx.obj['revision_storage']

	used_blobs = set()
	for revision in revision_storage.existing_revisions:
		logging.debug('Processing image %s@%s', revision.repository, revision.hash_)
		try:
			image = image_storage.images[revision.hash_]
		except KeyError:
			pass
		else:
			used_blobs.add(image.hash_)
			used_blobs.add(image.config_blob)
			for layer in image.data_layers:
				used_blobs.add(layer)

	if only_manifests:
		for blob_hash in blob_loader.available_blobs - used_blobs:
			if blob_loader.blobs[blob_hash].type_ is docker_registry_statistics.types.BlobTypes.IMAGE_MANIFEST:
				print(blob_hash)
	else:
		for blob_hash in blob_loader.available_blobs - used_blobs:
			print(blob_hash)
