# Docker Registry Statistics

This project aims to create tool which will calculate disk usage statistics 
of docker registry.

## Instalation
Project requires at least Python3.6, next just install package into virtualenv (or system if you don't mind)

```
pip install gitlab-registry git+https://github.com/pbabics/docker-registry-statistics.git@master
```

## Usage
Usage is fairly simple:
```
docker_registry_statistics  <Path to registry> <Command>
```

Right now these are implemented commands:
  * `statistics`
  * `orphaned_images`
  * `unused_blobs`

Note that registry path should contain directory structure like `docker/registry/v2/...`
for example this directory for Gitlab by default is `/var/opt/gitlab/gitlab-rails/shared/registry`.


### `statistics` command
Goes through all tags, images and blobs and sumarized disk usage statistics, per repository and overall disk usage of registry.

### `orphaned_images` command
Lists all images that are no longer used as a current image for tag under which they were pushed.

### `unused_blobs` command
Lists all blobs that are not used by any image and are just using up disk space.
