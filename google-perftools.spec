#
Summary:	Fast, multi-threaded malloc and performance analysis tools
Name:		google-perftools
Version:	0.98
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://google-perftools.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	be6d283bb6177f1febaefd3570f3366d
URL:		http://code.google.com/p/google-perftools/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
%ifarch %{x8664}
BuildRequires:	libunwind >= 0.98.6
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Perf Tools is a collection of a high-performance multi-threaded
malloc() implementation, plus some pretty nifty performance analysis
tools.

%package devel
Summary:	Development files of perftools library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libao2-devel

%description devel
The google-perftools-devel package contains the header files and
documentation needed to develop applications with google-perftools.

%package static
Summary:	Static perftools library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The google-perftools-static package contains the static libraries of
google-perftools.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%doc doc/*{html,png,gif,txt}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so.*.*.*
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/google

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
