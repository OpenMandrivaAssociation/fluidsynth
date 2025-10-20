%define	major	3
%define	libname	%mklibname %{name}
%define	oldlibname	%mklibname %{name} 3
%define	devname	%mklibname %{name} -d

### FIXME ###
# From 2.3.2 fluidsynth introduce some changes to pkgconfig and cmake mechanism and looks like that cause problems with tests.
# Nothing provides cmake(oboe), cmake(systemd), cmake(readline), cmake(jack) and few others.
# To workaround this, lets disable bogus cmake requires. Last good version was 2.3.1. #angry p.
%global	__cmake_requires %{nil}

Summary:	Realtime, SoundFont-based synthesizer
Name:	fluidsynth
Version:	2.5.0
Release:	1
License:	LGPLv2+
Group:	Sound
Url:	https://www.fluidsynth.org/
Source0:	https://github.com/FluidSynth/fluidsynth/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:	fluidsynth-2.4.7-fix-systemd-failing-with-spaces-in-filename.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	ninja
BuildRequires:gomp-devel
BuildRequires:	ladspa-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbus-1) >= 1.11.12
BuildRequires:	pkgconfig(glib-2.0) >= 2.6.5
BuildRequires:	pkgconfig(gthread-2.0) >= 2.6.5
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libinstpatch-1.0)
BuildRequires:	pkgconfig(libpipewire-0.3)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(sdl3)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(systemd)

%description
A real-time software synthesizer based on the SoundFont 2 specifications.
It is a "software synthesizer". It can read MIDI events from the MIDI input
device and render them to the audio device. It can also play MIDI files.

%files
%doc README.md TODO
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_unitdir}/%{name}.service

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Dynamic libraries from %{name}
Group:	System/Libraries
%rename	%{oldlibname}

%description -n %{libname}
Dynamic libraries from %{name}.

%files -n %{libname}
%{_libdir}/libfluidsynth.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and libraries from %{name}
Group:	Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and includes files for developing programs based on %{name}.

%files -n %{devname}
%{_includedir}/%{name}.h
%{_includedir}/%{name}/*.h
%{_libdir}/libfluidsynth.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

#-----------------------------------------------------------------------------

%prep
%autosetup -p1


%build
%cmake \
	-DLIB_SUFFIX='' \
	-Denable-portaudio=ON \
	-Denable-pipewire=ON \
	-Denable-sdl3=ON \
	-Denable-midishare=OFF \
	-Denable-oboe=OFF \
	-Denable-opensles=OFF \
	-DFLUID_DAEMON_ENV_FILE="%{_sysconfdir}/sysconfig/%{name}" \
	-G Ninja

%ninja_build


%install
%ninja_install -C build

# Fix bogus pkgconfig file...
#sed -i -e 's,//usr,,g;s,-L\${libdir} ,,g;s,^includedir=\${prefix}/include,includedir=\${prefix}/include/fluidsynth,' %%buildroot%%_libdir/pkgconfig/*.pc

mkdir -p %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
sed -e 's,^#SOUND_FONT,SOUND_FONT,' build/fluidsynth.conf >%{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Install systemd unit
install -c -m 644 build/fluidsynth.service %{buildroot}%{_unitdir}/
