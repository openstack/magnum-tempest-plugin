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

while ${KUBECTL} get pods -A -o wide | grep -q "ContainerCreating";
do
    count=$(( $count+1 ))
    if [ "$count" = "10" ]; then
        echo "ERROR: Waiting for pods to exit ContainerCreating state timed out"
        exit 1
    else
        sleep 60
    fi
done

${KUBECTL} get all -A -o wide > ${LOG_DIR}/kubectl_get_all

for ns in $(${KUBECTL} get -o name namespace); do
    mkdir -p ${LOG_DIR}/pods/${ns#*/}
    for pod in $(${KUBECTL} get -n ${ns#*/} -o name pod); do
        ${KUBECTL} -n ${ns#*/} describe pod ${pod#*/} > ${LOG_DIR}/pods/${ns#*/}/${pod#*/}_describe
        ${KUBECTL} -n ${ns#*/} logs ${pod#*/} > ${LOG_DIR}/pods/${ns#*/}/${pod#*/}
    done
done

# NOTE(mnasiadka): Fail if any pod is not Running
FAILED_PODS=$(${KUBECTL} get pods -A --field-selector=status.phase!=Running)

if [ ! -z "${FAILED_PODS}" ]; then
    echo "ERROR: Detected pods in state other than Running"
    echo ${FAILED_PODS}
    exit 1
fi

