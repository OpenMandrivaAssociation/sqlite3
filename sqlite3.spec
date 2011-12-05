%define realname sqlite
%define realver 3070900
%define rpmver %(echo %{realver}|sed -e "s/00//g" -e "s/0/./g")

%define	major 0
%define libname %mklibname %{name}_ %{major}
%define develname %mklibname %{name} -d

Summary:	C library that implements an embeddable SQL database engine
Name:		sqlite3
Version:	3.7.9
Release:	2
License:	Public Domain
Group:		System/Libraries
URL:		http://www.sqlite.org/
Source0:	http://www.sqlite.org/%{realname}-autoconf-%{realver}.tar.gz
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel

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
Requires:	%{libname} >= %{version}-%{release}
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

%package	tools
Summary:	Command line tools for managing the %{libname} library
Group:		Databases
Requires:	%{libname} >= %{version}-%{release}

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

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/lib*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files tools
%{_bindir}/sqlite3
%{_mandir}/man1/*
