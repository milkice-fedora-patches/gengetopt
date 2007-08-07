Summary: Tool to write command line option parsing code for C programs
Name: gengetopt
Version: 2.21
Release: 2%{dist}
License: GPLv3+
Group: Development/Tools
URL: http://www.gnu.org/software/gengetopt/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

BuildRequires: help2man
BuildRequires: valgrind

%description
Gengetopt is a tool to generate C code to parse the command line arguments
argc and argv that are part of every C or C++ program. The generated code uses
the C library function getopt_long to perform the actual command line parsing.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

# To retain timestamps on files installed without any modification.
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_infodir}/dir

# Move /usr/share/doc/gengetopt/examples to RPM_BUILD_DIR.
# To be later listed against %doc.
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/examples .
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz \
    %{_infodir}/dir >/dev/null 2>&1 || :
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
* Tue Aug 07 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.21-2
- Removed 'BuildRequires: source-highlight' to prevent build failure.

* Sat Aug 04 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.21-1
- Version bump to 2.21. Closes Red Hat Bugzilla bug #250817.
- License changed to GPLv3 or later.
- Parallel build problems fixed by upstream.
- README.example added by upstream.

* Mon Jun 12 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.20-1
- Version bump to 2.20.

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
