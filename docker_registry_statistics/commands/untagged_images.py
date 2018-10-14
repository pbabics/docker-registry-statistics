from typing import Dict, Any, Set

import logging



def untagged_images(ctx: Dict[str, Any]) -> None:
	'''
	Lists images which are no longer bound to tag
	'''
	revision_storage = ctx.obj['revision_storage']
	tag_storage = ctx.obj['tag_storage']

	for repository, revisions in revision_storage.per_repository_revisions.items():
		logging.debug('Listing untagged images for repository %s', repository)
		all_images: Set[str] = set(revision.hash_ for revision in revisions)
		currently_tagged_images: Set[str] = set()	
		for tag in tag_storage.per_repository_tags[repository]:
			currently_tagged_images.add(tag.current_image)

		for image_hash in all_images - currently_tagged_images:
			print('{:s}@{:s}'.format(repository, image_hash))
