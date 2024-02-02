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

# Save trace setting
XTRACE=$(set +o | grep xtrace)
set -o xtrace

echo "Magnum's copy_instance_logs.sh was called..."

SSH_IP=$1
COE=${2-kubernetes}
NODE_TYPE=${3-master}
LOG_PATH=/tmp/magnum-nodes/${NODE_TYPE}-${SSH_IP}
KEYPAIR=${4-default}

PRIVATE_KEY=

echo "If private key is specified, save to temp and use that; else, use default"
if [[ "$KEYPAIR" == "default" ]]; then
    PRIVATE_KEY=$(readlink -f ~/.ssh/id_rsa_magnum)
else
    PRIVATE_KEY="$(mktemp id_rsa_magnum.$SSH_IP.XXX)"
    echo -en "$KEYPAIR" > $PRIVATE_KEY
fi

function remote_exec {
    local ssh_user=$1
    local cmd=$2
    local logfile=${LOG_PATH}/$3
    ssh -i $PRIVATE_KEY -o StrictHostKeyChecking=no ${ssh_user}@${SSH_IP} "${cmd}" > ${logfile} 2>&1
}

mkdir -p $LOG_PATH

if [[ "$COE" == "kubernetes" ]]; then
    SSH_USER=core
    remote_exec $SSH_USER "sudo systemctl --full list-units --no-pager" systemctl_list_units.log
    remote_exec $SSH_USER "sudo journalctl -u kubelet --no-pager" kubelet.log
    remote_exec $SSH_USER "sudo journalctl -u kube-proxy --no-pager" kube-proxy.log
    remote_exec $SSH_USER "sudo journalctl -u etcd --no-pager" etcd.log
    remote_exec $SSH_USER "sudo journalctl -u kube-apiserver --no-pager" kube-apiserver.log
    remote_exec $SSH_USER "sudo journalctl -u kube-scheduler --no-pager" kube-scheduler.log
    remote_exec $SSH_USER "sudo journalctl -u kube-controller-manager --no-pager" kube-controller-manager.log
    remote_exec $SSH_USER "sudo journalctl -u docker --no-pager" docker.log
    remote_exec $SSH_USER "sudo systemctl status docker -l" docker.service.status.log
    remote_exec $SSH_USER "sudo systemctl show docker --no-pager" docker.service.show.log
    remote_exec $SSH_USER "sudo timeout 60s docker ps --all=true --no-trunc=true" docker-containers.log
    remote_exec $SSH_USER "sudo ip a" ipa.log
    remote_exec $SSH_USER "sudo netstat -an" netstat.log
    remote_exec $SSH_USER "sudo df -h" dfh.log
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/heat-params" heat-params
    remote_exec $SSH_USER "sudo cat /etc/etcd/etcd.conf" etcd.conf
    remote_exec $SSH_USER "sudo cat /etc/kubernetes/config" kubernetes-config
    remote_exec $SSH_USER "sudo cat /etc/kubernetes/apiserver" kubernetes-apiserver-config
    remote_exec $SSH_USER "sudo cat /etc/kubernetes/controller-manager" kubernetes-controller-config
    remote_exec $SSH_USER "sudo cat /etc/kubernetes/kubelet" kubelet-config
    remote_exec $SSH_USER "sudo cat /etc/kubernetes/proxy" kubernetes-proxy-config
    remote_exec $SSH_USER "sudo cat /etc/kubernetes/kube_openstack_config" kube_openstack_config
    remote_exec $SSH_USER "sudo journalctl --no-pager -u heat-container-agent" heat-container-agent.log
    remote_exec $SSH_USER "sudo cat /var/log/heat-config/heat-config-script/*kube_cluster*" heat-kube-cluster.log
    remote_exec $SSH_USER "sudo cat /var/log/heat-config/heat-config-script/*kube_masters*" heat-kube-masters.log
    remote_exec $SSH_USER "sudo cat /var/log/heat-config/heat-config-script/*kube_minions*" heat-kube-minions.log
