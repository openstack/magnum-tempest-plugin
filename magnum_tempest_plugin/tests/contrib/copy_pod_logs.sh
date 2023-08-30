#!/usr/bin/env bash
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

set -o xtrace

LOG_DIR="/tmp/magnum-nodes/kubernetes/"
KUBECTL="/opt/stack/bin/kubectl --kubeconfig /tmp/magnum-nodes/kube.conf"
mkdir -p ${LOG_DIR}

${KUBECTL} get all -A -o wide > ${LOG_DIR}/kubectl_get_all

for ns in $(${KUBECTL} get -o name namespace); do
    mkdir -p ${LOG_DIR}/pods/${ns#*/}
    for pod in $(${KUBECTL} get -n ${ns#*/} -o name pod); do
        ${KUBECTL} -n ${ns#*/} logs ${pod#*/} > ${LOG_DIR}/pods/${ns#*/}/${pod#*/}
    done
done