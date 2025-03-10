#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	python2		# CPython 2.x module
#
Summary:	A library to check account numbers and bank codes of German banks
Summary(pl.UTF-8):	Biblioteka do sprawdzania numerów kont i kodów bankowych niemieckich banków
Name:		ktoblzcheck
Version:	1.53
Release:	
License:	LGPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/ktoblzcheck/%{name}-%{version}.tar.gz
# Source0-md5:	5cedb258370acd22ec3d0c90e0e66fec
Patch0:		%{name}-static.patch
Patch1:		%{name}-python.patch
URL:		https://ktoblzcheck.sourceforge.net/
BuildRequires:	cmake >= 3.0
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
%{?with_python2:BuildRequires:	python-modules >= 1:2.6}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KtoBLZCheck is a library to check account numbers and bank codes of
German banks.

Both a library for other programs as well as a short command-line tool
is available. It is possible to check pairs of account numbers and
bank codes (BLZ) of German banks, and to map bank codes (BLZ) to the
clear-text name and location of the bank.

%description -l pl.UTF-8
KtoBLZCheck to biblioteka do sprawdzania numerów kont i kodów
bankowych niemieckich banków.

Dostępna jest zarówno biblioteka jak i proste narzędzie działające z
linii poleceń. Pozwalają na sprawdzenie par numerów kont i kodów
bankowych (BLZ) niemieckich banków oraz na zamianę kodów bankowych
(BLZ) na tekstową nazwę oraz lokalizację banku.

%package devel
Summary:	Header files for KtoBLZCheck library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki KtoBLZCheck
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for KtoBLZCheck library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki KtoBLZCheck.

%package static
Summary:	Static KtoBLZCheck library
Summary(pl.UTF-8):	Statyczna biblioteka KtoBLZCheck
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static KtoBLZCheck library.

%description static -l pl.UTF-8
Statyczna biblioteka KtoBLZCheck.

%package apidocs
Summary:	API documentation for KtoBLZCheck library
Summary(pl.UTF-8):	Dokumentacja API biblioteki KtoBLZCheck
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for KtoBLZCheck library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki KtoBLZCheck.

%package -n python-ktoblzcheck
Summary:	Python 2 binding for KtoBLZCheck library
Summary(pl.UTF-8):	Wiązanie Pythona 2 dla biblioteki KtoBLZCheck
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules >= 1:2.6

%description -n python-ktoblzcheck
Python binding for KtoBLZCheck library.

%description -n python-ktoblzcheck -l pl.UTF-8
Wiązanie Pythona dla biblioteki KtoBLZCheck.

%package -n python3-ktoblzcheck
Summary:	Python 3 binding for KtoBLZCheck library
Summary(pl.UTF-8):	Wiązanie Pythona 3 dla biblioteki KtoBLZCheck
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-modules >= 1:3.2

%description -n python3-ktoblzcheck
Python binding for KtoBLZCheck library.

%description -n python3-ktoblzcheck -l pl.UTF-8
Wiązanie Pythona dla biblioteki KtoBLZCheck.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# drop pythondir, wrongly joined
%{__sed} -i -e '/^pythondir=/d' ktoblzcheck.pc.in

%build
%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_STATIC=ON \
	-DENABLE_BANKDATA_DOWNLOAD=OFF

%{__make}
cd ..
%endif

install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_BINDIR=bin \
	-DCMAKE_INSTALL_DATADIR=share \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DENABLE_BANKDATA_DOWNLOAD=OFF

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT

# use the one from shared build
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/ktoblzcheck.pc
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

%if %{with python2}
# module supports CPython 2.6+, but cmake prefers python3, in such case python2 module must be installed manually
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}
cp -p src/python/ktoblzcheck.py $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md
%attr(755,root,root) %{_bindir}/ibanchk
%attr(755,root,root) %{_bindir}/ktoblzcheck
%attr(755,root,root) %{_libdir}/libktoblzcheck.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libktoblzcheck.so.1
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.txt
%{_mandir}/man1/ibanchk.1*
%{_mandir}/man1/ktoblzcheck.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libktoblzcheck.so
%{_includedir}/iban.h
%{_includedir}/ktoblzcheck.h
%{_libdir}/cmake/KtoBlzCheck
%{_pkgconfigdir}/ktoblzcheck.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libktoblzcheck.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/ktoblzcheck

%if %{with python2}
%files -n python-ktoblzcheck
%defattr(644,root,root,755)
%{py_sitescriptdir}/ktoblzcheck.py[co]
%endif

%files -n python3-ktoblzcheck
%defattr(644,root,root,755)
%{py3_sitescriptdir}/ktoblzcheck.py
%{py3_sitescriptdir}/__pycache__/ktoblzcheck.cpython-*.py[co]
