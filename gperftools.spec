# NOTE: shared /%{_lib}/libtcmalloc* is useless without /usr/%{_lib}/libstdc++.so.6
#
Summary:	Fast, multi-threaded malloc and performance analysis tools
Summary(pl.UTF-8):	Szybka, wielowątkowa implementacja malloc i narzędzia do analizy wydajności
Name:		gperftools
Version:	2.0
Release:	1
License:	BSD
Group:		Libraries
# Source0Download: http://code.google.com/p/gperftools/downloads/list
Source0:	http://gperftools.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	13f6e8961bc6a26749783137995786b6
Patch0:		%{name}-glibc216-siginfo_t.patch
URL:		http://code.google.com/p/gperftools/
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
%ifarch %{x8664} ia64
BuildRequires:	libunwind-devel >= 0.98.6
%endif
Requires:	libtcmalloc = %{version}-%{release}
Obsoletes:	google-perftools < 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly
heap-checker, a heap profiler, and a cpu-profiler.

%description -l pl.UTF-8
Perf Tools to zbiór narzędzi do analizy wydajności, zawierający także
bardzo wydajną, wielowątkową implementację malloc(), działającą dobrze
w szczególności z wątkami i STL-em, a także przyjazne wątkom narzędzie
do kontroli sterty, profilter sterty oraz profile wykorzystania CPU.

%package devel
Summary:	Development files of perftools libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek perftools
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libtcmalloc-devel = %{version}-%{release}
Obsoletes:	google-perftools-devel < 2.0

%description devel
The google-perftools-devel package contains the header files needed to
develop applications with google-perftools libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe niezbędne do tworzenia aplikacji z
użyciem bibliotek google-perftools.

%package static
Summary:	Static perftools libraries
Summary(pl.UTF-8):	Statyczne biblioteki perftools
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	google-perftools-static < 2.0

%description static
The google-perftools-static package contains the static libraries of
google-perftools.

%description static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne google-perftools.

%package -n libtcmalloc
Summary:	Fast, multi-threaded malloc by Google
Summary(pl.UTF-8):	Szybka, wielowątkowa implementacja malloc firmy Google
Group:		Libraries
Conflicts:	google-perftools < 1.8.3-3

%description -n libtcmalloc
Fast, multi-threaded malloc by Google.

%description -n libtcmalloc -l pl.UTF-8
Szybka, wielowątkowa implementacja malloc firmy Google.

%package -n libtcmalloc-devel
Summary:	Fast, multi-threaded malloc by Google - header files
Summary(pl.UTF-8):	Szybka, wielowątkowa implementacja malloc firmy Google - pliki nagłówkowe
Group:		Development/Libraries
Requires:	libstdc++-devel
Requires:	libtcmalloc = %{version}-%{release}

%description -n libtcmalloc-devel
Fast, multi-threaded malloc by Google - header files.

%description -n libtcmalloc-devel -l pl.UTF-8
Szybka, wielowątkowa implementacja malloc firmy Google - pliki
nagłówkowe.

%package -n libtcmalloc-static
Summary:	Fast, multi-threaded malloc by Google - static libraries
Summary(pl.UTF-8):	Szybka, wielowątkowa implementacja malloc firmy Google - biblioteki statyczne
Group:		Development/Libraries
Requires:	libtcmalloc-devel = %{version}-%{release}

%description -n libtcmalloc-static
Fast, multi-threaded malloc by Google - static libraries.

%description -n libtcmalloc-static -l pl.UTF-8
Szybka, wielowątkowa implementacja malloc firmy Google - biblioteki
statyczne.

%prep
%setup -q
%patch0 -p1

%build
%configure \
%ifnarch %{x8664} ia64
	ac_cv_lib_unwind_backtrace=no
%endif

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

# clean docdir
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n libtcmalloc -p /sbin/ldconfig
%postun	-n libtcmalloc -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# note: INSTALL contains many perftools-specific notes
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO doc/*{html,png,gif,txt}
%attr(755,root,root) %{_bindir}/pprof
%attr(755,root,root) %{_libdir}/libprofiler.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprofiler.so.0
%attr(755,root,root) %{_libdir}/libtcmalloc_and_profiler.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtcmalloc_and_profiler.so.4
%attr(755,root,root) %{_libdir}/libtcmalloc_debug.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtcmalloc_debug.so.4
%attr(755,root,root) %{_libdir}/libtcmalloc_minimal_debug.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtcmalloc_minimal_debug.so.4
%{_mandir}/man1/pprof.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtcmalloc_and_profiler.so
%attr(755,root,root) %{_libdir}/libtcmalloc_debug.so
%attr(755,root,root) %{_libdir}/libtcmalloc_minimal_debug.so
%attr(755,root,root) %{_libdir}/libprofiler.so
%{_libdir}/libtcmalloc_and_profiler.la
%{_libdir}/libtcmalloc_debug.la
%{_libdir}/libtcmalloc_minimal_debug.la
%{_libdir}/libprofiler.la
%{_includedir}/google/profiler.h
%{_includedir}/gperftools/profiler.h
%{_pkgconfigdir}/libprofiler.pc
%{_pkgconfigdir}/libtcmalloc_debug.pc
%{_pkgconfigdir}/libtcmalloc_minimal_debug.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libprofiler.a
%{_libdir}/libtcmalloc_and_profiler.a
%{_libdir}/libtcmalloc_debug.a
%{_libdir}/libtcmalloc_minimal_debug.a

%files -n libtcmalloc
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libtcmalloc.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libtcmalloc.so.4
%attr(755,root,root) /%{_lib}/libtcmalloc_minimal.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libtcmalloc_minimal.so.4

%files -n libtcmalloc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtcmalloc.so
%attr(755,root,root) %{_libdir}/libtcmalloc_minimal.so
%{_libdir}/libtcmalloc.la
%{_libdir}/libtcmalloc_minimal.la
%dir %{_includedir}/google
%{_includedir}/google/heap-*.h
%{_includedir}/google/malloc_extension*.h
%{_includedir}/google/malloc_hook*.h
%{_includedir}/google/stacktrace.h
%{_includedir}/google/tcmalloc.h
%dir %{_includedir}/gperftools
%{_includedir}/gperftools/heap-*.h
%{_includedir}/gperftools/malloc_extension*.h
%{_includedir}/gperftools/malloc_hook*.h
%{_includedir}/gperftools/stacktrace.h
%{_includedir}/gperftools/tcmalloc.h
%{_pkgconfigdir}/libtcmalloc.pc
%{_pkgconfigdir}/libtcmalloc_minimal.pc

%files -n libtcmalloc-static
%defattr(644,root,root,755)
%{_libdir}/libtcmalloc.a
%{_libdir}/libtcmalloc_minimal.a
