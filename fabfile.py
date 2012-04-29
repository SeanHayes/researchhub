# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes

import researchhub.settings as dj_settings
from fabric.api import local, run, sudo, env, prompt, settings, cd
from fabric.contrib.files import exists
from fabric.decorators import roles
import json
import logging
import os
import string

logging.getLogger('').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

env.user = 'sean'

#env.hosts = ['sean@50.56.208.20',]
env.hosts = ['108.171.187.214',]


env.roledefs['web'] = ['108.171.187.214',]
env.roledefs['cache'] = ['108.171.187.214',]
env.roledefs['db'] = ['108.171.187.214',]
env.roledefs['celery'] = []

env.code_dir = '/srv/'

env.project_name = dj_settings.PROJECT_MODULE
env.project_parent_dir = dj_settings.PROJECT_PARENT_DIR
env.project_dir = '%s%s/' % (env.code_dir, dj_settings.PROJECT_MODULE,)
env.package_dir = '%s%s/' % (env.project_dir, dj_settings.PROJECT_MODULE,)
env.project_git_uri = 'ssh://sean@seanhayes.name/development/researchhub/'
env.config_dir = '%sconfig/generated/' % env.project_dir

env.pip_dir = '%spip/' % env.code_dir

env.celery_script_dir = '%scelery/init.d/' % env.config_dir

main_dirs = [
#	env.code_dir,
	env.pip_dir,
]

project_dirs = [
	'/%s/logs/' % env.project_dir,
]

apt_packages = [
	'debconf-utils',
	'git',
	'mercurial',
	'gdebi-core',
	'graphviz',
	'graphviz-dev',
	'libmemcached-tools',
	'memcached',
	'nginx',
	'pkg-config',
	'postfix',
	'python-pip',
	'python-virtualenv',
	'python-dev',
	'postgresql',
	#'rabbitmq-server',
	#TODO: try to get as many of these as possible in requirements.txt
	#'python-django-doc',
	#some require 1/4 GB of dependencies to build the PIP version, which is unacceptable for this kind of application
	'python-imaging',
	'python-psycopg2',
	#'python-exactimage',
	#'python-crypto',
]

#Run the following to make binary eggs when setuptools isn't used
#python -c "import setuptools; execfile('setup.py')" bdist_egg

# tasks

def create_user():
	"Create admin user on fresh cloud instance."
	username = prompt('Enter username to create: ', default=env.user)
	with settings(user='root'):
		run('useradd --groups sudo,www-data -d /home/%s -m %s' % (username, username))
		run('passwd %s' % username)

def switch_to_bash():
	"switch from dash (the Ubuntu default) to bash"
	with cd('/bin'):
		#has to be one command since each call to sudo() is a different session,
		#and you can't login if sh isn't set
		sudo('rm sh; ln -s bash sh')

def set_django_colors():
	local('export DJANGO_COLORS="%s"' % dj_settings.DJANGO_COLORS)

@roles('db')
def setup_pgsql():
	"Sets up PostgreSQL user and databases."
	name = prompt('Enter PostgreSQL role/db to create: ', default=env.project_name)
	sudo('createuser -s -P %s' % name, user='postgres')
	sudo('createdb -O %s %s' % (name, name), user='postgres')
	#sudo('createdb -O %s celery_results' % name, user='postgres')

def mkdirs(dirs):
	"Sets up the directories we need and sets the right permissions."
	for d in dirs:
		if not exists(d):
			sudo('mkdir %s' % d)
			sudo('chown %s:www-data %s' % (env.user, d))
			sudo('chmod 775 %s' % d)

def upgrade_ubuntu():
	"Probably shouldn't run this through Fabric, but here's the commands for it anyway."
	sudo('apt-get install update-manager-core')
	#edit /etc/update-manager/release-upgrades, set Prompt=normal
	sudo('do-release-upgrade')

def install_apt():
	"Updates package list, upgrades all packages to latest available version, and installs Apt dependencies for this project."
	sudo('apt-get update')
	sudo('apt-get upgrade')
	sudo('apt-get install -f %s' % string.join(apt_packages, ' '))

def install_pip():
	"Installs the PIP requirements for this project."
	with cd(env.pip_dir):
		sudo('pip install -r %srequirements.txt' % env.project_dir)

def install_project():
	"Clones this project's Git repo if there's no copy on the target machine, else it pulls the latest version."
	if exists(env.project_dir):
		with cd(env.project_dir):
			run('git pull origin master')
	else:
		with cd(env.code_dir):
			run('git clone %s' % env.project_git_uri)
		sudo('chown -R %s:www-data %s' % (env.user, env.project_dir))
		sudo('chmod 775 %s' % env.project_dir)
			
		mkdirs(project_dirs)

def install():
	"Runs the commands to create all necessary directories, install Apt and PIP dependencies, and install project files."
	mkdirs(main_dirs)
	install_apt()
	sudo('chown :www-data %s' % (env.code_dir,))
	sudo('chmod 775 %s' % env.code_dir)
	install_project()
	install_pip()

def refresh_config_files():
	"Regenerates dynamic config files using django-config-gen."
	with cd(env.project_dir):
		run('./manage.py config_gen')

def link_config_file(source, destination):
	with settings(warn_only=True):
		sudo('rm %s' % destination)
	sudo('ln -s %s %s' % (source, destination))

@roles('web')
def config_nginx():
	with settings(warn_only=True):
		sudo('rm /etc/nginx/sites-available/*')
	link_config_file(os.path.join(env.config_dir, 'nginx'), '/etc/nginx/sites-available/default')

