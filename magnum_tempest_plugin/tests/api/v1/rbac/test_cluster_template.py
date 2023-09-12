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

from magnum_tempest_plugin.common.templates import cluster_template
from magnum_tempest_plugin.tests.api.v1.rbac import base


class ClusterTemplateTest(base.RbacBaseTests,
                          cluster_template.ClusterTemplateTestTemplate,
                          metaclass=abc.ABCMeta):
    """Tests for clustertemplate CRUD with RBAC."""
