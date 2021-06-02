%define debug_package %{nil}
%global pkgname alertmanager
%{!?pkgrevision: %global pkgrevision 1}
%if 0%{?rhel} == 7
 %define dist .el7
%endif

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Handles alerts sent by client applications such as the Prometheus server.
License:       Apache-2.0
Source0:       %{pkgname}-%{version}.tar.gz
Source1:       %{pkgname}.service
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Alertmanager handles alerts sent by client applications such as the Prometheus server.

%prep
%setup -q -n %{pkgname}-%{version}.linux-amd64

%build

%pre

%install
%{__install} -d %{buildroot}/etc/prometheus
%{__install} -d %{buildroot}/etc/systemd/system/

install -D alertmanager %{buildroot}%{_bindir}/alertmanager
install -D amtool %{buildroot}%{_bindir}/amtool

cp -r alertmanager.yml %{buildroot}/etc/prometheus

%{__install} -m 0644 %{SOURCE1} %{buildroot}/etc/systemd/system

%files
%defattr(-,prometheus,prometheus)
/etc/prometheus
/usr/bin/alertmanager
/usr/bin/amtool
%attr(-, root, root) /etc/systemd/system/alertmanager.service

%changelog
* Wed Jun 02 2021 Alexandre Pereira <alexandre.pereira@dalibo.com> - 0.21.0-1
- Initial packaging
