from typing import Dict, Any

import collections
import logging

import docker_registry_statistics.types
import docker_registry_statistics.utils



def statistics(ctx: Dict[str, Any]) -> None:
	'''
	Calculates statistics about existing tags, images and blobs
	'''
	blob_loader = ctx.obj['blob_loader']
	image_storage = ctx.obj['image_storage']
	revision_storage = ctx.obj['revision_storage']
	tag_storage = ctx.obj['tag_storage']

	for repository, revisions in sorted(revision_storage.per_repository_revisions.items()):
		layer_usage = collections.defaultdict(int)
		for revision in revisions:
			try:
				image = image_storage.images[revision.hash_]
			except KeyError:
				pass
			else:
				layer_usage[image.hash_] += 1
				layer_usage[image.config_blob] += 1
				for layer in image.data_layers:
					layer_usage[layer] += 1

		total_repository_size = sum(
			blob_loader.blobs[blob_hash].size
			for blob_hash in layer_usage.keys()
			if blob_hash in blob_loader.blobs
		)

		layer_usage = collections.defaultdict(int)
		for tag in sorted(tag_storage.per_repository_tags[repository], key = lambda tag: tag.name):
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


		untagged_images: Set[str] = {
			revision.hash_
			for revision in revision_storage.per_repository_revisions[repository]
		} - {
			tag.current_image
			for tag in tag_storage.per_repository_tags[repository]
		}

		layer_usage = collections.defaultdict(int)
		for image_hash in untagged_images:
			try:
				image = image_storage.images[image_hash]
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

				logging.debug(">> %s@%s %s", repository, image_hash, docker_registry_statistics.utils.convert_size(image_size))
		untagged_images_size = sum(blob_loader.blobs[blob_hash].size for blob_hash in layer_usage.keys())

		logging.info("Repository '%s'", repository)
		logging.info('>> Total images: Count: %d, Size: %s',
			len(revision_storage.per_repository_revisions[repository]),
			docker_registry_statistics.utils.convert_size(total_repository_size)
		)
		logging.info('>> Tagged images: Count: %d, Size: %s',
			len(tag_storage.per_repository_tags[repository]),
			docker_registry_statistics.utils.convert_size(tagged_images_size),
		)
		logging.info('>> Un-tagged images: Count %d, Size: %s',
			len(untagged_images),
			docker_registry_statistics.utils.convert_size(untagged_images_size)
		)

	layer_usage = collections.defaultdict(int)
	tagged_images: Set[str] = set()
	for repository, tags in tag_storage.per_repository_tags.items():
		for tag in tags:
			tagged_images.add(tag.current_image)
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

	untagged_images: Set[str] = {
		revision.hash_
		for revision in revision_storage.existing_revisions
	} - tagged_images

	layer_usage = collections.defaultdict(int)
	for image_hash in untagged_images:
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
	untagged_images_size = sum(
		blob_loader.blobs[blob_hash].size
		for blob_hash in layer_usage.keys()
		if blob_hash in blob_loader.blobs
	)
	logging.info('Summary counts')
	logging.info('>> Total repositories: %d', len(revision_storage.per_repository_revisions.keys()))
	logging.info('>> Total tags: %d', len(tag_storage.existing_tags))
	logging.info('>> Total images: %d (Tagged: %d, Untagged: %d)',
		len(revision_storage.existing_revisions),
		len(tagged_images),
		len(untagged_images)
	)
	logging.info('>> Total blobs: %d', len(blob_loader.blobs))

	logging.info('Summary sizes')
	logging.info('>> Total images size: %s', docker_registry_statistics.utils.convert_size(total_size))
	logging.info('>> Tagged images size: %s', docker_registry_statistics.utils.convert_size(tagged_images_size))
	logging.info('>> Un-tagged images size: %s', docker_registry_statistics.utils.convert_size(untagged_images_size))

	logging.info('Blobs')
	per_blob_type_counts: Dict[docker_registry_statistics.types.BlobTypes, int] = collections.defaultdict(int)
	per_blob_type_counts_unused: Dict[docker_registry_statistics.types.BlobTypes, int] = collections.defaultdict(int)
	for blob in blob_loader.blobs.values():
		per_blob_type_counts[blob.type_] += 1
		if blob.hash_ not in layer_usage:
			per_blob_type_counts_unused[blob.type_] += 1

	logging.info('>> Counts: Total %d, Manifests: %d, Image configs: %d, Compressed data: %d',
		sum(per_blob_type_counts.values()),
		per_blob_type_counts[docker_registry_statistics.types.BlobTypes.IMAGE_MANIFEST],
		per_blob_type_counts[docker_registry_statistics.types.BlobTypes.IMAGE_CONFIG],
		per_blob_type_counts[docker_registry_statistics.types.BlobTypes.COMPRESSED_LAYER],
	)
