from typing import List, Optional, Dict, Any

import enum
import pathlib

import attr



class BlobTypes(enum.Enum):
	IMAGE_CONFIG = 0
	IMAGE_MANIFEST = 1
	COMPRESSED_LAYER = 2



@attr.s
class RegistryObject:
	hash_: str = attr.ib()


@attr.s
class Blob(RegistryObject):
	path: pathlib.Path = attr.ib()
	type_: BlobTypes = attr.ib()
	size: int = attr.ib()
	data: Optional[Dict[str, Any]] = attr.ib()


@attr.s
class RegistryTag:
	repository: str = attr.ib()
	name: str = attr.ib()
	images: str = attr.ib()
	current_image: str = attr.ib()


@attr.s
class ImageObject(RegistryObject):
	config_blob: str = attr.ib()
	data_layers: List[str] = attr.ib()
