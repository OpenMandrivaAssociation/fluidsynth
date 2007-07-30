%define name	fluidsynth
%define version	1.0.7
%define release 1mdk

%define major	1
%define libname %mklibname %name %major

Name: 	 	%{name}
Summary: 	Realtime, SoundFont-based synthesizer
Version: 	%{version}
Release: 	%{release}

Source:		http://savannah.nongnu.org/download/fluid/%{name}-%{version}.tar.bz2
URL:		http://www.fluidsynth.org/
License:	GPL
Group:		Sound
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	jackit-devel ladspa-devel libalsa-devel ncurses-devel
BuildRequires:	pkgconfig e2fsprogs-devel
%if %mdkversion > 2006
BuildRequires:	lash-devel
%else
BuildRequires:	ladcca-devel
%endif

%description
FluidSynth is a real-time software synthesizer based on the SoundFont 2
specifications. It is a "software synthesizer". FluidSynth can read MIDI
events from the MIDI input device and render them to the audio device. It
can also play MIDI files.

%package -n 	%{libname}
Summary:        Dynamic libraries from %name
Group:          System/Libraries

%description -n %{libname}
Dynamic libraries from %name.

%package -n 	%{libname}-devel
Summary: 	Header files and static libraries from %name
Group: 		Development/C
Requires: 	%{libname} >= %{version}
Provides: 	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Obsoletes: 	%name-devel

%description -n %{libname}-devel
Libraries and includes files for developing programs based on %name.

%prep
%setup -q

%build
%configure2_5x --enable-ladspa --enable-jack-support \
%if %mdkversion > 2006
--disable-ladcca --enable-lash
%else
--enable-ladcca --disable-lash
%endif
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%{_bindir}/%name
%{_mandir}/man1/%name.1.*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/%name
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/%name.pc
