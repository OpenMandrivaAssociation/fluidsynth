%define major                   1
%define libname                 %mklibname %{name} %{major}
%define libnamedev              %mklibname %{name} -d

Name:           fluidsynth
Version:        1.1.2
Release:        %mkrel 1
Summary:        Realtime, SoundFont-based synthesizer
License:        GPL
Group:          Sound
URL:            http://www.fluidsynth.org/
Source0:        http://sourceforge.net/projects/fluidsynth/files/fluidsynth-1.1.2/fluidsynth-1.1.2.tar.bz2
BuildRequires:  chrpath
BuildRequires:  ladspa-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  jackit-devel
BuildRequires:  libalsa-devel
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  pulseaudio-devel
BuildRequires:  libreadline-devel
Obsoletes:	iiwusynth < %{version}-%{release}
Obsoletes:	%{name}-static-devel
Provides:	iiwusynth = %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
FluidSynth is a real-time software synthesizer based on the SoundFont 2
specifications. It is a "software synthesizer". FluidSynth can read MIDI
events from the MIDI input device and render them to the audio device. It
can also play MIDI files.

%package -n %{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %{name}.

%package -n %{libnamedev}
Summary:         Header files and libraries from %{name}
Group:           Development/C
Requires:        %{libname} = %{version}-%{release}
Provides:        lib%{name}-devel = %{version}-%{release}
Provides:        %{name}-devel = %{version}-%{release} 
Obsoletes:       %{name}-devel < %{version}-%{release}
Obsoletes:	 %mklibname -d %name 1

%description -n %{libnamedev}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q

%build
# use new cmake build environment
mkdir build
cd build
# enable floats has to be set for now, bug reported upstream
cmake .. -DCMAKE_INSTALL_PREFIX=%_prefix \
		 -Denable-ladspa=1 \
		 -Denable-lash=0 \
		 -Denable-floats=yes
%make
                                                                                
%install
rm -rf $RPM_BUILD_ROOT
cd build
%{makeinstall_std}
%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libfluidsynth.so.*.*.*

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu May 21 2009 Frederik Himpe <fhimpe@mandriva.org> 1.0.9-1mdv2010.0
+ Revision: 378433
- Build with Pulseaudio support
- Add BuildRequires: libreadline-devel
- update to new version 1.0.9

* Sun Aug 24 2008 Adam Williamson <awilliamson@mandriva.org> 1.0.8-3mdv2009.0
+ Revision: 275548
- obsoletes / provides iiwusynth (the old name of this project)

* Sun Jul 13 2008 Funda Wang <fundawang@mandriva.org> 1.0.8-2mdv2009.0
+ Revision: 234217
- obsolete old name

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Dec 28 2007 Austin Acton <austin@mandriva.org> 1.0.8-1mdv2008.1
+ Revision: 138724
- new version

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Jul 31 2007 David Walluck <walluck@mandriva.org> 1.0.7a-1mdv2008.0
+ Revision: 56870
- 1.0.7a
- Import fluidsynth



* Mon Feb 20 2006 Austin Acton <austin@mandriva.org> 1.0.7-1mdk
- New release 1.0.7
- build with lash support on > 2006

* Sun Jun 12 2005 Austin Acton <austin@mandriva.org> 1.0.6-1mdk
- 1.0.6
- source URL

* Sun Feb 6 2005 Austin Acton <austin@mandrake.org> 1.0.5-2mdk
- rebuild for readline

* Fri Aug 20 2004 Austin Acton <austin@mandrake.org> 1.0.5-1mdk
- 1.0.5
- configure 2.5

* Thu Nov 6 2003 Austin Acton <aacton@yorku.ca> 1.0.3-2mdk
- rebuild without ladcca until it works

* Thu Aug 28 2003 Austin Acton <aacton@yorku.ca> 1.0.3-1mdk
- 1.0.3

* Tue Jul 15 2003 Austin Acton <aacton@yorku.ca> 1.0.2-3mdk
- DIRM

* Mon Jul 14 2003 Austin Acton <aacton@yorku.ca> 1.0.2-2mdk
- rebuild for rpm

* Mon Jun 23 2003 Austin Acton <aacton@yorku.ca> 1.0.2-1mdk
- 1.0.2

* Thu May 22 2003 Austin Acton <aacton@yorku.ca> 1.0.1-2mdk
- add .so symbolic link

* Wed May 21 2003 Austin Acton <aacton@yorku.ca> 1.0.1-1mdk
- initial package
