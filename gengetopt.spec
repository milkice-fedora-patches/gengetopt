Name:             gengetopt
Version:          2.22.6
Release:          1%{dist}
Summary:          Tool to write command line option parsing code for C programs
License:          GPLv3+
URL:              http://www.gnu.org/software/gengetopt/
Source0:          ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
%ifarch %{ix86} x86_64 ppc ppc64 %{arm}
BuildRequires:    valgrind
%endif
Requires(post):	  info
Requires(preun):  info
Provides:         bundled(gnulib)

%description
Gengetopt is a tool to generate C code to parse the command line arguments
argc and argv that are part of every C or C++ program. The generated code uses
the C library function getopt_long to perform the actual command line parsing.

%prep
%setup -q

# Suppress rpmlint error.
chmod 644 ./AUTHORS
chmod 644 ./ChangeLog
chmod 644 ./COPYING
chmod 644 ./LICENSE
chmod 644 ./NEWS
chmod 644 ./README
chmod 644 ./THANKS
chmod 644 ./TODO
chmod 644 ./doc/README.example
chmod 644 ./doc/index.html
chmod 644 ./src/parser.yy
chmod 644 ./src/scanner.ll
find . -name '*.c' -exec chmod 644 {} ';'
find . -name '*.cc' -exec chmod 644 {} ';'
find . -name '*.cpp' -exec chmod 644 {} ';'
find . -name '*.h' -exec chmod 644 {} ';'
find . -name '*.ggo' -exec chmod 644 {} ';'

%build
%configure
# Parallel build doesn't work.
make

%install
make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}
rm -rfv %{buildroot}%{_infodir}/dir
# Use %%doc macro to install instead.
rm -rfv %{buildroot}%{_docdir}/%{name}

mkdir ./examples
pushd ./doc
  cp -p README.example ../examples
  cp -p main1.cc sample1.ggo ../examples
  cp -p main2.c sample2.ggo ../examples
popd

%check
make check

%post
install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
  install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%doc AUTHORS ChangeLog COPYING LICENSE NEWS README THANKS TODO
%doc doc/index.html doc/%{name}.html
%doc examples/
%{_infodir}/%{name}.info*
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Thu Feb 20 2014 Christopher Meng <rpm@cicku.me> - 2.22.6-1
- Update to 2.22.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.22.5-1
- Update to 2.22.5-1 to fix FTBFS
- valgrind supported on ARM too

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-4
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 04 2009 Debarshi Ray <rishi@fedoraproject.org> - 2.22.3-1
- Version bump to 2.22.3. (Red Hat Bugzilla #512414)
  * enum option values can contain + and -.
  * Fixed compilation problems due to macro FIX_UNUSED which was not in the
    right place.
  * New command line switches --header-output-dir and --src_output-dir to
    store cmdline.h separately from cmdline.c.
  * Use #include <getopt.h> in the generated files, instead of "getopt.h".
  * Generated functions use prototypes with char ** instead of char *const *.
  * Removed compilation warnings for generated files.
  * Fixed a compilation problem for files generated with --include-getopt
    with some versions of stdlib.h.
  * Use PACKAGE_NAME, if defined, for printing help and version.
- Encoding of ChangeLog and THANKS fixed by upstream.
- Removed spurious executable permissions from a bunch of files.

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 2.22.1-3
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 2.22.1-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 02 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.22.1-1
- Version bump to 2.22.1. (Red Hat Bugzilla #444335)
  * Removed compilation warnings for generated files.
  * Fixed a bug with --long-help and enum options.
  * The outputs of --help and output of --show-help correspond with each other.
  * Fixed a compilation problem in generated output with mode options.
- Parallel build problems fixed by upstream.

* Fri Mar 07 2008 Debarshi Ray <rishi@fedoraproject.org> - 2.22-1
- Version bump to 2.22. (Red Hat Bugzilla #428641)
- Fixed build failure with gcc-4.3.
- Trimmed the 'BuildRequires' list.
- Changed character encodings from ISO8859-1 to UTF-8.
- Disabled parallel make to prevent failure with -j2.
- Added 'make check-valgrind' for ix86, x86_64, ppc and ppc64 in check stanza.
- Fixed Texinfo scriptlets according to Fedora packaging guidelines.

* Tue Aug 07 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.21-2
- Removed 'BuildRequires: source-highlight' to prevent build failure.

* Sat Aug 04 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.21-1
- Version bump to 2.21. (Red Hat Bugzilla #250817)
- License changed to GPLv3 or later.
- Parallel build problems fixed by upstream.
- README.example added by upstream.

* Tue Jun 12 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.20-1
- Version bump to 2.20.

* Tue Jun 12 2007 Debarshi Ray <rishi@fedoraproject.org> - 2.19.1-3
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
