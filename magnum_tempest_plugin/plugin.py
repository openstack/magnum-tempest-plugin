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


import os

from tempest import config
from tempest.test_discover import plugins

from magnum_tempest_plugin import config as magnum_config


class MagnumTempestPlugin(plugins.TempestPlugin):
    def load_tests(self):
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(__file__)))[0]
        test_dir = "magnum_tempest_plugin/tests/api/v1"
        full_test_dir = os.path.join(base_path, test_dir)
        return full_test_dir, base_path

    def register_opts(self, conf):
        conf.register_opt(magnum_config.service_option,
                          group='service_available')
        conf.register_opt(magnum_config.magnum_scope_enforcement,
                          group='enforce_scope')
        conf.register_group(magnum_config.magnum_group)
        conf.register_opts(magnum_config.MagnumGroup, group='magnum')

    def get_opt_lists(self):
        return [
            (magnum_config.magnum_group.name, magnum_config.MagnumGroup),
            ('service_available', [magnum_config.service_option]),
            ('enforce_scope', [magnum_config.magnum_scope_enforcement])
        ]

    def get_service_clients(self):
        magnum_config = config.service_client_config('magnum')
        v1_params = {
            'name': 'magnum_v1',
            'service_version': 'magnum.v1',
            'module_path': 'magnum_tempest_plugin.tests.api.v1.clients',
            'client_names': [
                'CertClient', 'ClusterTemplateClient',
                'ClusterClient', 'MagnumServiceClient'
            ]
        }
        v1_params.update(magnum_config)
        return [v1_params]
