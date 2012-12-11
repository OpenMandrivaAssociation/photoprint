%define		bordersversion 0.0.2

Name:		photoprint
Version:	0.3.9
Release:	%mkrel 1
Summary:	Prints photos in various layouts and with color management
License:	GPL
Group:		Publishing
Source0:	http://www.blackfiveservices.co.uk/photoprint_resources/%{name}-%{version}.tar.gz
Source1:	http://www.blackfiveservices.co.uk/photoprint_resources/photoprint-borders-%{bordersversion}.tar.gz
Source2:	http://www.blackfiveservices.co.uk/PhotoPrint/Downloads/ProfilingKit.tar.bz2
Patch0:		photoprint-0.3.8-fmtstr.diff
Patch1:		photoprint-0.3.9-gcc4.x.diff
Patch2:		photoprint-0.3.9-glib_bork.diff
Patch3:		photoprint-0.3.9-netpbm.diff
Url:		http://www.blackfiveservices.co.uk/PhotoPrint/About.shtml
BuildRequires:	lcms-devel
BuildRequires:	libtiff-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libnetpbm-devel
BuildRequires:	cups-devel
BuildRequires:	libgutenprint-devel
BuildRequires:	libgtk+2.0-devel
BuildRequires:	desktop-file-utils
BuildRequires:	autoconf automake libtool
BuildRoot:	%_tmppath/%name-%version

%description
Photo Print is a utility for printing images via Gutenprint (a
rebranding of Gimp-Print for the latest version).

It supports different printing layouts, as one picture per page,
several pictures (scaled to equal size) per page, a poster of one
picture put together of several sheets, or several pictures combined
to one round picture for a CD back.

Image frames (Templates in /usr/share/photoprint/borders/) and color
management (Profiling instructions in
/usr/share/photoprint/ProfilingKit/ProfilingKit.html) are also
supported.

Photo Print can be used as GUI tool and also as command line tool in
batch mode.

Works nicely as an image editor in GQ-View.

%prep
%setup -q
%setup -q -T -D -a 1 -n %{name}-%{version}
%setup -q -T -D -a 2 -n %{name}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
export GTK2_LIBS="`pkg-config --libs gtk+-2.0` -lX11"

%configure2_5x

# bork
perl -pi -e "s|hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=\"\"|g" libtool
perl -pi -e "s|-L/lib/../%{_lib} -L/usr/lib/../%{_lib}|-L/%{_lib} -L%{_libdir}|g" libtool

%make

%install
rm -rf %{buildroot}
%makeinstall

# install borders
install -d %buildroot%{_datadir}/photoprint/borders
cp -a photoprint-borders*/. %buildroot%{_datadir}/photoprint/borders
install -d %buildroot%{_datadir}/photoprint/ProfilingKit
cp -a ProfilingKit*/. %buildroot%{_datadir}/photoprint/ProfilingKit

%find_lang %{name} --with-gnome

# install man page
install -d %buildroot%{_mandir}/man1/
install -m 644 photoprint.1 %buildroot%{_mandir}/man1/


desktop-file-install \
    --vendor="" \
    --dir %{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/fotoprint.desktop

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -fr %buildroot

%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING NEWS TODO
%_bindir/*
%_iconsdir/hicolor/48x48/apps/fotoprint.png
%_mandir/man*/*
%_datadir/photoprint
%_datadir/applications/fotoprint.desktop


%changelog
* Sun Nov 20 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3.9-1mdv2012.0
+ Revision: 731945
- 0.3.9
- fix build
- rebuilt against libnetpbm.so.11

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Jun 15 2008 Frederik Himpe <fhimpe@mandriva.org> 0.3.8-1mdv2009.0
+ Revision: 219261
- update to new version 0.3.8

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 10 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.6-1mdv2008.1
+ Revision: 116943
- new version
  drop old menu
  spec cleanup

  + Thierry Vignaud <tv@mandriva.org>
    - use %%mkrel

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - Import photoprint



* Tue Feb 21 2006 Till Kamppeter <till@mandriva.com> 0.3.1-1mdk
- Updated to version 0.3.1 (Dedicated profile selector, path editor widget,
  image selector, new "Paths" dialog for selecting profile and border paths,
  batch mode fixed, various bug fixes).

* Tue Nov  1 2005 Till Kamppeter <till@mandriva.com> 0.3.0-1mdk
- Updated to version 0.3.0 (Color management improvements, bug fixes).

* Sat Aug 27 2005 Till Kamppeter <till@mandriva.com> 0.2.9-2mdk
- Improved package description.

* Sat Aug 27 2005 Till Kamppeter <till@mandriva.com> 0.2.9-1mdk
- Updated to version 0.2.8 (Changing of of modes for many/all photos,
  canceling of transfer between layouts possible).
- Added photoprint borders and profiling kit.

* Sat Aug 13 2005 Till Kamppeter <till@mandriva.com> 0.2.8-2mdk
- Rebuilt for new Gutenprint.

* Sat Aug 13 2005 Till Kamppeter <till@mandriva.com> 0.2.8-1mdk
- Updated to version 0.2.8 (Some bug fixes, optimized compilation works 
  now.).
- Activated optimized compilation again.
- New home page and download URLs.

* Tue Jul 25 2005 Till Kamppeter <till@mandriva.com> 0.2.7-1mdk
- Updated to version 0.2.7 (Many bug fixes and improvements).
- Do not do any compiler optimizations, they break the program.

* Sun Jul 17 2005 Till Kamppeter <till@mandriva.com> 0.2.6-1mdk
- initial release.
