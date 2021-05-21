%define debug_package %{nil}
%global pkgname node_exporter
%{!?pkgrevision: %global pkgrevision 1}
%if 0%{?rhel} == 7
 %define dist .el7
%endif

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Prometheus exporter for hardware and OS metrics
License:       Apache License 2.0
URL:           https://github.com/prometheus/%{pkgname}

Source0:       %{pkgname}-%{version}.tar.gz
Source1:       %{pkgname}.service
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Prometheus exporter for hardware and OS metrics exposed by *NIX kernels, written in Go with pluggable metric collectors.

%prep
%setup -n %{pkgname}-%{version}.linux-amd64

%build

%pre

%install
%{__install} -d %{buildroot}/var/lib/prometheus
%{__install} -d %{buildroot}%{_sysconfdir}/systemd/system

%{__install} -D -m 755 %{pkgname} %{buildroot}%{_bindir}/%{pkgname}
%{__install} -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/systemd/system

%files
%defattr(-,root,root,-)
%{_bindir}/%{pkgname}
%{_sysconfdir}/systemd/system/%{pkgname}.service
