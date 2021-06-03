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

%description
postgres_exporter is an Prometheus exporter for PostgreSQL server metrics.

%prep
%setup -n postgres_exporter-%{version}.linux-amd64

%build

%pre
# Create system user now to let rpm chown %files.
if ! getent passwd postgres &>/dev/null ; then
  useradd \
    --system --user-group --shell /bin/bash \
    --home-dir /var/lib/pgsql \
    --comment "PostgreSQL user" postgres &>/dev/null
fi

%install
%{__install} -d %{buildroot}/var/lib/prometheus
%{__install} -d %{buildroot}%{_unitdir}

%{__install} -D -m 755 postgres_exporter %{buildroot}%{_bindir}/postgres_exporter
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{pkgname}.service
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/prometheus/postgres_exporter.conf
%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/postgres_exporter_queries-pg13.yaml
%{__install} -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/prometheus/postgres_exporter_queries.yaml


%files
%defattr(-,root,root,-)
%{_bindir}/postgres_exporter
%{_unitdir}/%{pkgname}.service
%config(noreplace) %{_sysconfdir}/prometheus/postgres_exporter.conf
%config(noreplace) %{_sysconfdir}/prometheus/postgres_exporter_queries.yaml
%config(noreplace) %{_sysconfdir}/prometheus/postgres_exporter_queries-pg13.yaml

%changelog
* Tue Jun 01 2021 Alexandre Pereira <alexandre.pereira@dalibo.com> - 0.9.0-1
- Initial packaging
