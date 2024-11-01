%define major	3
%define libname	%mklibname %{name}
%define oldlibname	%mklibname %{name} 3
%define devname	%mklibname %{name} -d

### FIXME ###
# From 2.3.2 fluidsynth introduce some changes to pkgconfix and cmake mechanism and looks like that cause problems with tests.
# nothing provides cmake(oboe), cmake(systemd), cmake(readline), cmake(jack) and few others.
# To workaround this, lets disable bogus cmake requires. Last good version was 2.3.1. #angry p.
%global	__cmake_requires %{nil}

Name:           fluidsynth
Version:	2.4.0
Release:	1
Summary:        Realtime, SoundFont-based synthesizer
License:        LGPLv2+
Group:          Sound
Url:            https://www.fluidsynth.org/
Source0:        https://github.com/FluidSynth/fluidsynth/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:	ninja
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
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libinstpatch-1.0)

%description
FluidSynth is a real-time software synthesizer based on the SoundFont 2
specifications. It is a "software synthesizer". FluidSynth can read MIDI
events from the MIDI input device and render them to the audio device. It
can also play MIDI files.

%package -n %{libname}
Summary:        Dynamic libraries from %{name}
Group:          System/Libraries
%rename %{oldlibname}

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
%cmake \
	-DLIB_SUFFIX='' \
	-Denable-portaudio=1 \
	-Denable-pipewire=ON \
	-Denable-lash=0 \
	-DFLUID_DAEMON_ENV_FILE=%{_sysconfdir}/sysconfig/fluidsynth \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libfluidsynth.so.*.*.*
# Fix bogus pkgconfig file...
#sed -i -e 's,//usr,,g;s,-L\${libdir} ,,g;s,^includedir=\${prefix}/include,includedir=\${prefix}/include/fluidsynth,' %buildroot%_libdir/pkgconfig/*.pc
mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -c -m 644 build/fluidsynth.service %{buildroot}%{_unitdir}/
sed -e 's,^#SOUND_FONT,SOUND_FONT,' build/fluidsynth.conf >%{buildroot}%{_sysconfdir}/sysconfig/fluidsynth

%files
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_unitdir}/fluidsynth.service
%config(noreplace) %{_sysconfdir}/sysconfig/fluidsynth

%files -n %{libname}
%{_libdir}/libfluidsynth.so.%{major}*

%files -n %{devname}
%{_includedir}/*.h
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/fluidsynth/
