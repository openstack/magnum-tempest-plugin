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


from magnum_tempest_plugin.common.templates import cluster_template


class ClusterTemplateTest(cluster_template.ClusterTemplateTestTemplate):

    """Tests for clustertemplate CRUD."""

    def __init__(self, *args, **kwargs):
        super(ClusterTemplateTest, self).__init__(*args, **kwargs)
        self.cluster_template_client = None
        self.keypairs_client = None

    def setUp(self):
        try:
            super(ClusterTemplateTest, self).setUp()
            (self.cluster_template_client,
             self.keypairs_client) = self.get_clients_with_new_creds(
                 type_of_creds='default',
                 request_type='cluster_template')
            self.ct_reader_client = self.cluster_template_client
            self.ct_member_client = self.cluster_template_client
        except Exception:
            self.tearDown()
            raise
