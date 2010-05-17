Summary:	A scalable and highly available distributed key-value store
Name:		kumofs
Version:	0.4.2
Release:	1%{?dist}
Group:		Development/Libraries
License:	Apache License
URL:		http://code.etolabo.com/kumofs
Source0:	http://github.com/etolabo/kumofs/downloads/%{name}-%{version}.tar.gz
Source10:	kumofs-kumo-manager.sysinit
Source11:	kumofs-kumo-manager.sysconfig
Source12:	kumofs-kumo-manager.logrotate
Source20:	kumofs-kumo-server.sysinit
Source21:	kumofs-kumo-server.sysconfig
Source22:	kumofs-kumo-server.logrotate
Source30:	kumofs-kumo-gateway.sysinit
Source31:	kumofs-kumo-gateway.sysconfig
Source32:	kumofs-kumo-gateway.logrotate
Requires:	tokyocabinet >= 1.4.10
Requires:	msgpack >= 0.3.1
BuildRequires:	gcc >= 4.1
BuildRequires:	ruby >= 1.8.6
BuildRequires:	tokyocabinet-devel >= 1.4.10
BuildRequires:	msgpack-devel >= 0.3.1
BuildRequires:	openssl
BuildRequires:	zlib
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
kumofs is a scalabe and highly available distributed key-value store.

%package manager
Summary:        kumo-manager manages kumo-servers.
Group:		Development/Libraries
Requires:       kumofs = %{version}-%{release}

%description manager
kumo-manager manages kumo-servers.

%package server
Summary:        kumo-server stores actual data. 
Group:		Development/Libraries
Requires:       kumofs = %{version}-%{release}

%description server
kumo-server stores actual data. \
You can add kumo-servers after  buiding the  cluster.

%package gateway
Summary:        kumo-server stores actual data. 
Group:		Development/Libraries

%description gateway
kumo-gateway receives requests from applications and \
relays it to the kumo-servers.

%prep
if [ -z `/usr/bin/gem list -l msgpack` ]; then
    echo "Could not found msgpack gem."
    exit 1
fi

%setup -q

%build
%{configure} --prefix=/usr 
%{__make} %{?_smp_mflags}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT

# init script
install -Dp -m0755 %{SOURCE10} $RPM_BUILD_ROOT%{_initrddir}/kumo-manager
install -Dp -m0755 %{SOURCE20} $RPM_BUILD_ROOT%{_initrddir}/kumo-server
install -Dp -m0755 %{SOURCE30} $RPM_BUILD_ROOT%{_initrddir}/kumo-gateway

# sysconfig
install -Dp -m0644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/kumo-manager
install -Dp -m0644 %{SOURCE21} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/kumo-server
install -Dp -m0644 %{SOURCE31} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/kumo-gateway

# logrotate
install -Dp -m0644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/kumo-manager
install -Dp -m0644 %{SOURCE22} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/kumo-server
install -Dp -m0644 %{SOURCE32} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/kumo-gateway

%preun

%post

%postun

%post manager
/sbin/chkconfig --add kumo-manager

%preun manager
if [ $1 -lt 1 ]; then
  /sbin/service kumo-manager stop > /dev/null 2>&1
  /sbin/chkconfig --del kumo-manager
fi

%post server
/sbin/chkconfig --add kumo-server

%preun server
if [ $1 -lt 1 ]; then
  /sbin/service kumo-server stop > /dev/null 2>&1
  /sbin/chkconfig --del kumo-server
fi

%post gateway
/sbin/chkconfig --add kumo-gateway

%preun gateway
if [ $1 -lt 1 ]; then
  /sbin/service kumo-gateway stop > /dev/null 2>&1
  /sbin/chkconfig --del kumo-gateway
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildrootndir}


%files
%defattr(-,root,root)
%{_bindir}/kumoctl
%{_bindir}/kumohash
%{_bindir}/kumolog
%{_bindir}/kumomergedb
%{_bindir}/kumostat
%{_bindir}/kumotop
%{_mandir}/man1/kumoctl.1.gz
%{_mandir}/man1/kumohash.1.gz
%{_mandir}/man1/kumolog.1.gz
%{_mandir}/man1/kumomergedb.1.gz
%{_mandir}/man1/kumostat.1.gz
%{_mandir}/man1/kumotop.1.gz

%files manager
%defattr(-,root,root)
%{_bindir}/kumo-manager
%{_mandir}/man1/kumo-manager.1.gz
%{_initrddir}/kumo-manager
%{_sysconfdir}/logrotate.d/kumo-manager
%config(noreplace) %{_sysconfdir}/sysconfig/kumo-manager

%files server
%defattr(-,root,root)
%{_bindir}/kumo-server
%{_mandir}/man1/kumo-server.1.gz
%{_initrddir}/kumo-server
%{_sysconfdir}/logrotate.d/kumo-server
%config(noreplace) %{_sysconfdir}/sysconfig/kumo-server

%files gateway
%defattr(-,root,root)
%{_bindir}/kumo-gateway
%{_mandir}/man1/kumo-gateway.1.gz
%{_initrddir}/kumo-gateway
%{_sysconfdir}/logrotate.d/kumo-gateway
%config(noreplace) %{_sysconfdir}/sysconfig/kumo-gateway

%changelog
* Sat May 15 2010 Naoya Nakazawa <naoya.n@gmail.com> - 1.4.5-1
- Updated to version 1.4.5

* Tue Jan 19 2010 Naoya Nakazawa <naoya.n@gmail.com> - 0.3.0-1
- Initial Version