elif [[ "$COE" == "swarm" || "$COE" == "swarm-mode" ]]; then
    SSH_USER=fedora
    remote_exec $SSH_USER "sudo systemctl --full list-units --no-pager" systemctl_list_units.log
    remote_exec $SSH_USER "sudo journalctl -u cloud-config --no-pager" cloud-config.log
    remote_exec $SSH_USER "sudo journalctl -u cloud-final --no-pager" cloud-final.log
    remote_exec $SSH_USER "sudo journalctl -u cloud-init-local --no-pager" cloud-init-local.log
    remote_exec $SSH_USER "sudo journalctl -u cloud-init --no-pager" cloud-init.log
    remote_exec $SSH_USER "sudo cat /var/log/cloud-init-output.log" cloud-init-output.log
    remote_exec $SSH_USER "sudo journalctl -u etcd --no-pager" etcd.log
    remote_exec $SSH_USER "sudo journalctl -u swarm-manager --no-pager" swarm-manager.log
    remote_exec $SSH_USER "sudo journalctl -u swarm-agent --no-pager" swarm-agent.log
    remote_exec $SSH_USER "sudo journalctl -u swarm-worker --no-pager" swarm-worker.log
    remote_exec $SSH_USER "sudo journalctl -u docker-storage-setup --no-pager" docker-storage-setup.log
    remote_exec $SSH_USER "sudo systemctl status docker-storage-setup -l" docker-storage-setup.service.status.log
    remote_exec $SSH_USER "sudo systemctl show docker-storage-setup --no-pager" docker-storage-setup.service.show.log
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/docker-storage-setup 2>/dev/null" docker-storage-setup.sysconfig.env.log
    remote_exec $SSH_USER "sudo journalctl -u docker --no-pager" docker.log
    remote_exec $SSH_USER "sudo journalctl -u docker-containerd --no-pager" docker-containerd.log
    remote_exec $SSH_USER "sudo systemctl status docker.socket -l" docker.socket.status.log
    remote_exec $SSH_USER "sudo systemctl show docker.socket --no-pager" docker.socket.show.log
    remote_exec $SSH_USER "sudo systemctl status docker -l" docker.service.status.log
    remote_exec $SSH_USER "sudo systemctl show docker --no-pager" docker.service.show.log
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/docker" docker.sysconfig.env.log
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/docker-storage" docker-storage.sysconfig.env.log
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/docker-network" docker-network.sysconfig.env.log
    remote_exec $SSH_USER "sudo timeout 60s docker ps --all=true --no-trunc=true" docker-containers.log
    remote_exec $SSH_USER "sudo tar zcvf - /var/lib/docker/containers 2>/dev/null" docker-container-configs.tar.gz
    remote_exec $SSH_USER "sudo journalctl -u flanneld --no-pager" flanneld.log
    remote_exec $SSH_USER "sudo ip a" ipa.log
    remote_exec $SSH_USER "sudo netstat -an" netstat.log
    remote_exec $SSH_USER "sudo df -h" dfh.log
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/heat-params" heat-params
    remote_exec $SSH_USER "sudo cat /etc/etcd/etcd.conf" etcd.conf
    remote_exec $SSH_USER "sudo ls -lR /etc/docker" docker-certs
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/flanneld" flanneld.sysconfig
    remote_exec $SSH_USER "sudo cat /etc/sysconfig/flannel-network.json" flannel-network.json.sysconfig
    remote_exec $SSH_USER "sudo cat /usr/local/bin/flannel-docker-bridge" bin-flannel-docker-bridge
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/docker.service.d/flannel.conf" docker-flannel.conf
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/flanneld.service.d/flannel-docker-bridge.conf" flannel-docker-bridge.conf
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/flannel-docker-bridge.service" flannel-docker-bridge.service
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/swarm-manager.service" swarm-manager.service
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/swarm-manager-failure.service" swarm-manager-failure.service
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/swarm-agent.service" swarm-agent.service
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/swarm-agent-failure.service" swarm-agent-failure.service
    remote_exec $SSH_USER "sudo cat /etc/systemd/system/swarm-worker.service" swarm-worker.service
    remote_exec $SSH_USER "sudo cat /usr/local/bin/magnum-start-swarm-manager" bin-magnum-start-swarm-manager
    remote_exec $SSH_USER "sudo cat /usr/local/bin/magnum-start-swarm-worker" bin-magnum-start-swarm-worker
else
    echo "ERROR: Unknown COE '${COE}'"
    EXIT_CODE=1
fi

# Restore xtrace
$XTRACE

exit $EXIT_CODE
