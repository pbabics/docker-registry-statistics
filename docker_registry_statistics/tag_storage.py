from typing import Iterator

import collections
import pathlib

from . import types



class TagStorage:

	def __init__(self, base_path: pathlib.Path) -> None:
		self.existing_tags: List[types.RegistryTag] = list(self.list_tags(base_path))
		self.per_repository_tags: Dict[str, List[types.RegistryTag]] = collections.defaultdict(list)
		for tag in self.existing_tags:
			self.per_repository_tags[tag.repository].append(tag)


	@staticmethod
	def list_tags(base_path: pathlib.Path) -> Iterator[types.RegistryTag]:
		for tags_directory in base_path.glob('docker/registry/v2/repositories/**/_manifests/tags'):
			repository = '/'.join(tags_directory.parts[tags_directory.parts.index('repositories') + 1 : -2])
			for tag_directory in tags_directory.glob('*'):
				tag_name = tag_directory.parts[-1]

				with open(tag_directory / 'current' / 'link', 'r') as fin:
					current_image = fin.read()

				associated_images: List[str] = []
				for associated_image in tag_directory.glob('index/**/link'):
					with open(associated_image) as fin:
						associated_images.append(fin.read())
				yield types.RegistryTag(
					repository = repository,
					name = tag_name,
					images = associated_images,
					current_image = current_image
				)
