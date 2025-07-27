%global appname PCSX2

%undefine __cmake_in_source_build

Name:           pcsx2
Version:        1.6.0
Release:        13%{?dist}
Summary:        Playstation 2 Emulator

License:        GPLv2 and GPLv3+ and LGPLv2+ and LGPLv3
URL:            https://pcsx2.net
Source0:        https://github.com/%{appname}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch1:         wx-config-3.2.patch
Patch2:         gcc12.patch
ExclusiveArch:  i686

BuildRequires:  cmake3
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  libaio-devel
BuildRequires:  ninja-build
BuildRequires:  perl
BuildRequires:  wxGTK-devel
BuildRequires:  xz-devel

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libpcap)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(soundtouch)
BuildRequires:  pkgconfig(zlib)

# https://bugzilla.rpmfusion.org/show_bug.cgi?id=6054
Requires:       alsa-plugins-pulseaudio
Requires:       alsa-plugins-pulseaudio%{?_isa}
Requires:       mesa-dri-drivers
Requires:       mesa-dri-drivers%{?_isa}

Recommends:     %{name}-langpacks = %{version}-%{release}

%description
PCSX2 is a free and open-source PlayStation 2 (PS2) emulator. Its purpose is to
emulate the PS2's hardware, using a combination of MIPS CPU Interpreters,
Recompilers and a Virtual Machine which manages hardware states and PS2 system
memory. This allows you to play PS2 games on your PC, with many additional
features and benefits.

The PCSX2 project has been running for more than ten years. Past versions could
only run a few public domain game demos, but newer versions can run many games
at full speed, including popular titles such as Final Fantasy X and Devil May
Cry 3. Visit the PCSX2 homepage to check the latest compatibility status of
games (with more than 2000 titles tested), or ask for help in the official
forums.


# Langpacks package
%package        langpacks
Summary:        Translations files for %{appname}
BuildArch:      noarch

Requires:       %{name} = %{version}-%{release}

%description    langpacks
Translations files for %{appname}.


%prep
%autosetup -p1

# Unbundle third-party
rm -r 3rdparty/


%build
%set_build_flags
%cmake3 -G Ninja                                \
    -DCMAKE_BUILD_PO=TRUE                       \
    -DCMAKE_BUILD_TYPE=Release                  \
    -DCMAKE_INSTALL_PREFIX=%{_prefix}           \
    -DDISABLE_ADVANCE_SIMD=TRUE                 \
    -DDISABLE_PCSX2_WRAPPER=TRUE                \
    -DDOC_DIR=%{_docdir}/%{name}                \
    -DGAMEINDEX_DIR=%{_datadir}/games/%{name}   \
    -DGTK3_API=TRUE                             \
    -DPACKAGE_MODE=TRUE                         \
    -DPLUGIN_DIR=%{_libdir}/games/%{name}       \
    -DXDG_STD=TRUE                              \
    -DEGL_API=TRUE                              \
    %dnl  # -DUSE_LTO=TRUE                      \  # We handle this via default Fedora build flags
    %{nil}

%cmake3_build


