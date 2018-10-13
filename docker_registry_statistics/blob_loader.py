from typing import Set, Iterator

import pathlib
import json

from . import types



class BlobLoader:
	
	def __init__(self, base_path: pathlib.Path) -> None:
		self._registry_base_path = base_path
		self._blobs_path = base_path / 'docker' / 'registry' / 'v2' / 'blobs' / 'sha256'
		self.available_blobs: Set[str] = set(self.list_blobs(base_path))
		self.blobs: Dict[str, types.Blob] = {
			blob.hash_: blob
			for blob in self._load_blobs()
		}


	@staticmethod
	def list_blobs(base_path: pathlib.Path) -> Iterator[str]:
		for file_ in base_path.glob('docker/registry/v2/blobs/sha256/**/data'):
			yield 'sha256:' + file_.parts[-2]
	
	
	def _load_blobs(self) -> Iterator[types.Blob]:
		for blob_hash in self.available_blobs:
			blob_path = self.get_blob_path(self._blobs_path, blob_hash)
			file_size = blob_path.stat().st_size
			blob_type: types.BlobTypes
			file_data: Optional[Dict[str, Any]] = None
			with open(blob_path, 'rb') as fin:
				first_character: bytes = fin.read(1)
			if first_character != b'{':
				blob_type = types.BlobTypes.COMPRESSED_LAYER
			else:
				with open(blob_path, 'r') as fin:
					file_data: Dict[str, Any] = json.load(fin)
				if file_data.get('mediaType') == 'application/vnd.docker.distribution.manifest.v2+json':
					blob_type = types.BlobTypes.IMAGE_MANIFEST
				else:
					blob_type = types.BlobTypes.IMAGE_CONFIG
			yield types.Blob(
				path = blob_path,
				hash_ = blob_hash,
				type_ = blob_type,
				size = file_size,
				data = file_data
			)


	@staticmethod
	def get_blob_path(base_blob_path: pathlib.Path, blob_hash: str) -> pathlib.Path:
		assert blob_hash.startswith('sha256:')
		raw_hash = blob_hash[7:]
		return base_blob_path / raw_hash[:2] / raw_hash / 'data'
