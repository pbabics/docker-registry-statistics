from typing import Dict, Any

import logging
import pathlib

import click

import docker_registry_statistics.blob_loader
import docker_registry_statistics.image_storage
import docker_registry_statistics.tag_storage

import docker_registry_statistics.commands.unused_blobs
import docker_registry_statistics.commands.orphaned_images
import docker_registry_statistics.commands.statistics



@click.group()
@click.option('--verbose', '-v', is_flag = True, default = False)
@click.argument('registry-path', type = pathlib.Path)
@click.pass_context
def cli(ctx: Any, registry_path: pathlib.Path, verbose: bool) -> None:
	'''
	Application to calculate statistics and list orphaned images and blobs
	from docker registry v2
	'''
	logging.basicConfig(
		level = logging.DEBUG if verbose else logging.INFO,
		format = '%(asctime)s %(levelname)s %(message)s',
	)
	ctx.ensure_object(dict)


	if not registry_path.is_dir():
		logging.error('Registry path is not a directory')
		raise SystemExit(1)

	ctx.obj['tag_storage'] = tag_storage = docker_registry_statistics.tag_storage.TagStorage(registry_path)
	ctx.obj['blob_loader'] = blob_loader = docker_registry_statistics.blob_loader.BlobLoader(registry_path)
	ctx.obj['image_storage'] = docker_registry_statistics.image_storage.ImageStorage(tag_storage.existing_tags, blob_loader)
	


for command in [
	docker_registry_statistics.commands.statistics.statistics,
	docker_registry_statistics.commands.orphaned_images.orphaned_images,
	docker_registry_statistics.commands.unused_blobs.unused_blobs,
]:
	cli.command()(
		click.pass_context(command)
	)



if __name__ == '__main__':
	cli(obj = {})