%install
%cmake3_install
%find_lang %{name}_Iconized
%find_lang %{name}_Main


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%license COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1 COPYING.LGPLv3
%doc README.md
%{_bindir}/%{appname}
%{_datadir}/applications/*.desktop
%{_datadir}/games/%{name}/
%{_datadir}/pixmaps/%{appname}.xpm
%{_docdir}/%{name}/*.pdf
%{_libdir}/games/%{name}/
%{_mandir}/man1/%{appname}.1*

%files -f %{name}_Iconized.lang -f %{name}_Main.lang langpacks

# FIXME: Directories without known owners:
%dir %{_datadir}/locale/ar_SA/
%dir %{_datadir}/locale/ar_SA/LC_MESSAGES


%changelog
* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 07 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.0-6
- build(add dep): alsa-plugins-pulseaudio, mesa-dri-drivers | #6054
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=6054

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 18 2020 Sérgio Basto <sergio@serjux.com> - 1.6.0-2
- Enable egl

* Thu May 07 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.0-1
- Update to 1.6

* Fri Mar 27 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.0-0.1rc
- Update to 1.6-rc

* Wed Feb 05 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.0-5.20200205git5308be3
- Update to latest git snapshot

* Sat Feb 01 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.0-1.20200201git69ae598
- Update to 1.5+

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Sat Jul 28 2018 Sérgio Basto <sergio@serjux.com> - 1.4-10
- Try fix rfbz #4962
- Use the same SDL that wxGTK depends on (F27 SDL, F28 SDL2)

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun May 20 2018 Sérgio Basto <sergio@serjux.com> - 1.4-8
- Try fix f27 (#4775) use compat-wxGTK3-gtk2-devel
- Add BR xz-devel to dectect LibLZMA
- Remove manually-specified variables were not used by the project
- Add DISABLE_ADVANCE_SIMD=TRUE, recomended by upstream
- OpenGL_GL_PREFERENCE=GLVND to not use legacy OpenGL

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Sérgio Basto <sergio@serjux.com> - 1.4-6
- Rebuilt to fix core dump with wxWindow

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 1.4-5
- Rebuild for soundtouch 2.0.0
- Just enable compat-wxGTK3-gtk2, pcsx2 fails to detect wxGTK3
  therefore SDL2 also is disabled, intructions on
  https://github.com/PCSX2/pcsx2/wiki/Installing-on-Linux
- Enable GLSL_API and AVX
- Fix Perl builroot changes.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 14 2016 Sérgio Basto <sergio@serjux.com> - 1.4-2
- Add gcc6 patch

* Thu Feb 11 2016 Giles Birchley <gbirchley@blueyonder.co.uk> -1.4-1
- Build for new release 1.4
- Drop patch pcsx2-1.3.1_fedora_cflags_opts.diff - cflag options now streamlined upstream
- Add dependency for lzma-devel
- Add dependency for libICE-devel
- Remove dependency for Cg
- Remove dependency for libjpeg-turbo-devel
- Remove dependency for package glew-devel
- Add build option to retain WxWidget 2.8 -DWX28_API=TRUE
- Add build option -DGTK3_API=FALSE
- Add build option -DSDL2_API=FALSE
- Add build option -DDISABLE_ADVANCE_SIMD=TRUE
- For now, avoided specifying crosscompile (-DCMAKE_TOOLCHAIN_FILE=cmake/linux-compiler-i386-multilib.cmake) as not sure of rpmfusion guideline on this
- Binary name has been altered to PCSX2 upstream; renamed PCSX2.desktop.in, PCSX2.xpm and PCSX2.1
- Added new launcher script PCSX2-linux.sh

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.1-1
- Updated source to 1.2.1
- Updated patch1 permissions
- Source required modification to remove copyrighted files - added Source1

* Tue Feb 04 2014 Giles Birchley <gbirchey@blueyonder.co.uk> -1.2.0-1
- Updated source to 1.2
- Updated patch1
- Source required modification to remove copyrighted files - added Source1

* Sat Jul 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-5
- made overlooked change suggested in rpmfusion review (#2455)
- changed requires from libGL-devel/libGLU-devel instead of mesa-libGL-devel

* Sun Jun 30 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-4
- made some minor changes suggested in rpmfusion review (#2455)
- removed backslash in cmake command
- removed pcsx2-1.1.0-fedora_cflags.diff
- replaced patch with pcsx2-1.1.0-fedora_cflags_opts.diff

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-3
- made some minor changes suggested in rpmfusion review (#2455)
- fix URL

* Tue Jun 25 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-2
- made some minor changes suggested in rpmfusion review (#2455):
- changed icon install permissions
- changed URL
- changed description line length
- reintroduced %%{version} macro to source0
- removed extra backslash from %%cmake
- changed line indentations so all are single space
- removed -DDOC_DIR from %%cmake
- removed extraneous remove lines

* Sun Jun 09 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.1.0-1
- changes following rpmfusion review (#2455).
- removed Group tag.
- updated source to v1.1 (linux fixes) 
- removed pcsx2-1.0.0_helpfile.diff (no longer needed).
- removed pcsx2-1.0.0_fedora_cmake.diff (Fedora<16 is no longer supported).
- removed pcsx2-1.1.0_fedora_gcc.diff as this patch is now applied in 1.1.0 source
- added Requires: hicolor-icon-theme (icons in %%{_datadir}/icons/hicolor/).
- added BuildRequires: libaio-devel (needed for 1.1.0).
- added warning about SSE2 to %%description.
- comment about 64 bit status shortened.
- version from names of docs removed (unversioned in 1.1.0).
- fixed omissions in pcsx2.xpm shebang (fix rpmlint error)
- Use %%{_docdir} instead of %%{_defaultdocdir}.
- removed some docs that were either misplaced or should not be packaged.
- removed specification of CMAKE_INSTALL_PREFIX and CMAKE_VERBOSE_MAKEFILE (%%cmake macro already sets them).
- moved %%find_lang macro to end of %%install.
- moved shell invocation to line following %%post %%postun (fix rpmlint error)

* Mon May 27 2013 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-2
- further changes to comply with rpmfusion review (#2455):
- libGL-devel/libGLU-devel instead of mesa-libGL-devel
- Remove BuildRequires: libCg (redundant with Cg)
- Use %%{_prefix} instead of /usr for CMAKE install prefix
- add Gregory Hainaut's patch to fix issue with gcc 4.8, for Fedora 19 build
- Changed cmake option of DBUILD_REPLAY_LOADERS to false and changed %%files accrdingly

* Tue Mar 05 2013 Giles Birchley <gbirchey@blueyonder.co.uk>
- bleeding edge build, altered package name
- added pcsx2 as a conflict

* Mon Oct 15 2012 Giles Birchley <gbirchey@blueyonder.co.uk> - 1.0.0-1
- Build of official 1.0.0 Release
- Significant modifications to script to comply with Fedora/RPMFusion packaging requirements
- Removed redundant BuildRequires
- Added upstream source
- Added Patch to make CFLAGS compliant
- Changed DCMAKE_BUILD_STRIP to FALSE to allow rpm debug package to be created
- Changed document destination in cmake by specifying DDOC_DIR=
- Changed language detection
- Changed icon and desktop file installation

* Tue Aug 09 2011 Danger Boy <Danger[dot] Boy [at]necac.tv.idl> - 0.9.8.4851-1
- initial build
