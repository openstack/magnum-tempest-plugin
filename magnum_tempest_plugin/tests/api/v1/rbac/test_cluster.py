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
import abc

from magnum_tempest_plugin.common.templates import cluster
from magnum_tempest_plugin.tests.api.v1.rbac import base

IDEMPOTENT_IDS = {
    "test_delete_cluster_for_nonexisting_cluster": (
        "09589881-e3c1-4507-9ded-55994e46963f"),
    "test_update_cluster_for_nonexisting_cluster": (
        "145d02ee-a804-476a-948f-727099c3525d"),
    "test_create_cluster_with_nonexisting_flavor": (
        "a08f129e-b0cb-411b-9cc0-e6b97db3d6d7"),
    "test_create_cluster_with_zero_masters": (
        "9eee202d-77a0-43e0-b5e3-657ab5d46835"),
    "test_create_cluster_with_zero_nodes": (
        "bdfb3894-d970-4e35-95b3-fec3e8a717ae"),
    "test_create_cluster_for_nonexisting_cluster_template": (
        "f3be4b27-62f1-46d4-8c07-8b7315a2b4c3"),
    "test_create_list_sign_delete_clusters": (
        "b03cb130-d2ca-4721-8298-b491020d72db"),
}


class ClusterTest(base.RbacBaseTests,
                  cluster.ClusterTestTemplate,
                  metaclass=abc.ABCMeta):

    """Tests for cluster CRUD with RBAC."""

    @classmethod
    def tearDownClass(cls):
        if cls.delete_template:
            cls._delete_cluster_template(cls.cluster_template.uuid)
        super(ClusterTest, cls).tearDownClass()

    def setUp(self):
        super(ClusterTest, self).setUp()
        self._setup_cluster_template()
