%define debug_package %{nil}
%global pkgname prometheus-postgres-exporter
%{!?pkgrevision: %global pkgrevision 1}
%if 0%{?rhel} == 7
 %define dist .el7
%endif

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Prometheus exporter for PostgreSQL server metrics.
License:       Apache License 2.0
URL:           https://github.com/prometheus-community/postgres_exporter

Source0:       postgres_exporter-%{version}.tar.gz
Source1:       %{pkgname}.service
Source2:       postgres_exporter.conf
Source3:       queries-pg13.yaml
Source4:       queries.yaml
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes:     postgres_exporter

%description
postgres_exporter is an Prometheus exporter for PostgreSQL server metrics.

%prep
%setup -n postgres_exporter-%{version}.linux-amd64

%build

%pre
# Create system user now to let rpm chown %files.
if ! getent passwd postgres &>/dev/null ; then
    groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
    useradd -M -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
        -c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :
fi

%install
%{__install} -d %{buildroot}/var/lib/prometheus
%{__install} -d %{buildroot}%{_unitdir}

%{__install} -D -m 755 postgres_exporter %{buildroot}%{_bindir}/postgres_exporter
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{pkgname}.service
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/prometheus/postgres_exporter.conf
%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/prometheus/postgres_exporter_queries-pg13.yaml
%{__ln_s} -r %{buildroot}%{_datadir}/prometheus/postgres_exporter_queries-pg13.yaml %{buildroot}%{_datadir}/prometheus/postgres_exporter_queries-pg14.yaml
%{__install} -D -m 644 %{SOURCE4} %{buildroot}%{_datadir}/prometheus/postgres_exporter_queries.yaml
for x in 10 11 12; do
    %{__ln_s} -r %{buildroot}%{_datadir}/prometheus/postgres_exporter_queries.yaml %{buildroot}%{_datadir}/prometheus/postgres_exporter_queries-pg${x}.yaml
done


%files
%defattr(-,root,root,-)
%{_bindir}/postgres_exporter
%{_unitdir}/%{pkgname}.service
%config(noreplace) %{_sysconfdir}/prometheus/postgres_exporter.conf
%{_datadir}/prometheus/postgres_exporter_queries.yaml
%{_datadir}/prometheus/postgres_exporter_queries-pg*.yaml

%changelog
* Mon Nov 15 2021 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 0.10.0-1
- Update to 0.10.0
- Install queries for all supported versions of PostgreSQL as of Nov 2021
- Install queries in /usr/share
- Create the same user as the PostgreSQL server RPM from PGDG

* Tue Jun 01 2021 Alexandre Pereira <alexandre.pereira@dalibo.com> - 0.9.0-1
- Initial packaging
