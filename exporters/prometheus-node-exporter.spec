%define debug_package %{nil}
%global pkgname prometheus-node-exporter
%{!?pkgrevision: %global pkgrevision 1}
%if 0%{?rhel} == 7
 %define dist .el7
%endif

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Prometheus exporter for hardware and OS metrics
License:       Apache License 2.0
URL:           https://github.com/prometheus/node_exporter

Source0:       node_exporter-%{version}.tar.gz
Source1:       %{pkgname}.service
Source2:       node_exporter.conf
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%setup -n node_exporter-%{version}.linux-amd64

%build

%pre
if ! getent passwd prometheus &>/dev/null ; then
  useradd \
    --system --user-group --shell /sbin/nologin \
    --home-dir /var/lib/prometheus \
    --comment "Prometheus User" prometheus &>/dev/null
fi

%install
%{__install} -d %{buildroot}/var/lib/prometheus
%{__install} -d %{buildroot}%{_unitdir}
%{__install} -d -m 750 %{buildroot}/etc/prometheus

%{__install} -D -m 755 node_exporter %{buildroot}%{_bindir}/node_exporter
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{pkgname}.service
%{__install} -m 640 %{SOURCE2} %{buildroot}/etc/prometheus

%files
%defattr(-,root,root,-)
%attr(-,prometheus,prometheus) %config(noreplace) /etc/prometheus/node_exporter.conf
%{_bindir}/node_exporter
%{_unitdir}/%{pkgname}.service

%changelog
* Tue Jun 01 2021 Alexandre Pereira <alexandre.pereira@dalibo.com> - 1.1.2-1
- Initial packaging
