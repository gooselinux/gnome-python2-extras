%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define glib_version 2.6.0
%define gtk_version 2.4.0
%define gnome_panel_version 2.2.0
%define gnome_python_version 2.10.0
%define gtkhtml2_version 2.3.1
%define gtkspell_version 2.0.7
%define libgda_version 3.99.9
%define libgdl_version 2.24.0

%define enable_gda 0
%define enable_gdl 0

### Abstract ###

Name: gnome-python2-extras
Version: 2.25.3
Release: 20%{?dist}
License: GPLv2+ and LGPLv2+
Group: Development/Languages
Summary: Additional PyGNOME Python extension modules
URL: http://www.pygtk.org/
Source0: ftp://ftp.gnome.org/pub/GNOME/sources/gnome-python-extras/2.25/gnome-python-extras-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Obsoletes: gnome-python2-gda <= 2.14.3-1
Obsoletes: gnome-python2-gda-devel <= 2.14.3-1

### Patches ###

# GNOME bug #584126
Patch1: gnome-python-extras-2.25.3-update-for-2.27.2.patch

### Dependencies ###

Requires: gnome-python2 >= %{gnome_python_version}

### Build Dependencies ###

BuildRequires: glib2 >= %{glib_version}
BuildRequires: gnome-panel-devel >= %{gnome_panel_version}
BuildRequires: gnome-python2-bonobo >= %{gnome_python_version}
BuildRequires: gnome-python2-devel >= %{gnome_python_version}
BuildRequires: gnome-python2-gnome >= %{gnome_python_version}
BuildRequires: gtk2 >= %{gtk_version}
BuildRequires: gtkhtml2-devel >= %{gtkhtml2_version}
BuildRequires: gtkspell-devel >= %{gtkspell_version}
BuildRequires: libbonoboui-devel
BuildRequires: pygtk2-devel
BuildRequires: python-devel

%if %{enable_gda}
BuildRequires: libgda-devel >= %{libgda_version}
%endif

%if %{enable_gdl}
BuildRequires: libgdl-devel >= %{libgdl_version}
%endif

%description
The gnome-python-extra package contains the source packages for additional 
Python bindings for GNOME. It should be used together with gnome-python.

%if %{enable_gda}
%package -n gnome-python2-gda
Summary: Python bindings for interacting with libgda
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libgda >= %{libgda_version}

%description -n gnome-python2-gda
This module contains a wrapper that allows the use of libgda via Python.

%package -n gnome-python2-gda-devel
Summary: Headers for developing programs that will use gnome-python2-gda
Group: Development/Libraries
Requires: gnome-python2-gda = %{version}-%{release}
Requires: pkgconfig
Requires: pygobject2-devel
Requires: libgda-devel >= %{libgda_version}

%description -n gnome-python2-gda-devel
This module contains files needed for developing applications using
gnome-python2-gda.
%endif

%if %{enable_gdl}
%package -n gnome-python2-gdl
Summary: Python bindings for the GNOME Development Library
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: libgdl >= %{libgdl_version}

%description -n gnome-python2-gdl
This module contains a wrapper that allows the use of the GNOME Development
Library (gdl) via Python.
%endif

%package -n gnome-python2-gtkhtml2
Summary: Python bindings for interacting with gtkhtml2
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gtkhtml2 >= %{gtkhtml2_version}
Obsoletes: pygnome-gtkhtml

%description -n gnome-python2-gtkhtml2
This module contains a wrapper that allows the use of gtkhtml2 via Python.

%package -n gnome-python2-gtkspell
Summary: Python bindings for interacting with gtkspell
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gtkspell >= %{gtkspell_version}

%description -n gnome-python2-gtkspell
This module contains a wrapper that allows the use of gtkspell via Python.

%package -n gnome-python2-libegg
Summary: Python bindings for recent files and tray icons
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: gnome-python2-bonobo >= %{gnome_python_version}
Requires: gnome-python2-gnome >= %{gnome_python_version}

%description -n gnome-python2-libegg
This module contains a wrapper that allows the use of recent files and tray
icons via Python.

%prep
%setup -q -n gnome-python-extras-%{version}
%patch1 -p1 -b .update-for-2.27.2

%build

%if %{enable_gda}
%define gda_flags --enable-gda
%else
%define gda_flags --disable-gda
%endif

%if %{enable_gdl}
%define gdl_flags --enable-gdl
%else
%define gdl_flags --disable-gdl
%endif

