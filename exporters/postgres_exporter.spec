%define debug_package %{nil}
%global pkgname postgres_exporter
%{!?pkgrevision: %global pkgrevision 1}
%if 0%{?rhel} == 7
 %define dist .el7
%endif

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Prometheus exporter for PostgreSQL server metrics.
License:       Apache License 2.0
URL:           https://github.com/prometheus-community/%{pkgname}

Source0:       %{pkgname}-%{version}.tar.gz
Source1:       %{pkgname}.service
Source2:       %{pkgname}.default
Source3:       queries-pg13.yaml
Source4:       queries.yaml
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
postgres_exporter is an Prometheus exporter for PostgreSQL server metrics.

%prep
%setup -n %{pkgname}-%{version}.linux-amd64

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
%{__install} -d %{buildroot}%{_sysconfdir}/systemd/system

%{__install} -D -m 755 postgres_exporter %{buildroot}%{_bindir}/%{pkgname}
%{__install} -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/system
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/prometheus/%{pkgname}.conf
%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{pkgname}_queries-pg13.yaml
%{__install} -D -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/prometheus/%{pkgname}_queries.yaml


%files
%defattr(-,root,root,-)
%{_bindir}/%{pkgname}
%{_sysconfdir}/systemd/system/%{pkgname}.service
%config(noreplace) %{_sysconfdir}/prometheus/%{pkgname}.conf
%config(noreplace) %{_sysconfdir}/prometheus/%{pkgname}_queries.yaml
%config(noreplace) %{_sysconfdir}/prometheus/%{pkgname}_queries-pg13.yaml
