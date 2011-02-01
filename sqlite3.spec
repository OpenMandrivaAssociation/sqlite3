%define realname sqlite
%define realver 3070500
%define rpmver %(echo %{realver}|sed -e "s/00//g" -e "s/0/./g")

%define	major 0
%define libname	%mklibname %{name}_ %{major}
%define develname	%mklibname %{name} -d
%define staticdevelname	%mklibname %{name} -d -s

Summary:	C library that implements an embeddable SQL database engine
Name:		sqlite3
Version:	%rpmver
Release:	%mkrel 1
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%{realname}-autoconf-%{realver}.tar.gz
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
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
Group:		System/Libraries

%description -n	%{libname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the shared libraries for %{name}

%package -n	%{develname}
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}_ %{major} -d

%description -n	%{develname}
SQLite is a C library that implements an embeddable SQL database
engine. Programs that link with the SQLite library can have SQL
database access without running a separate RDBMS process. The
distribution comes with a standalone command-line access program
(sqlite) that can be used to administer an SQLite database and
which serves as an example of how to use the SQLite library.

This package contains the static %{libname} library and its header
files.

%package -n	%{staticdevelname}
Summary:	Static development library for the %{name} library
Group:		Development/C
Requires:	%{develname} = %{version}-%{release}
Provides:	lib%{name}-static-devel = %{version}-%{release}
Provides:	%{name}-static-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}_ %{major} -d -s

%description -n	%{staticdevelname}
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

%prep
%setup -q -n %{realname}-autoconf-%{realver}

%build
%serverbuild

export CFLAGS="${CFLAGS:-%optflags} -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -Wall -DNDEBUG=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1"

%configure2_5x	--enable-threadsafe \
	--enable-dynamic-extensions
# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files -n %{staticdevelname}
%defattr(-,root,root)
%{_libdir}/lib*.a

%files tools
%defattr(-,root,root)
%{_bindir}/sqlite3
%{_mandir}/man1/*
