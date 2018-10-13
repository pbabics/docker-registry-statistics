from typing import Dict, Any

import logging



def orphaned_images(ctx: Dict[str, Any]) -> None:
	'''
	Lists images which are no longer bound to tag
	'''
	tag_storage = ctx.obj['tag_storage']
	blob_loader = ctx.obj['blob_loader']
	image_storage = ctx.obj['image_storage']

	for repository, tags in tag_storage.per_repository_tags.items():
		logging.debug('Listing orphaned images for repository %s', repository)
		for tag in tags:
			logging.debug('Listing orphaned images for %s:%s', repository, tag.name)
			orphaned_tag_images = set(tag.images) - {tag.current_image}
			for image_hash in orphaned_tag_images:
				print('{:s}@{:s}'.format(repository, image_hash))
