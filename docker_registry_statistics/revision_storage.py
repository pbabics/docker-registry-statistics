from typing import Iterator

import collections
import pathlib

from . import types



class RevisionStorage:

	def __init__(self, base_path: pathlib.Path) -> None:
		self.existing_revisions: List[types.ImageRevision] = list(self.list_revisions(base_path))
		self.per_repository_revisions: Dict[str, List[types.ImageRevision]] = collections.defaultdict(list)
		for revision in self.existing_revisions:
			self.per_repository_revisions[revision.repository].append(revision)


	@staticmethod
	def list_revisions(base_path: pathlib.Path) -> Iterator[types.ImageRevision]:
		for revisions_directory in base_path.glob('docker/registry/v2/repositories/**/_manifests/revisions'):
			repository = '/'.join(revisions_directory.parts[revisions_directory.parts.index('repositories') + 1 : -2])
			for revision_file in revisions_directory.glob('sha256/*/link'):
				with open(revision_file) as fin:
					revision_hash = fin.read()
				yield types.ImageRevision(
					repository = repository,
					hash_ = revision_hash
				)
