from typing import Dict, Any

import collections
import logging

import docker_registry_statistics.types
import docker_registry_statistics.utils



def statistics(ctx: Dict[str, Any]) -> None:
	'''
	Calculates statistics about existing tags, images and blobs
	'''
	tag_storage = ctx.obj['tag_storage']
	blob_loader = ctx.obj['blob_loader']
	image_storage = ctx.obj['image_storage']

	for repository, tags in tag_storage.per_repository_tags.items():
		layer_usage = collections.defaultdict(int)
		for tag in tags:
			for image_hash in tag.images:
				try:
					image = image_storage.images[image_hash]
				except KeyError:
					pass
				else:
					layer_usage[image.hash_] += 1
					layer_usage[image.config_blob] += 1
					for layer in image.data_layers:
						layer_usage[layer] += 1

		total_repository_size = sum(blob_loader.blobs[blob_hash].size for blob_hash in layer_usage.keys())

		layer_usage = collections.defaultdict(int)
		for tag in sorted(tags, key = lambda tag: tag.name):
			try:
				image = image_storage.images[tag.current_image]
			except KeyError:
				pass
			else:
				image_size: int = blob_loader.blobs[image.hash_].size \
					+ blob_loader.blobs[image.config_blob].size \
					+ sum(
						blob_loader.blobs[layer].size
						for layer in image.data_layers
					)

				# Mark used layers
				layer_usage[image.hash_] += 1
				layer_usage[image.config_blob] += 1
				for layer in image.data_layers:
					layer_usage[layer] += 1

				logging.debug(">> %s:%s %s", repository, tag.name, docker_registry_statistics.utils.convert_size(image_size))

		tagged_images_size = sum(blob_loader.blobs[blob_hash].size for blob_hash in layer_usage.keys())
		logging.info("Repository '%s' repository size %s tagged images size %s orphaned tags size %s",
			repository, 
			docker_registry_statistics.utils.convert_size(total_repository_size), 
			docker_registry_statistics.utils.convert_size(tagged_images_size), 
			docker_registry_statistics.utils.convert_size(total_repository_size - tagged_images_size)
		)

	layer_usage = collections.defaultdict(int)
	for repository, tags in tag_storage.per_repository_tags.items():
		for tag in tags:
			try:
				image = image_storage.images[tag.current_image]
			except KeyError:
				pass
			else:
				layer_usage[image.hash_] += 1
				layer_usage[image.config_blob] += 1
				for layer in image.data_layers:
					layer_usage[layer] += 1
	tagged_images_size = sum(blob_loader.blobs[blob_hash].size for blob_hash in layer_usage.keys())

	layer_usage = collections.defaultdict(int)
	for repository, tags in tag_storage.per_repository_tags.items():
		for tag in tags:
			for image_hash in tag.images:
				try:
					image = image_storage.images[image_hash]
				except KeyError:
					pass
				else:
					layer_usage[image.hash_] += 1
					layer_usage[image.config_blob] += 1
					for layer in image.data_layers:
						layer_usage[layer] += 1

	total_size = sum(blob.size for blob in blob_loader.blobs.values())
	existing_images_size = sum(blob_loader.blobs[blob_hash].size for blob_hash in layer_usage.keys())
	logging.info('Total tags: %d', len(tag_storage.existing_tags))
	logging.info('Total images: %d', sum(1 for blob in blob_loader.blobs.values() if blob.type_ is docker_registry_statistics.types.BlobTypes.IMAGE_MANIFEST))
	logging.info('Total blobs: %d', len(blob_loader.blobs))
	logging.info('Total size: %s', docker_registry_statistics.utils.convert_size(total_size))
	logging.info('Total images size: %s', docker_registry_statistics.utils.convert_size(existing_images_size))
	logging.info('Tagged images size: %s', docker_registry_statistics.utils.convert_size(tagged_images_size))
	logging.info('Orphaned images size: %s', docker_registry_statistics.utils.convert_size(existing_images_size - tagged_images_size))
	logging.info('Orphaned blobs size: %s', docker_registry_statistics.utils.convert_size(total_size - existing_images_size))
