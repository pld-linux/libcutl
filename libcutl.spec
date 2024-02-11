#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	C++ utility library
Summary(pl.UTF-8):	Biblioteka narzędziowa C++
Name:		libcutl
Version:	1.10.0
Release:	1
License:	MIT (with Boost fragments)
Group:		Libraries
Source0:	https://www.codesynthesis.com/download/libcutl/1.10/%{name}-%{version}.tar.bz2
# Source0-md5:	462930494a5e7094ea14b00f3767f6af
Patch0:		%{name}-boost.patch
URL:		https://www.codesynthesis.com/projects/libcutl/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.54.0
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libcutl is a C++ utility library. It contains a collection of generic
and fairly independent components.

%description -l pl.UTF-8
libcutl to biblioteka narzędziowa C++. Zawiera zbiór ogólnych i w
miarę niezależnych komponentów.

%package devel
Summary:	Header files for cutl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki cutl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel >= 1.54.0
Requires:	libstdc++-devel

%description devel
Header files for cutl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki cutl.

%package static
Summary:	Static cutl library
Summary(pl.UTF-8):	Statyczna biblioteka cutl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static cutl library.

%description static -l pl.UTF-8
Statyczna biblioteka cutl.

%prep
%setup -q
%patch0 -p1

# boost (as of 1.82) includes C++ <version> header; take out version file from include path
%{__mv} version version.txt

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-external-boost \
	--with-external-expat
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcutl.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libcutl

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS README
%attr(755,root,root) %{_libdir}/libcutl-1.10.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcutl.so
%{_includedir}/cutl
%{_pkgconfigdir}/libcutl.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcutl.a
%endif
