%define major	3
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Name:           fluidsynth
Version:	2.2.2
Release:	1
Summary:        Realtime, SoundFont-based synthesizer
License:        LGPLv2+
Group:          Sound
Url:            http://www.fluidsynth.org/
Source0:        https://github.com/FluidSynth/fluidsynth/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  chrpath
BuildRequires:	doxygen
BuildRequires:  ladspa-devel
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(dbus-1) >= 1.0.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.6.5
BuildRequires:  pkgconfig(gthread-2.0) >= 2.6.5
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(sndfile)

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

%package -n %{devname}
Summary:         Header files and libraries from %{name}
Group:           Development/C
Requires:        %{libname} = %{version}-%{release}
Provides:        %{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q

%build
%cmake \
	-DLIB_SUFFIX='' \
	-Denable-portaudio=1 \
	-Denable-lash=0
%make_build

%install
%makeinstall_std -C build
%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libfluidsynth.so.*.*.*
# Fix bogus pkgconfig file...
#sed -i -e 's,//usr,,g;s,-L\${libdir} ,,g;s,^includedir=\${prefix}/include,includedir=\${prefix}/include/fluidsynth,' %buildroot%_libdir/pkgconfig/*.pc

%files
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%{_libdir}/libfluidsynth.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
