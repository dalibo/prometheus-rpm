#!/bin/bash -eux

build_prometheus() {
  # Prometheus version
  VERSION="2.27.1"
  sudo wget https://github.com/prometheus/prometheus/releases/download/v${VERSION}/prometheus-${VERSION}.linux-amd64.tar.gz -O /workspace/prometheus-${VERSION}.tar.gz

  sudo rpmbuild \
  	--clean \
  	--define "pkgversion ${VERSION}" \
  	--define "_topdir ${PWD}/tmp/rpm" \
  	--define "_sourcedir ${PWD}/workspace" \
  	-bb /workspace/prometheus.spec

  sudo cp ${PWD}/tmp/rpm/RPMS/*/*.rpm ${PWD}/workspace/build/
}

build_alertmanager() {
  # alertmanager version
  VERSION="0.21.0"
  sudo wget https://github.com/prometheus/alertmanager/releases/download/v${VERSION}/alertmanager-${VERSION}.linux-amd64.tar.gz -O /workspace/alertmanager/alertmanager-${VERSION}.tar.gz

  sudo rpmbuild \
  	--clean \
  	--define "pkgversion ${VERSION}" \
  	--define "_topdir ${PWD}/tmp/rpm" \
  	--define "_sourcedir ${PWD}/workspace/alertmanager" \
  	-bb /workspace/alertmanager/alertmanager.spec

  sudo cp ${PWD}/tmp/rpm/RPMS/*/*.rpm ${PWD}/workspace/build/
}

build_postgres_exporter() {
  # postgres_exporter version
  VERSION="0.9.0"
  sudo wget https://github.com/prometheus-community/postgres_exporter/releases/download/v${VERSION}/postgres_exporter-${VERSION}.linux-amd64.tar.gz -O /workspace/exporters/postgres_exporter-${VERSION}.tar.gz
  sudo wget https://raw.githubusercontent.com/prometheus-community/postgres_exporter/v${VERSION}/queries.yaml -O /workspace/exporters/queries.yaml

  sudo rpmbuild \
    --clean \
    --define "pkgversion ${VERSION}" \
    --define "_topdir ${PWD}/tmp/rpm" \
    --define "_sourcedir ${PWD}/workspace/exporters" \
    -bb /workspace/exporters/prometheus-postgres-exporter.spec

  sudo cp ${PWD}/tmp/rpm/RPMS/*/*.rpm ${PWD}/workspace/build/
}

build_node_exporter() {
  # node_exporter version
  VERSION="1.1.2"
  sudo wget https://github.com/prometheus/node_exporter/releases/download/v${VERSION}/node_exporter-${VERSION}.linux-amd64.tar.gz -O /workspace/exporters/node_exporter-${VERSION}.tar.gz

  sudo rpmbuild \
    --clean \
    --define "pkgversion ${VERSION}" \
    --define "_topdir ${PWD}/tmp/rpm" \
    --define "_sourcedir ${PWD}/workspace/exporters" \
    -bb /workspace/exporters/prometheus-node-exporter.spec

  sudo cp ${PWD}/tmp/rpm/RPMS/*/*.rpm ${PWD}/workspace/build/
}


sudo yum install wget epel-release -y
sudo mkdir -p ${PWD}/workspace/build/

case $1 in
  prometheus )
  build_prometheus
    ;;
  alertmanager )
  build_alertmanager
    ;;
  postgres_exporter )
  build_postgres_exporter
    ;;
  node_exporter )
  build_node_exporter
    ;;
  all )
  build_prometheus
  build_postgres_exporter
  build_node_exporter
  build_alertmanager
    ;;
  *)    # unknown option
  echo "Unknown option."
  exit 1
  ;;
esac
