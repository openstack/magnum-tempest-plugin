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
COPY_LOG_HELPER = "magnum_tempest_plugin/tests/contrib/copy_instance_logs.sh"
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
    def copy_logs_handler(cls, get_nodes_fn, coe, keypair):
        """Copy logs closure.

        This method will retrieve all running nodes for a specified cluster
        and copy addresses from there locally.

        :param get_nodes_fn: function that takes no parameters and returns
            a list of node IPs which are in such form:
                [[master_nodes], [slave_nodes]].
        :param coe: the COE type of the nodes
        """
        def int_copy_logs():
            try:
                func_name = "test"
                msg = ("Failed to copy logs for cluster")
                nodes_addresses = get_nodes_fn()
                master_nodes = nodes_addresses[0]
                slave_nodes = nodes_addresses[1]

                base_path = os.path.split(os.path.dirname(
                    os.path.abspath(magnum_tempest_plugin.__file__)))[0]
                full_location = os.path.join(base_path, COPY_LOG_HELPER)

                def do_copy_logs(prefix, nodes_address):
                    if not nodes_address:
                        return

                    msg = "copy logs from : %s" % ','.join(nodes_address)
                    cls.LOG.info(msg)
                    log_name = prefix + "-" + func_name
                    for node_address in nodes_address:
                        try:
                            cls.LOG.debug("running %s", full_location)
                            cls.LOG.debug("keypair: %s", keypair)
                            subprocess.check_call([
                                full_location,
                                node_address,
                                coe,
                                log_name,
                                str(keypair)
                            ])
                        except Exception:
                            cls.LOG.error(msg)
                            msg = (
                                "failed to copy from %(node_address)s "
                                "to %(base_path)s%(log_name)s-"
                                "%(node_address)s" %
                                {'node_address': node_address,
                                 'base_path': "/opt/stack/logs/magnum-nodes/",
                                 'log_name': log_name})
                            cls.LOG.exception(msg)
                            raise

                do_copy_logs('master', master_nodes)
                do_copy_logs('node', slave_nodes)
            except Exception:
                cls.LOG.exception(msg)
                raise

        return int_copy_logs()

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
