Summary: Tool to write command line option parsing code for C programs
Name: gengetopt
Version: 2.19.1
Release: 3%{dist}
License: GPL
Group: Development/Tools
URL: http://www.gnu.org/software/gengetopt/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Patch0: %{name}-%{version}-from-debian.patch
Patch1: %{name}-%{version}-man.patch

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

BuildRequires: help2man
BuildRequires: source-highlight
BuildRequires: valgrind

%description
Gengetopt is a tool to generate C code to parse the command line arguments
argc and argv that are part of every C or C++ program. The generated code uses
the C library function getopt_long to perform the actual command line parsing.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure

# Disabling parallel make to prevent failure with -j2.
make

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir

# Move /usr/share/doc/gengetopt/examples to RPM_BUILD_DIR.
# To be later listed against %doc.
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/examples .
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

# README.example
mv ./doc/README.example ./examples

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING LICENSE NEWS README THANKS TODO doc/gengetopt.html doc/index.html examples
%{_bindir}/%{name}
%{_infodir}/%{name}.info.gz
%{_mandir}/man1/%{name}.1.gz

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/getopt.c
%{_datadir}/%{name}/getopt1.c
%{_datadir}/%{name}/gnugetopt.h

%changelog
* Mon Jun 12 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.19.1-3
- Added 'BuildRequires: ...' for check stanza.
- Added a check stanza.
- Removed -devel package.

* Mon Jun 11 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.19.1-2
- Used variables name and version in Source0.
- Mentioned /sbin/install-info as a requirement for post and preun.
- Used _datadir instead of defining sharedir.
- Disabled parallel make to prevent failure with -j2.
- Removing /usr/share/info/dir in the install stanza.
- Replaced '$RPM_BUILD_DIR' with '.' in the install stanza.

* Sun Jun 10 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.19.1-1
- Initial build.
- Added README.example from Debian.
- Changed version and date in online manual page to 2.19.1 from 2.19rc.