%configure --enable-docs %gda_flags %gdl_flags
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \;

rm -rf $RPM_BUILD_ROOT/%{python_sitearch}/gtk-2.0/gksu

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS
%{_libdir}/pkgconfig/gnome-python-extras-2.0.pc
%{_datadir}/pygtk

%if %{enable_gda}
%files -n gnome-python2-gda
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/gda.so

%files -n gnome-python2-gda-devel
%defattr(-,root,root,-)
%{_includedir}/pygda-4.0/
%{_libdir}/pkgconfig/pygda-4.0.pc
%endif

%if %{enable_gdl}
%files -n gnome-python2-gdl
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/gdl.so
%endif

%files -n gnome-python2-gtkhtml2
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/gtkhtml*
%defattr(644,root,root,755)
%doc examples/gtkhtml2/*

%files -n gnome-python2-gtkspell
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/gtkspell.so
%{_datadir}/gtk-doc/html/pygtkspell

%files -n gnome-python2-libegg
%defattr(-,root,root,-)
%{python_sitearch}/gtk-2.0/egg
%defattr(644,root,root,755)
%doc examples/egg/*

%changelog
* Thu Jul 15 2010 Christopher Aillon <caillon@redhat.com> - 2.25.3-20
- Drop the -gtkmozembed subpackage

* Mon May 24 2010 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-19
- Rebuild (yet again) again newer gecko

* Mon May 17 2010 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-18
- Rebuild against newer gecko

* Wed Apr 28 2010 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-17
- Rebuild against newer gecko

* Wed Feb 24 2010 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-16
- Rebuild against newer gecko

* Thu Jan 07 2010 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-15
- Disable gda and gdl subpackages for RHEL6 (RH bug #530587).

* Thu Jan 07 2010 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-14
- Add switches to disable gda and gdl subpackages.

* Thu Nov 05 2009 Jan Horak <jhorak@redhat.com> - 2.25.3-13
- Rebuild against newer gecko

* Tue Oct 27 2009 Jan Horak <jhorak@redhat.com> - 2.25.3-12
- Rebuild against newer gecko

* Fri Sep 11 2009 Jan Horak <jhorak@redhat.com> - 2.25.3-11
- Rebuild against newer gecko

* Thu Aug 06 2009 Jan Horak <jhorak@redhat.com> - 2.25.3-10
- Rebuild against newer gecko

* Tue Aug 04 2009 Jan Horak <jhorak@redhat.com> - 2.25.3-9
- Rebuild against newer gecko

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Jan Horak <jhorak@redhat.com> - 2.25.3-7
- Rebuild against newer gecko

* Fri Jul 17 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-6
- Rebuild against newer gecko.

* Sun Jul 12 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-5
- Add patch for GNOME bug #584126 (gdl API break).

* Wed Jun 17 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-4
- Improve summary (RH bug #506526).

* Mon Apr 27 2009 Christopher Aillon <caillon@redhat.com> - 2.25.3-3
- Rebuild against newer gecko

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Fri Jan 30 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.2-1
- Update to 2.25.2
- Bump libgda_version to 3.99.9

* Fri Jan 23 2009 Denis Leroy <denis@poolshark.org> - 2.25.1-1
- Fixed Source URL
- Switch to libgda 4.0 API

* Wed Jan 21 2009 Matthew Barnes <mbarnes@redhat.com> - 2.25.1-1
- Update to 2.25.1
- Remove the xulrunner patches (fixed upstream).
- Remove patch for GNOME bug #553911 (fixed upstream).

* Wed Dec  24 2008 Deji Akingunola <dakingun@gmail.com> - 2.19.1-28
- Fix the gecko-lib version

* Tue Dec  23 2008 Deji Akingunola <dakingun@gmail.com> - 2.19.1-27
- Another rebuild against new gecko

* Fri Dec  5 2008 Matthias Clasen  <mclasen@redhat.com> - 2.19.1-26
- Rebuild against new gecko

* Wed Dec  3 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.19.1-25
- Fudge the gecko versioning

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.19.1-24
- Rebuild for Python 2.6

* Mon Oct 27 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-23
- Give us --force-tag back.

* Mon Oct 27 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-22
- Fix build break with libgdl-2.24.0 (GNOME bug #553911).
- Bump libgdl_version to 2.24.0.

* Mon Oct 27 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-21
- Provide Python bindings for libgdl on ppc64 (RH bug #468693).

* Thu Oct 09 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-20
- Remove gtkspell-static patch.  Appears to not be needed anymore.

* Wed Oct 08 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-19
- Add build requirements to get this building again.

* Fri Oct 03 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-18
- Add Requires: gnome-python2-gnome.

* Fri Oct 03 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-17
* Rebuild against gecko-devel-unstable-1.9.0.2.

* Wed Jul 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.19.1-16
- fix license tag

* Mon Apr 07 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-15.fc9
- Make gnome-python2-mozembed require gnome-python2-extras (RH bug #441228).

* Sun Feb 17 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-14.fc9
- Rebuild with GCC 4.3

* Sat Jan 12 2008 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-13.fc9
- Rename anjuta-gdl dependency to libgdl.
- Build now requires gecko-devel-unstable instead of gecko-devel
  (for mozilla-gtkmozembed pkg-config module).
- Add patch to make pkg-config look for mozilla-gtkmozembed even
  though we're using xulrunner.

* Tue Nov 27 2007 Martin Stransky <stransky@redhat.com> - 2.19.1-12.fc9
- added wraper for gtk_moz_embed_set_path()

* Mon Nov 26 2007 Martin Stransky <stransky@redhat.com> - 2.19.1-11.fc9
- Rebuild against gecko-libs 1.9 (xulrunner)

* Fri Nov 09 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-10.fc9
- Rebuild against gecko-libs 1.8.1.9.

* Thu Oct 25 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-9.fc9
- Require gecko-libs instead of firefox (RH bug #352111).

* Wed Oct 24 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-8.fc9
- Rebuild against firefox 2.0.0.8.

* Fri Oct 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-7.fc8
- Use ifarch instead of ExcludeArch to skip building the gdl subpackage
  on ppc64.  ExcludeArch affects the whole spec.

* Fri Sep 28 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-6.fc8
- Add a gnome-python2-gdl subpackage (RH bug #303141).

* Wed Aug 22 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-5.fc8
- Mass rebuild

* Thu Aug 09 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-4.fc8
- Rebuild against firefox-2.0.0.6.

* Thu Jul 19 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-3.fc8
- Rebuild against firefox-2.0.0.5.

* Mon Jul 16 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-2.fc8
- New gda subpackage obsoletes the separate gnome-python2-gda package.

* Tue Jun 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.19.1-1.fc8
- Update to 2.19.1

* Fri Jun 01 2007 Matthew Barnes <mbarnes@redhat.com> - 2.14.3-3.fc8
- Rebuild against firefox-2.0.0.4.

* Wed Apr 11 2007 Matthew Barnes <mbarnes@redhat.com> - 2.14.3-2.fc7
- Rebuild against firefox-2.0.0.3.
- Require exactly 2.0.0.3 so we're notified of dependency breaks.

* Sun Feb 25 2007 Matthew Barnes <mbarnes@redhat.com> - 2.14.3-1.fc7
- Update to 2.14.3

* Mon Feb 05 2007 Matthew Barnes <mbarnes@redhat.com> - 2.14.2-9.fc7
- Rename spec file to gnome-python2-extras.spec (RH bug #225833).

* Sat Jan 20 2007 Matthew Barnes <mbarnes@redhat.com> - 2.14.2-8.fc7
- Add missing BuildRequires gnome-python2-devel (RH bug #223602).

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.14.2-7
- rebuild for python 2.5

* Mon Nov  6 2006 Jeremy Katz <katzj@redhat.com> - 2.14.2-6
- fix to follow python packaging guidelines better

* Mon Nov  6 2006 Jeremy Katz <katzj@redhat.com> - 2.14.2-5
- rebuild against new firefox

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.14.2-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 John (J5) Palmieri <johnp@redhat.com> - 2.14.2-3
- Remove the Requires on the parent package from gtkmozembed
  so we don't pull in gnome-python2 also.  At some point we
  should look at what requires gnome-python2 and only Require it
  for those sub packages and not the parent package.

* Fri Sep 22 2006 Matthew Barnes <mbarnes@redhat.com> - 2.14.2-2
- Rebuild

* Tue Aug 29 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-1
- Update to 2.14.2
- Drop upstreamed patch

* Mon Jul 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-6
- fix a typo in configure

* Mon Jul 31 2006 Jesse Keating <jkeating@redhat.com> - 2.14.1-5
- again

* Mon Jul 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-3
- Rebuild against firefox

* Thu Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Rebuild

* Thu Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-1
- Update to 2.14.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.0-2.1
- rebuild

* Sat Jun 24 2006 Jesse Keating <jkeating@redhat.com> 2.14.0-2
- Add missing BR pygtk2-devel

* Mon Mar 13 2006 Ray Strode <rstrode@redhat.de> 2.14.0-1
- Update to 2.14.0

* Tue Feb 28 2006 Karsten Hopp <karsten@redhat.de> 2.13.3-4
- Buildrequires: python-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 John (J5) Palmieri <johnp@redhat.com> - 2.13.3-3
- Upload correct tar ball and try again

* Mon Feb  6 2006 John (J5) Palmieri <johnp@redhat.com> - 2.13.3-2
- Bump and rebuild (force-tag fails for this module)

* Mon Feb  6 2006 John (J5) Palmieri <johnp@redhat.com> - 2.13.3-1
- Update to 2.13.3
- Move the gnome-python2-applet gnome-python2-gnomeprint 
  gnome-python2-gtksourceview gnome-python2-libwnck 
  gnome-python2-libgtop2 gnome-python2-nautilus-cd-burner 
  gnome-python2-metacity and gnome-python2-totem subpackages 
  to gnome-python2-desktop because gnome-python-extras was split upstream

* Mon Jan 23 2006 Ray Strode <rstrode@redhat.com> - 2.12.1-10
- rebuild

* Thu Jan 05 2006 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-9
- Last rebuild didn't get the new libgtop

* Tue Dec 20 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-8
- rebuild for new libgtop soname change

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 2.12.1-7.1
- rebuilt

* Fri Dec 02 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-7
- rebuild with new libnautilus-cd-burner

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-6
- Don't delete the mozembed docs

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-5
- Try this again

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-4
- Remove ifarch directives around mozembed since it is now built on
  ppc64. Bump release again and retag

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-3
- Use pyver directly and bump release because force-tag doesn't work

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-2
- Module won't tag - bump release and try again

* Wed Nov 09 2005 John (J5) Palmieri <johnp@redhat.com> - 2.12.1-1
- Update to 2.12.1

* Tue Sep 27 2005 David Malcolm <dmalcolm@redhat.com> - 2.12.0-4
- remove conditionality of requirement on gnome-media-devel

* Tue Sep 27 2005 David Malcolm <dmalcolm@redhat.com> - 2.12.0-3
- consolidate s390 conditional part of build requirement on gnome-media-devel

* Tue Sep 27 2005 David Malcolm <dmalcolm@redhat.com> - 2.12.0-2
- fix sources

* Tue Sep 27 2005 David Malcolm <dmalcolm@redhat.com> - 2.12.0-1
- bump from 2.11.4 to 2.12.0
- rename wnck_window_demands_attention to wnck_window_needs_attention, to track
  change made in libwnck C API in 2.11.4, #169383
- added build requirement on gnome-media-devel, since this is needed to build
  mediaprofiles.so

* Fri Aug 19 2005 Jonathan Blandford <jrb@redhat.com> - 2.11.4-9
- add requires for gtksourceview, #162403

* Fri Aug 19 2005 Jeremy Katz <katzj@redhat.com> - 2.11.4-8
- totem subpackage shouldn't require mozilla
- build again on s390{,x}, but don't do the -nautilus-cdburner subpackage

* Wed Aug 17 2005 David Zeuthen <davidz@redhat.com> - 2.11.4-6
- Rebuilt

* Thu Aug 11 2005 Jeremy Katz <katzj@redhat.com> - 2.11.4-5
- add -totem subpackage
- nuke mozembed docs on ppc64

* Tue Aug  9 2005 Jeremy Katz <katzj@redhat.com> - 2.11.4-2
- and fix the build

* Tue Aug  9 2005 Jeremy Katz <katzj@redhat.com> - 2.11.4-1
- bump version and rebuild against current stack

* Mon Jul 11 2005  <jrb@redhat.com> - 2.11.2-1
- bump version and fix nautilus-cd-burner for s390

* Mon Mar 28 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.0-2.1
- Retag and rebuild

* Mon Mar 28 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.0-2
- Add patch to fix build error with gtkspell module

* Mon Mar 28 2005 John (J5) Palmieri <johnp@redhat.com> - 2.10.0-1
- Update to upstream 2.10.0

* Mon Feb  7 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.3-1
- Initial build.

