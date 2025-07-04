# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ast

from tempest import config


CONF = config.CONF


class Config(object):

    """Parses configuration to attributes required for auth and test data"""

    @classmethod
    def set_admin_creds(cls, config):
        cls.admin_user = CONF.auth.admin_username
        cls.admin_passwd = CONF.auth.admin_password
        cls.admin_tenant = CONF.auth.admin_project_name

    @classmethod
    def set_user_creds(cls, config):
        # normal user creds
        # Fixme(eliqiao): this is quick workaround to passing tempest
        # legacy credentials provider is removed by tempest
        # I8c24cd17f643083dde71ab2bd2a38417c54aeccb.
        # TODO(eliqiao): find a way to using an accounts.yaml file
        # check Ia5132c5cb32355d6f26b8acdd92a0e55a2c19f41
        cls.user = CONF.auth.admin_username
        cls.passwd = CONF.auth.admin_password
        cls.tenant = CONF.auth.admin_project_name

    @classmethod
    def set_auth_version(cls, config):
        # auth version for client authentication
        cls.auth_version = CONF.identity.auth_version

    @classmethod
    def set_auth_url(cls, config):
        # auth_url for client authentication
        if cls.auth_version == 'v3':
            cls.auth_v3_url = CONF.identity.uri_v3
        else:
            if 'uri' not in CONF.identity:
                raise Exception('config missing auth_url key')
            cls.auth_url = CONF.identity.uri

    @classmethod
    def set_admin_role(cls, config):
        # admin_role for client authentication
        if cls.auth_version == 'v3':
            cls.admin_role = CONF.identity.admin_role
        else:
            cls.admin_role = 'admin'

    @classmethod
    def set_docker_storage_driver(cls, config):
        cls.docker_storage_driver = CONF.magnum.get('docker_storage_driver')

    @classmethod
    def set_region(cls, config):
        if 'region' in CONF.identity:
            cls.region = CONF.identity.region
        else:
            cls.region = 'RegionOne'

    @classmethod
    def set_image_id(cls, config):
        if 'image_id' not in CONF.magnum:
            raise Exception('config missing image_id key')
        cls.image_id = CONF.magnum.image_id

    @classmethod
    def set_nic_id(cls, config):
        if 'nic_id' not in CONF.magnum:
            raise Exception('config missing nic_id key')
        cls.nic_id = CONF.magnum.nic_id

    @classmethod
    def set_keypair_name(cls, config):
        if 'keypair_name' not in CONF.magnum:
            raise Exception('config missing keypair_name key')
        cls.keypair_name = CONF.magnum.keypair_name

    @classmethod
    def set_flavor_id(cls, config):
        if 'flavor_id' not in CONF.magnum:
            raise Exception('config missing flavor_id key')
        cls.flavor_id = CONF.magnum.flavor_id

    @classmethod
    def set_magnum_url(cls, config):
        cls.magnum_url = CONF.magnum.get('magnum_url', None)

    @classmethod
    def set_master_flavor_id(cls, config):
        if 'master_flavor_id' not in CONF.magnum:
            raise Exception('config missing master_flavor_id key')
        cls.master_flavor_id = CONF.magnum.master_flavor_id

    @classmethod
    def set_dns_nameserver(cls, config):
        if 'dns_nameserver' not in CONF.magnum:
            raise Exception('config missing dns_nameserver')
        cls.dns_nameserver = CONF.magnum.dns_nameserver

    @classmethod
    def set_copy_logs(cls, config):
        cls.copy_logs = CONF.magnum.get('copy_logs', True)
        cls.copy_logs_success = CONF.magnum.get('copy_logs_success', True)

    @classmethod
    def set_coe(cls, config):
        cls.coe = CONF.magnum.coe

    @classmethod
    def set_network_driver(cls, config):
        cls.network_driver = CONF.magnum.network_driver

    @classmethod
    def set_cluster_template_id(cls, config):
        cls.cluster_template_id = CONF.magnum.cluster_template_id

    @classmethod
    def set_cluster_creation_timeout(cls, config):
        cls.cluster_creation_timeout = CONF.magnum.cluster_creation_timeout

    @classmethod
    def set_labels(cls, config):
        cls.labels = ast.literal_eval(CONF.magnum.labels)

    @classmethod
    def setUp(cls):
        cls.set_admin_creds(config)
        cls.set_user_creds(config)
        cls.set_auth_version(config)
        cls.set_auth_url(config)
        cls.set_admin_role(config)

        cls.set_docker_storage_driver(config)
        cls.set_region(config)
        cls.set_image_id(config)
        cls.set_nic_id(config)
        cls.set_keypair_name(config)
        cls.set_flavor_id(config)
        cls.set_magnum_url(config)
        cls.set_master_flavor_id(config)
        cls.set_dns_nameserver(config)
        cls.set_copy_logs(config)
        cls.set_coe(config)
        cls.set_network_driver(config)
        cls.set_cluster_template_id(config)
        cls.set_cluster_creation_timeout(config)
        cls.set_labels(config)
