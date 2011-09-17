%define major                   1
%define libname                 %mklibname %{name} %{major}
%define libnamedev              %mklibname %{name} -d
%define oldlibnamestaticdev     %mklibname %{name} -d -s

Name:           fluidsynth
Version:        1.1.5
Release:        %mkrel 1
Summary:        Realtime, SoundFont-based synthesizer
License:        LGPLv2+
Group:          Sound
URL:            http://www.fluidsynth.org/
Source0:        http://sourceforge.net/projects/fluidsynth/files/%{name}-%{version}/%{name}-%{version}.tar.bz2
BuildRequires:  cmake
BuildRequires:  chrpath
BuildRequires:  ladspa-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  jackit-devel
BuildRequires:  libalsa-devel
BuildRequires:  ncurses-devel
BuildRequires:  pkgconfig
BuildRequires:  pulseaudio-devel
BuildRequires:  portaudio-devel
BuildRequires:  libreadline-devel
BuildRequires:  libsndfile-devel
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
Obsoletes:       %mklibname -d %name 1
Obsoletes:       %{oldlibnamestaticdev} < 1.1.3

%description -n %{libnamedev}
Libraries and includes files for developing programs based on %{name}.

%prep
%setup -q

%build

%cmake -DLIB_SUFFIX='' \
       -Denable-ladspa=1 \
       -Denable-lash=0
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build
%{_bindir}/chrpath -d %{buildroot}%{_libdir}/libfluidsynth.so.*.*.*

%clean
rm -rf %{buildroot}

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
