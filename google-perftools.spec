Summary:	Fast, multi-threaded malloc and performance analysis tools
Name:		google-perftools
Version:	1.8.3
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://google-perftools.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	70c95322c9bac97e67f0162e4cc55996
URL:		http://code.google.com/p/google-perftools/
BuildRequires:	libtool
%ifarch %{x8664}
BuildRequires:	libunwind-devel >= 0.98.6
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly
heap-checker, a heap profiler, and a cpu-profiler.

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
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for pkg in libtcmalloc libtcmalloc_minimal; do
	mv $RPM_BUILD_ROOT%{_libdir}/${pkg}.so.* \
		$RPM_BUILD_ROOT/%{_lib}
	ln -snf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/${pkg}.so.*.*.*) \
		$RPM_BUILD_ROOT/%{_libdir}/${pkg}.so
done

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%doc doc/*{html,png,gif,txt}
%attr(755,root,root) %{_bindir}/pprof
%ghost %{_libdir}/libprofiler.so.0
%attr(755,root,root) %{_libdir}/libprofiler.so.*.*.*
%ghost /%{_lib}/libtcmalloc.so.0
%attr(755,root,root) /%{_lib}/libtcmalloc.so.*.*.*
%ghost %{_libdir}/libtcmalloc_and_profiler.so.0
%attr(755,root,root) %{_libdir}/libtcmalloc_and_profiler.so.*.*.*
%ghost %{_libdir}/libtcmalloc_debug.so.0
%attr(755,root,root) %{_libdir}/libtcmalloc_debug.so.*.*.*
%ghost /%{_lib}/libtcmalloc_minimal.so.0
%attr(755,root,root) /%{_lib}/libtcmalloc_minimal.so.*.*.*
%ghost %{_libdir}/libtcmalloc_minimal_debug.so.0
%attr(755,root,root) %{_libdir}/libtcmalloc_minimal_debug.so.*.*.*
%{_mandir}/man1/pprof.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtcmalloc_and_profiler.so
%{_libdir}/libprofiler.la
%{_libdir}/libprofiler.so
%{_libdir}/libtcmalloc.la
%{_libdir}/libtcmalloc.so
%{_libdir}/libtcmalloc_and_profiler.la
%{_libdir}/libtcmalloc_debug.la
%{_libdir}/libtcmalloc_debug.so
%{_libdir}/libtcmalloc_minimal.la
%{_libdir}/libtcmalloc_minimal.so
%{_libdir}/libtcmalloc_minimal_debug.la
%{_libdir}/libtcmalloc_minimal_debug.so
%{_pkgconfigdir}/libprofiler.pc
%{_pkgconfigdir}/libtcmalloc.pc
%{_pkgconfigdir}/libtcmalloc_debug.pc
%{_pkgconfigdir}/libtcmalloc_minimal.pc
%{_pkgconfigdir}/libtcmalloc_minimal_debug.pc
%dir %{_includedir}/google
%{_includedir}/google/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libprofiler.a
%{_libdir}/libtcmalloc.a
%{_libdir}/libtcmalloc_and_profiler.a
%{_libdir}/libtcmalloc_debug.a
%{_libdir}/libtcmalloc_minimal.a
%{_libdir}/libtcmalloc_minimal_debug.a
