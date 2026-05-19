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

import logging
import os
import subprocess

from tempest import config
from tempest import test

import magnum_tempest_plugin


CONF = config.CONF
COPY_PODLOG_HELPER = "magnum_tempest_plugin/tests/contrib/copy_pod_logs.sh"


class BaseMagnumTest(test.BaseTestCase):
    """Sets up configuration required for functional tests"""

    LOG = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super(BaseMagnumTest, self).__init__(*args, **kwargs)

    @classmethod
    def skip_checks(cls):
        super(BaseMagnumTest, cls).skip_checks()

        if not CONF.service_available.magnum:
            skip_msg = ("%s skipped as magnum is not available"
                        % cls.__name__)
            raise cls.skipException(skip_msg)

    @classmethod
    def copy_pod_logs(cls):
        """Copy pod logs

        This method will retrieve all pod logs using bash script,
        expects a kube.config file under /tmp/magnum-nodes/
        """
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(magnum_tempest_plugin.__file__)))[0]
        full_location = os.path.join(base_path, COPY_PODLOG_HELPER)

        try:
            cls.LOG.debug("running %s", full_location)
            subprocess.check_call([full_location])
        except Exception as e:
            cls.LOG.exception(e)
            raise
