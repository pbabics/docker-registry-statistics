from setuptools import setup



setup(
	name = 'docker-registry-statistics',
	version = '0.0.3',
	description = 'Tool which will calculates disk usage statistics of docker registry',
	long_description = open('README.md').read(),
	long_description_content_type = 'text/markdown',
	author = 'Peter Babics',
	author_email = 'peter.ntx@gmail.com',
	url = 'https://github.com/pbabics/docker-registry-statistics/',
	keywords = 'docker registry gitlab statistics',
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
	},
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Topic :: System :: Monitoring',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
	project_urls = {
		'Bug Reports': 'https://github.com/pbabics/docker-registry-statistics/issues',
		'Source': 'https://github.com/pbabics/docker-registry-statistics/',
	}
)
