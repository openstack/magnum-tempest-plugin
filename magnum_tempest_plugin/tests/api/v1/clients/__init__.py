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

from magnum_tempest_plugin.tests.api.v1.clients.cert_client \
    import CertClient
from magnum_tempest_plugin.tests.api.v1.clients.cluster_client \
    import ClusterClient
from magnum_tempest_plugin.tests.api.v1.clients.cluster_template_client \
    import ClusterTemplateClient
from magnum_tempest_plugin.tests.api.v1.clients.magnum_service_client \
    import MagnumServiceClient


__all__ = [
    'CertClient',
    'ClusterClient',
    'ClusterTemplateClient',
    'MagnumServiceClient'
]
