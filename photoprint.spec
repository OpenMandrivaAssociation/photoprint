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
BuildRequires:	libcups-devel
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
