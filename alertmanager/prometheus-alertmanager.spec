%define debug_package %{nil}
%global pkgname prometheus-alertmanager
%{!?pkgrevision: %global pkgrevision 1}
%if 0%{?rhel} == 7
 %define dist .el7
%endif

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Handles alerts sent by client applications such as the Prometheus server.
License:       Apache-2.0
Source0:       alertmanager-%{version}.tar.gz
Source1:       %{pkgname}.service
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Alertmanager handles alerts sent by client applications such as the
Prometheus server.

%prep
%setup -q -n alertmanager-%{version}.linux-amd64

%build

%pre
if ! getent passwd prometheus &>/dev/null ; then
  useradd \
    --system --user-group --shell /sbin/nologin \
    --home-dir /var/lib/prometheus \
    --comment "Prometheus User" prometheus &>/dev/null
fi

%install
%{__install} -d -m 755 %{buildroot}/etc/prometheus
%{__install} -m 640 alertmanager.yml %{buildroot}/etc/prometheus

%{__install} -D -m 755 alertmanager %{buildroot}%{_bindir}/alertmanager
%{__install} -D -m 755 amtool %{buildroot}%{_bindir}/amtool

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{pkgname}.service

%{__install} -d -m 750 %{buildroot}/var/lib/prometheus/alertmanager

%files
%defattr(-,prometheus,prometheus)
%config(noreplace) /etc/prometheus/alertmanager.yml
%attr(-, root, root) /usr/bin/alertmanager
%attr(-, root, root) /usr/bin/amtool
%attr(-, root, root) %{_unitdir}/%{pkgname}.service
%dir /var/lib/prometheus/alertmanager

%changelog
* Wed Jun 02 2021 Alexandre Pereira <alexandre.pereira@dalibo.com> - 0.21.0-1
- Initial packaging
