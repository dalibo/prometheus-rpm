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
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%setup -n node_exporter-%{version}.linux-amd64

%build

%pre

%install
%{__install} -d %{buildroot}/var/lib/prometheus
%{__install} -d %{buildroot}%{_sysconfdir}/systemd/system

%{__install} -D -m 755 node_exporter %{buildroot}%{_bindir}/node_exporter
%{__install} -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/system

%files
%defattr(-,root,root,-)
%{_bindir}/node_exporter
%{_sysconfdir}/systemd/system/%{pkgname}.service
