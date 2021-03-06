%define debug_package %{nil}
%global pkgname prometheus
%if 0%{?rhel} == 7
  %define dist .el7
%endif

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       2%{?dist}
Summary:       An open-source systems monitoring and alerting toolkit with an active ecosystem.
License:       Apache License 2.0
URL:           https://prometheus.io/
Source0:       %{pkgname}-%{version}.tar.gz
Source1:       prometheus.service
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Prometheus is a complete open-source monitoring solution with a time series
database. It offers a language and API for external display tools like Grafana,
alerting and a rich set of probes

%prep
%setup -q -n %{pkgname}-%{version}.linux-amd64

%build

%pre
# Create system user now to let rpm chown %files.
if ! getent passwd prometheus &>/dev/null ; then
  useradd \
    --system --user-group --shell /sbin/nologin \
    --home-dir /var/lib/prometheus \
    --comment "Prometheus Web UI" prometheus &>/dev/null
fi

%install
%{__install} -d -m 750 %{buildroot}/var/lib/prometheus
%{__cp} -r consoles %{buildroot}/var/lib/prometheus
%{__cp} -r console_libraries %{buildroot}/var/lib/prometheus
%{__install} -d -m 750 %{buildroot}/var/lib/prometheus/data

%{__install} -d -m 755 %{buildroot}/etc/prometheus
%{__install} -m 640 prometheus.yml %{buildroot}/etc/prometheus

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/prometheus.service

%{__install} -d -m 755 %{buildroot}/usr/bin
%{__install} -m 755 prometheus %{buildroot}/usr/bin/prometheus
%{__install} -m 755 promtool %{buildroot}/usr/bin/promtool




%files
%defattr(-,prometheus,prometheus)
%config(noreplace) /etc/prometheus/prometheus.yml
/var/lib/prometheus/consoles
/var/lib/prometheus/console_libraries
/var/lib/prometheus/data
%attr(-,root,root)/usr/bin/prometheus
%attr(-,root,root)/usr/bin/promtool
%attr(-, root, root) %{_unitdir}/prometheus.service

%changelog
* Fri Jun 04 2021 Nicolas Thauvin <nicolas.thauvin@dalibo.com> - 2.27.1-2
- Bump revision after enhancing packaging

* Fri May 21 2021 Alexandre Pereira <alexandre.pereira@dalibo.com> - 2.27.1-1
- Initial packaging
