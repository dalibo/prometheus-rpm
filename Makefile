RPM_DIST?=centos7
#RPM_DIST?=centos8

all:
	PKG=all docker-compose run --rm $(RPM_DIST)

prometheus:
	PKG=prometheus docker-compose run --rm $(RPM_DIST)

prometheus-alertmanager:
	PKG=alertmanager docker-compose run --rm $(RPM_DIST)

postgres_exporter:
	PKG=postgres_exporter docker-compose run --rm $(RPM_DIST)

node_exporter:
	PKG=node_exporter docker-compose run --rm $(RPM_DIST)

clean:
	rm -f build/* \
				prometheus-*.tar.gz \
				exporters/postgres_exporter-*.tar.gz \
				exporters/node_exporter-*.tar.gz \
				alertmanager/alertmanager-*.tar.gz
