Summary:	Tool to write command line option parsing code for C programs
Name:		gengetopt
Version:	2.22
Release:	1%{dist}
License:	GPLv3+
Group:		Development/Tools
URL:		http://www.gnu.org/software/gengetopt/
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz

Patch0:		%{name}-%{version}-gcc43.patch

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires(post):	/sbin/install-info
Requires(preun): /sbin/install-info

%ifarch %{ix86} x86_64 ppc ppc64
BuildRequires:	valgrind
%endif

%description
Gengetopt is a tool to generate C code to parse the command line arguments
argc and argv that are part of every C or C++ program. The generated code uses
the C library function getopt_long to perform the actual command line parsing.

%prep
%setup -q
%patch0 -p1

# Suppress rpmlint error.
iconv --from-code ISO8859-1 --to-code UTF-8 ./ChangeLog \
  --output ChangeLog.utf-8 && mv ChangeLog.utf-8 ./ChangeLog
iconv --from-code ISO8859-1 --to-code UTF-8 ./THANKS \
  --output THANKS.utf-8 && mv THANKS.utf-8 ./THANKS

%build
%configure

# Parallel make does not work.
make

%check
make check

%ifarch %{ix86} x86_64 ppc ppc64
pushd ./tests
  make check-valgrind
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT

make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Move /usr/share/doc/gengetopt/examples to RPM_BUILD_DIR.
# To be later listed against %doc.
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/examples .
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS
%doc ChangeLog
%doc COPYING
%doc LICENSE
%doc NEWS
%doc README
%doc THANKS
%doc TODO
%doc doc/index.html
%doc doc/%{name}.html
%doc examples
%{_bindir}/%{name}
%{_infodir}/%{name}.info.gz
%{_mandir}/man1/%{name}.1.gz

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/getopt.c
%{_datadir}/%{name}/getopt1.c
%{_datadir}/%{name}/gnugetopt.h

%changelog
* Fri Mar 07 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.22-1
- Version bump to 2.22. Closes Red Hat Bugzilla bug #428641.
- Fixed build failure with gcc-4.3.
- Trimmed the 'BuildRequires' list.
- Changed character encodings from ISO8859-1 to UTF-8.
- Disabled parallel make to prevent failure with -j2.
- Added 'make check-valgrind' for ix86, x86_64, ppc and ppc64 in check stanza.
- Fixed Texinfo scriptlets according to Fedora packaging guidelines.

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
