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

from magnum_tempest_plugin.common import config
from magnum_tempest_plugin.common.templates import cluster

IDEMPOTENT_IDS = {
    "test_delete_cluster_for_nonexisting_cluster": (
        "376c45ea-a857-11e9-9382-00224d6b7bc1"),
    "test_update_cluster_for_nonexisting_cluster": (
        "33bd0416-a857-11e9-9382-00224d6b7bc1"),
    "test_create_cluster_with_nonexisting_flavor": (
        "2cf16528-a857-11e9-9382-00224d6b7bc1"),
    "test_create_cluster_with_zero_masters": (
        "29c6c5f0-a857-11e9-9382-00224d6b7bc1"),
    "test_create_cluster_with_zero_nodes": (
        "262eb132-a857-11e9-9382-00224d6b7bc1"),
    "test_create_cluster_for_nonexisting_cluster_template": (
        "11c293da-a857-11e9-9382-00224d6b7bc1"),
    "test_create_list_sign_delete_clusters": (
        "44158a8c-a856-11e9-9382-00224d6b7bc1"),
}


class ClusterTest(cluster.ClusterTestTemplate):

    """Tests for cluster CRUD."""

    @classmethod
    def setUpClass(cls):
        super(ClusterTest, cls).setUpClass()

        try:
            (cls.creds, cls.keypair) = cls.get_credentials_with_keypair(
                type_of_creds='default'
            )
            (cls.cluster_template_client,
             cls.keypairs_client) = cls.get_clients_with_existing_creds(
                creds=cls.creds,
                type_of_creds='default',
                request_type='cluster_template'
            )
            cls.ct_reader_client = cls.cluster_template_client
            cls.ct_member_client = cls.cluster_template_client
            cls.ct_admin_client = cls.cluster_template_client
            (cls.cluster_client, _) = cls.get_clients_with_existing_creds(
                creds=cls.creds,
                type_of_creds='default',
                request_type='cluster'
            )
            cls.cluster_reader_client = cls.cluster_client
            cls.cluster_member_client = cls.cluster_client
            cls.cluster_admin_client = cls.cluster_client
            (cls.cert_client, _) = cls.get_clients_with_existing_creds(
                creds=cls.creds,
                type_of_creds='default',
                request_type='cert'
            )
            cls.cert_reader_client = cls.cert_client
            cls.cert_member_client = cls.cert_client
            cls.cert_admin_client = cls.cert_client

            cls._setup_cluster_template()
        except Exception:
            raise

    @classmethod
    def tearDownClass(cls):
        if cls.delete_template:
            cls._delete_cluster_template(cls.cluster_template.uuid)

        if config.Config.keypair_name:
            cls.keypairs_client.delete_keypair(config.Config.keypair_name)

        super(ClusterTest, cls).tearDownClass()