@roles('db')
def config_postgresql():
	link_config_file(os.path.join(env.config_dir, 'pg_hba.conf'), '/etc/postgresql/9.1/main/pg_hba.conf')

@roles('cache')
def config_memcached():
	link_config_file(os.path.join(env.config_dir, 'memcached.conf'), '/etc/memcached.conf')

@roles('celery')
def config_celery():
	"Links Celery's Debian init scripts to /etc/init.d/."
	init_list=string.split(run('ls %s' % env.celery_script_dir))
	
	for script in init_list:
		p = '/etc/init.d/%s' % script
		link_config_file(os.path.join(env.celery_script_dir, script), p)
	
	link_config_file(os.path.join(env.config_dir, 'celery/celeryd_default'), '/etc/default/celeryd')

def config_tzdata():
	"Configures the time zone for the server."
	run('echo \'America/New_York\'| sudo tee /etc/timezone')
	sudo('dpkg-reconfigure -f noninteractive tzdata')

def config():
	"Runs the commands to generate config files using django-config-gen and symlinks the generated files to the normal config file locations for Apache, Nginx, Memcached, etc."
	refresh_config_files()
	config_nginx()
	config_memcached()
	config_celery()
	config_tzdata()

def restart_servers():
	"Restarts Apache, Nginx, Rabbit MQ, and Celery."
	sudo('/etc/init.d/nginx restart')
	#sudo('/etc/init.d/rabbitmq-server restart')
	sudo('/etc/init.d/celeryd restart')
	sudo('/etc/init.d/celerybeat restart')
	sudo('/etc/init.d/celeryevcam restart')
	sudo('/etc/init.d/memcached restart')

def reload_servers():
	"Reloads Apache, Nginx, Rabbit MQ, and Celery where possible, otherwise it restarts them. Reloading config files is faster than restarting the processes."
	sudo('/etc/init.d/nginx reload')
	#sudo('/etc/init.d/rabbitmq-server reload')
	sudo('/etc/init.d/celeryd restart')#no reload
	sudo('/etc/init.d/celerybeat restart')#no reload
	sudo('/etc/init.d/celeryevcam restart')#no reload
	sudo('/etc/init.d/memcached restart')#no reload

def venv():
	run('virtualenv --no-site-packages virtualenv')
	run('pip install -I -E virtualenv -r requirements.txt')

#local development scripts
fixtures = {
	'user': ['auth.User'],
	'sites': ['sites'],
	'flatpages': ['flatpages'],
	'djcelery': ['djcelery'],
	'researchhub_app': ['researchhub_app'],
}

def reload_db():
	"""
	Deletes and recreates the DB, runs sync and migrations, and loads fixtures.
	
	If PG whines about encoding differences, see: https://wiki.archlinux.org/index.php/PostgreSQL#Change_Default_Encoding_of_New_Databases_To_UTF-8_.28Optional.29
	"""
	local('%s/manage.py reset_db --noinput --router=default' % dj_settings.PROJECT_ROOT)
	local('%s/manage.py syncdb --migrate --noinput' % dj_settings.PROJECT_ROOT)
	for k in fixtures:
		local('%s/manage.py loaddata %s' % (dj_settings.PROJECT_ROOT, k))
	local('%s/manage.py loaddata the_rest' % dj_settings.PROJECT_ROOT)
	#local('%s/manage.py createsuperuser --username=sean --email=sean@seanhayes.name' % dj_settings.PROJECT_ROOT)

def backup_fixtures():
	exclude = []
	for k, v in fixtures.items():
		local('%s/manage.py dumpdata --format=json --indent=4 --natural %s > %s/%s.json' % (dj_settings.PROJECT_ROOT, ' '.join(v), dj_settings.MAIN_FIXTURE_DIR, k))
		exclude.extend(v)
	
	for e in exclude:
		e = '--exclude=%s' % e
	local('%s/manage.py dumpdata --format=json --indent=4 --natural --exclude=contenttypes --exclude=admin %s > %s/the_rest.json' % (dj_settings.PROJECT_ROOT, ' '.join(exclude), dj_settings.MAIN_FIXTURE_DIR))

def check_for_pdb():
	"Easily check for instances of pdb.set_trace() in your code before committing."
	local('find . -name \'*.py\'|xargs grep \'pdb.set_trace\'')
	#TODO: handle exit code

def start_local_env():
	local('sudo /etc/init.d/nginx start')
	local('sudo /etc/init.d/postgresql start')
	#local('sudo /etc/init.d/rabbitmq-server start')
	local('sudo /etc/init.d/celeryd start')
	local('sudo /etc/init.d/celerybeat start')
	local('sudo /etc/init.d/celeryevcam start')
	local('sudo /etc/init.d/memcached start')

def restart_local_env():
	local('sudo /etc/init.d/nginx restart')
	local('sudo /etc/init.d/postgresql restart')
	#local('sudo /etc/init.d/rabbitmq-server restart')
	local('sudo /etc/init.d/celeryd restart')
	local('sudo /etc/init.d/celerybeat restart')
	local('sudo /etc/init.d/celeryevcam restart')
	local('sudo /etc/init.d/memcached restart')

def stop_local_env():
	local('sudo /etc/init.d/nginx stop')
	local('sudo /etc/init.d/postgresql stop')
	#local('sudo /etc/init.d/rabbitmq-server stop')
	local('sudo /etc/init.d/celeryd stop')
	local('sudo /etc/init.d/celerybeat stop')
	local('sudo /etc/init.d/celeryevcam stop')
	local('sudo /etc/init.d/memcached stop')
