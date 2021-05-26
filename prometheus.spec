%define debug_package %{nil}
%global pkgname prometheus
%{!?pkgrevision: %global pkgrevision 1}

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
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
%{__install} -d %{buildroot}/var/lib/prometheus
%{__install} -d %{buildroot}/etc/prometheus

%{__install} -d %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/prometheus.service

%{__install} -d -m 755 %{buildroot}/usr/bin
%{__install} -m 755 prometheus %{buildroot}/usr/bin/prometheus
%{__install} -m 755 promtool %{buildroot}/usr/bin/promtool

cp -r consoles %{buildroot}/etc/prometheus
cp -r console_libraries/ %{buildroot}/etc/prometheus
cp prometheus.yml %{buildroot}/etc/prometheus


%files
%defattr(-,prometheus,prometheus)
/etc/prometheus
/var/lib/prometheus
%attr(-,root,root)/usr/bin/prometheus
%attr(-,root,root)/usr/bin/promtool
%attr(-, root, root) %{_unitdir}/prometheus.service

%changelog
* Fri May 21 2021 Alexandre Pereira <alexandre.pereira@dalibo.com> - 2.27.1-1
- Initial packaging
