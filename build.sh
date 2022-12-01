#!/bin/bash -eux

build_prometheus() {
  # Prometheus version
  VERSION="2.40.2"
  wget https://github.com/prometheus/prometheus/releases/download/v${VERSION}/prometheus-${VERSION}.linux-amd64.tar.gz -O /workspace/prometheus-${VERSION}.tar.gz -c

  rpmbuild \
  	--clean \
  	--define "pkgversion ${VERSION}" \
  	--define "_topdir /tmp/rpm" \
  	--define "_sourcedir /workspace" \
  	-bb /workspace/prometheus.spec

  cp /tmp/rpm/x86_64/*.rpm /workspace/build/
}

build_alertmanager() {
  # alertmanager version
  VERSION="0.24.0"
  wget https://github.com/prometheus/alertmanager/releases/download/v${VERSION}/alertmanager-${VERSION}.linux-amd64.tar.gz -O /workspace/alertmanager/alertmanager-${VERSION}.tar.gz -c

  rpmbuild \
  	--clean \
  	--define "pkgversion ${VERSION}" \
  	--define "_topdir /tmp/rpm" \
  	--define "_sourcedir /workspace/alertmanager" \
	-bb /workspace/alertmanager/prometheus-alertmanager.spec

  cp /tmp/rpm/x86_64/*.rpm /workspace/build/
}

build_postgres_exporter() {
  # postgres_exporter version
  VERSION="0.11.1"
  wget https://github.com/prometheus-community/postgres_exporter/releases/download/v${VERSION}/postgres_exporter-${VERSION}.linux-amd64.tar.gz -O /workspace/exporters/postgres_exporter-${VERSION}.tar.gz -c
  wget https://raw.githubusercontent.com/prometheus-community/postgres_exporter/v${VERSION}/queries.yaml -O /workspace/exporters/queries.yaml

  rpmbuild \
    --clean \
    --define "pkgversion ${VERSION}" \
    --define "_topdir /tmp/rpm" \
    --define "_sourcedir /workspace/exporters" \
    -bb /workspace/exporters/prometheus-postgres-exporter.spec

  cp /tmp/rpm/x86_64/*.rpm /workspace/build/
}

build_node_exporter() {
  # node_exporter version
  VERSION="1.4.0"
  wget https://github.com/prometheus/node_exporter/releases/download/v${VERSION}/node_exporter-${VERSION}.linux-amd64.tar.gz -O /workspace/exporters/node_exporter-${VERSION}.tar.gz -c

  rpmbuild \
    --clean \
    --define "pkgversion ${VERSION}" \
    --define "_topdir /tmp/rpm" \
    --define "_sourcedir /workspace/exporters" \
    -bb /workspace/exporters/prometheus-node-exporter.spec

  cp /tmp/rpm/x86_64/*.rpm /workspace/build/
}


sudo yum install wget epel-release -y
sudo mkdir -p /workspace/build/
sudo chown builder: /workspace/build/

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
