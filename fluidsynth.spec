%define major                   1
%define libname                 %mklibname %{name} %{major}
%define libnamedev              %mklibname %{name} -d
%define libnamestaticdev        %mklibname %{name} -d -s

Name:           fluidsynth
Version:        1.1.1
Release:        %mkrel 2
Summary:        Realtime, SoundFont-based synthesizer
License:        LGPLv2+
Group:          Sound
URL:            http://www.fluidsynth.org/
Source0:        http://savannah.nongnu.org/download/fluid/%{name}-%{version}.tar.gz
Source1:        http://savannah.nongnu.org/download/fluid/%{name}-%{version}.tar.gz.sig
BuildRequires:  chrpath
BuildRequires:  e2fsprogs-devel
BuildRequires:  jackit-devel
%if %{mdkversion} > 2006
BuildRequires:  lash-devel
%else
BuildRequires:  ladcca-devel
%endif
BuildRequires:  ladspa-devel
BuildRequires:  libalsa-devel
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  pulseaudio-devel
BuildRequires:  libreadline-devel
BuildRequires:  libsndfile-devel
Obsoletes:	iiwusynth < %{version}-%{release}
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

%package -n %{libnamestaticdev}
Summary:         Static libraries from %{name}
Group:           Development/C
Requires:        %{libnamedev} = %{version}-%{release}
Provides:        lib%{name}-static-devel = %{version}-%{release}
Provides:        %{name}-static-devel = %{version}-%{release} 
Obsoletes:       %{name}-static-devel < %{version}-%{release}

%description -n %{libnamestaticdev}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q

%build
%{configure2_5x} --enable-ladspa --enable-jack-support \
%if %{mdkversion} > 2006
--disable-ladcca --enable-lash
%else
--enable-ladcca --disable-lash
%endif
%make
                                                                                
%install
rm -rf $RPM_BUILD_ROOT
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
%{_libdir}/*.la
%{_libdir}/pkgconfig/%{name}.pc

%files -n %{libnamestaticdev}
%defattr(-,root,root)
%{_libdir}/*.a
