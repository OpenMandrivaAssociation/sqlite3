%define realname sqlite

%define	major 0
%define libname	%mklibname %{name}_ %{major}
%define develname	%mklibname %{name} -d
%define staticdevelname	%mklibname %{name} -d -s

Summary:	C library that implements an embeddable SQL database engine
Name:		sqlite3
Version:	3.5.7
Release:	%mkrel 1
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%{realname}-%{version}.tar.gz
Patch0:     sqlite3-disable-tcl-build-doc.patch
BuildRequires:	chrpath
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl-devel tcl
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

%package -n	%{libname}
Summary:	C library that implements an embeddable SQL database engine
Group:          System/Libraries

%description -n	%{libname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the shared libraries for %{name}

%package -n	%develname
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel
Provides:	%{name}-devel
Obsoletes: %mklibname %{name}_ %{major} -d

%description -n	%develname
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library and its header
files.

%package -n	%staticdevelname
Summary:	Static development library for the %{name} library
Group:		Development/C
Requires:	%develname = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes: %mklibname %{name}_ %{major} -d -s

%description -n	%staticdevelname
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library.

%package	tools
Summary:	Command line tools for managing the %{libname} library
Group:		Databases
Requires:	%{libname} = %{version}-%{release}

%description	tools
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains command line tools for managing the
%{libname} library.

%package -n	tcl-%{name}
Summary:	Tcl binding for %{name}
Group:		Databases
Provides:	%{name}-tcl

%description -n	tcl-%{name}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains tcl binding for %{name}.

%prep

%setup -q -n %{realname}-%{version}
#%patch -p0 -b .tcl-b-doc

%build
#%define __libtoolize true

%serverbuild

export CFLAGS="${CFLAGS:-%optflags} -DNDEBUG=1"
export CXXFLAGS="${CXXFLAGS:-%optflags} -DNDEBUG=1"
export FFLAGS="${FFLAGS:-%optflags} -DNDEBUG=1"

%configure2_5x \
    --enable-utf8 \
    --enable-threadsafe \
    --enable-threads-override-locks

%make

make doc

%check
#make test

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_mandir}/man1

%makeinstall_std

install -m644 sqlite3.1 %{buildroot}%{_mandir}/man1/%name.1

chrpath -d %{buildroot}%{_bindir}/*

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README
%{_libdir}/lib*.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%doc doc/*.html 
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files -n %staticdevelname
%defattr(-,root,root)
%{_libdir}/lib*.a

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files -n tcl-%{name}
%defattr(-,root,root)
%{_prefix}/lib/tcl*/sqlite3
