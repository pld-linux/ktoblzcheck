Summary:	A library to check account numbers and bank codes of German banks
Summary(pl.UTF-8):	Biblioteka do sprawdzania numerów kont i kodów bankowych niemieckich banków
Name:		ktoblzcheck
Version:	1.40
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/ktoblzcheck/%{name}-%{version}.tar.gz
# Source0-md5:	fe29ec3ef8b48adf0302fd9d2607580b
URL:		http://ktoblzcheck.sourceforge.net/
BuildRequires:	libstdc++-devel
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpm-pythonprov
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

%package -n python-ktoblzcheck
Summary:	Python binding for KtoBLZCheck library
Summary(pl.UTF-8):	Wiązanie Pythona dla biblioteki KtoBLZCheck
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
# for python-ctypes (>= 1:2.5 already forced by BR + _eq below)
%pyrequires_eq	python-modules

%description -n python-ktoblzcheck
Python binding for KtoBLZCheck library.

%description -n python-ktoblzcheck -l pl.UTF-8
Wiązanie Pythona dla biblioteki KtoBLZCheck.

%prep
%setup -q

%build
%configure \
	--enable-python \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/ktoblzcheck
%attr(755,root,root) %{_libdir}/libktoblzcheck.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libktoblzcheck.so.1
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.txt
%attr(755,root,root) %{_datadir}/%{name}/*.pl
%{_mandir}/man1/ktoblzcheck.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libktoblzcheck.so
%{_libdir}/libktoblzcheck.la
%{_includedir}/iban.h
%{_includedir}/ktoblzcheck.h
%{_pkgconfigdir}/ktoblzcheck.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libktoblzcheck.a

%files -n python-ktoblzcheck
%defattr(644,root,root,755)
%{py_sitescriptdir}/ktoblzcheck.py[co]
