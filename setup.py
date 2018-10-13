from setuptools import setup



setup(
	name = 'docker-registry-statistics',
	version = '0.0.1',
	description = 'A useful module',
	author = 'Peter Babics',
	author_email = 'peter.ntx@gmail.com',
	license = 'GNU GPLv3',
	packages = [
		'docker_registry_statistics',
		'docker_registry_statistics.commands'
	],
	install_requires = [
		'click>=6.7,<7.0',
		'attrs>=18.0,<19.0'
	],
	entry_points = {
		'console_scripts': [
			'docker-registry-statistics = docker_registry_statistics.__main__:cli'
		]
	}
)
