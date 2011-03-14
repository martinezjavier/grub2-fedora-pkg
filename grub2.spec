# Modules always contain just 32-bit code
%define _libdir %{_exec_prefix}/lib

# 64bit intel machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif
#sparc is always compile 64 bit
%ifarch %{sparc}
%define _target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif

%if ! 0%{?efi}
%global efi %{ix86} x86_64 ia64
%endif

Name:           grub2
Epoch:          1
Version:        1.99
%define filever 1.99~rc1
Release:        0.1%{?dist}
Summary:        Bootloader with support for Linux, Multiboot and more

Group:          System Environment/Base
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Source0:        ftp://alpha.gnu.org/gnu/grub/grub-%{filever}.tar.gz
Source1:        90_persistent
Source2:        grub.default
Source3:        README.Fedora
Patch0:		grub-1.99-handle-fwrite-return.patch
Patch1:		grub-1.99-unused-variable.patch
Patch2:		grub-1.99-grub_test_assert_printf.patch
Patch3:		grub-1.99-just-say-linux.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  flex bison binutils python
BuildRequires:  ncurses-devel xz-devel
BuildRequires:  freetype-devel libusb-devel
%ifarch %{sparc}
BuildRequires:  /usr/lib64/crt1.o glibc-static
%else
BuildRequires:  /usr/lib/crt1.o glibc-static
%endif
BuildRequires:  autoconf automake autogen device-mapper-devel
BuildRequires:	freetype-devel gettext-devel git

Requires:	gettext
Requires(pre):  dracut
Requires(post): dracut

# TODO: ppc
# ExclusiveArch:  %{ix86} x86_64 %{sparc}

%description
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.

%ifarch %{efi}
%package efi
Summary:	GRUB for EFI systems.
Group:		System Environment/Base

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for EFI systems.
%endif

%prep
%setup -T -c -n grub-%{version}
%ifarch %{efi}
%setup -D -q -T -a 0 -n grub-%{version}
cd grub-%{filever}
cp %{SOURCE3} .
git init
git config user.email "pjones@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches}
cd ..
mv grub-%{filever} grub-efi-%{filever}
%endif
%setup -D -q -T -a 0 -n grub-%{version}
cd grub-%{filever}
cp %{SOURCE3} .
git init
git config user.email "pjones@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches}


%build
%ifarch %{efi}
cd grub-efi-%{filever}
./autogen.sh
%configure						\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed		\
		-e 's/-fstack-protector//g'		\
		-e 's/--param=ssp-buffer-size=4//g'	\
		-e 's/-mregparm=3/-mregparm=4//g'	\
		-e 's/-fasynchronous-unwind-tables//g' )"\
	TARGET_LDFLAGS=-static				\
        --with-platform=efi				\
        --program-transform-name=s,grub,%{name}-efi,
make %{?_smp_mflags}
%ifarch %{ix86}
%define grubefiarch i386-efi
%else
%define grubefiarch %{_arch}-efi
%endif
./grub-mkimage -O %{grubefiarch} -o grub.efi -d grub-core part_gpt hfsplus fat \
	ext2 btrfs normal chain boot configfile linux appleldr minicmd \
	loadbios reboot halt search font gfxterm
cd ..
%endif

cd grub-%{filever}
./autogen.sh
# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
%ifarch %{sparc}
PLATFORM=ieee1275
%else
PLATFORM=pc
%endif
%configure						\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed		\
		-e 's/-fstack-protector//g'		\
		-e 's/--param=ssp-buffer-size=4//g'	\
		-e 's/-mregparm=3/-mregparm=4//g'	\
		-e 's/-fasynchronous-unwind-tables//g' )"\
	TARGET_LDFLAGS=-static				\
        --with-platform=$PLATFORM			\
        --program-transform-name=s,grub,%{name},

make %{?_smp_mflags}

%install
set -e
rm -fr $RPM_BUILD_ROOT

%ifarch %{efi}
cd grub-efi-%{filever}
make DESTDIR=$RPM_BUILD_ROOT install

# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}-efi
touch $RPM_BUILD_ROOT/boot/%{name}-efi/grub.cfg
ln -s ../boot/%{name}-efi/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-efi.cfg

# Install ELF files modules and images were created from into
# the shadow root, where debuginfo generator will grab them from
find $RPM_BUILD_ROOT -name '*.mod' -o -name '*.img' |
while read MODULE
do
        BASE=$(echo $MODULE |sed -r "s,.*/([^/]*)\.(mod|img),\1,")
        # Symbols from .img files are in .exec files, while .mod
        # modules store symbols in .elf. This is just because we
        # have both boot.img and boot.mod ...
        EXT=$(echo $MODULE |grep -q '.mod' && echo '.elf' || echo '.exec')
        TGT=$(echo $MODULE |sed "s,$RPM_BUILD_ROOT,.debugroot,")
#        install -m 755 -D $BASE$EXT $TGT
done
install -m 755 -d $RPM_BUILD_ROOT/boot/efi/EFI/redhat/
install -m 755 grub.efi $RPM_BUILD_ROOT/boot/efi/EFI/redhat/grub.efi
cd ..
%endif

cd grub-%{filever}
make DESTDIR=$RPM_BUILD_ROOT install

# Script that makes part of grub.cfg persist across updates
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/grub.d/

# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}
touch $RPM_BUILD_ROOT/boot/%{name}/grub.cfg
ln -s ../boot/%{name}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg

# Install ELF files modules and images were created from into
# the shadow root, where debuginfo generator will grab them from
find $RPM_BUILD_ROOT -name '*.mod' -o -name '*.img' |
while read MODULE
do
        BASE=$(echo $MODULE |sed -r "s,.*/([^/]*)\.(mod|img),\1,")
        # Symbols from .img files are in .exec files, while .mod
        # modules store symbols in .elf. This is just because we
        # have both boot.img and boot.mod ...
        EXT=$(echo $MODULE |grep -q '.mod' && echo '.elf' || echo '.exec')
        TGT=$(echo $MODULE |sed "s,$RPM_BUILD_ROOT,.debugroot,")
#        install -m 755 -D $BASE$EXT $TGT
done

mv $RPM_BUILD_ROOT%{_infodir}/grub.info $RPM_BUILD_ROOT%{_infodir}/grub2.info
rm $RPM_BUILD_ROOT%{_infodir}/dir

# Defaults
install -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/grub

%clean    
rm -rf $RPM_BUILD_ROOT

%post
exec >/dev/null 2>&1
# Create device.map or reuse one from GRUB Legacy
cp -u /boot/grub/device.map /boot/%{name}/device.map 2>/dev/null ||
        %{name}-mkdevicemap
# Determine the partition with /boot
BOOT_PARTITION=$(df -h /boot |(read; awk '{print $1; exit}'))
# Generate core.img, but don't let it be installed in boot sector
%{name}-install --grub-setup=/bin/true $BOOT_PARTITION
# Remove stale menu.lst entries
/sbin/grubby --remove-kernel=/boot/%{name}/core.img
# Add core.img as multiboot kernel to GRUB Legacy menu
/sbin/grubby --add-kernel=/boot/%{name}/core.img --title="GNU GRUB 2, (%{version})"
if [ "$1" = 1 ]; then
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/grub2.info.gz || :
fi


%preun
if [ "$1" = 0 ]; then
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/grub2.info.gz || :
fi
exec >/dev/null
/sbin/grubby --remove-kernel=/boot/%{name}/core.img
# XXX Ugly
rm -f /boot/%{name}/*.mod
rm -f /boot/%{name}/*.img
rm -f /boot/%{name}/*.lst
rm -f /boot/%{name}/device.map

%files
%defattr(-,root,root,-)
/etc/bash_completion.d/grub
%{_libdir}/%{name}
%{_libdir}/grub/
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-mkdevicemap
%{_sbindir}/%{name}-mknetdir
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-setup
%{_bindir}/%{name}-bin2h
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
# %{_bindir}/%{name}-mkelfimage
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mkimage
# %{_bindir}/%{name}-mkisofs
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%ifnarch %{sparc}
%{_bindir}/%{name}-mkrescue
%endif
%ifarch %{sparc}
%{_sbindir}/%{name}-ofpathname
%endif
%{_bindir}/%{name}-script-check
%dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%{_sysconfdir}/%{name}.cfg
%{_sysconfdir}/default/grub
%dir /boot/%{name}
# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
%config(noreplace) /boot/%{name}/grub.cfg
%doc grub-%{filever}/COPYING grub-%{filever}/INSTALL grub-%{filever}/NEWS
%doc grub-%{filever}/README grub-%{filever}/THANKS grub-%{filever}/TODO
%doc grub-%{filever}/ChangeLog grub-%{filever}/README.Fedora
%exclude %{_mandir}
%{_infodir}/grub2*

%ifarch %{efi}
%files efi
%defattr(-,root,root,-)
%attr(0755,root,root)/boot/efi/EFI/redhat
/etc/bash_completion.d/grub
%{_libdir}/grub2-efi
%{_libdir}/grub/
%{_sbindir}/grub2-efi-mkconfig
%{_sbindir}/grub2-efi-mkdevicemap
%{_sbindir}/grub2-efi-mknetdir
%{_sbindir}/grub2-efi-install
%{_sbindir}/grub2-efi-probe
%{_sbindir}/grub2-efi-reboot
%{_sbindir}/grub2-efi-set-default
#%{_sbindir}/grub2-efi-setup
%{_bindir}/grub2-efi-bin2h
%{_bindir}/grub2-efi-editenv
%{_bindir}/grub2-efi-fstest
%{_bindir}/grub2-efi-kbdcomp
%{_bindir}/grub2-efi-menulst2cfg
# %{_bindir}/grub2-efi-mkelfimage
%{_bindir}/grub2-efi-mkfont
%{_bindir}/grub2-efi-mklayout
%{_bindir}/grub2-efi-mkimage
# %{_bindir}/grub2-efi-mkisofs
%{_bindir}/grub2-efi-mkpasswd-pbkdf2
%{_bindir}/grub2-efi-mkrelpath
%ifnarch %{sparc}
%{_bindir}/grub2-efi-mkrescue
%endif
%ifarch %{sparc}
%{_sbindir}/grub2-efi-ofpathname
%endif
%{_bindir}/grub2-efi-script-check
%dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%{_sysconfdir}/grub2-efi.cfg
%{_sysconfdir}/default/grub
%dir /boot/grub2-efi
# Actually, this is replaced by update-grub from scriptlets,
# but it takes care of modified persistent part
%config(noreplace) /boot/grub2-efi/grub.cfg
%doc grub-%{filever}/COPYING grub-%{filever}/INSTALL grub-%{filever}/NEWS
%doc grub-%{filever}/README grub-%{filever}/THANKS grub-%{filever}/TODO
%doc grub-%{filever}/ChangeLog grub-%{filever}/README.Fedora
%exclude %{_mandir}
%{_infodir}/grub2*
%endif

%changelog
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.98-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 17 2010 Dennis Gilmore <dennis@ausil.us> - 1:1.98-3
- correctly generate a grub.cfg on kernel update

* Fri May 28 2010 Dennis Gilmore <dennis@ausil.us> - 1:1.98-2
- add patch so grub2-probe works with lvm to detect devices correctly

* Wed Apr 21 2010 Dennis Gilmore <dennis@ausil.us> - 1:1.98-1
- update to 1.98

* Fri Feb 12 2010 Dennis Gilmore <dennis@ausil.us> - 1:1.97.2-1
- update to 1.97.2

* Wed Jan 20 2010 Dennis Gilmore <dennis@ausil.us> - 1:1.97.1-5
- drop requires on mkinitrd

* Tue Dec 01 2009 Dennis Gilmore <dennis@ausil.us> - 1:1.97.1-4
- add patch so that grub2 finds fedora's initramfs

* Tue Nov 10 2009 Dennis Gilmore <dennis@ausil.us> - 1:1.97.1-3
- no mkrescue on sparc arches
- ofpathname on sparc arches
- Requires dracut, not sure if we should just drop mkinitrd for dracut

* Tue Nov 10 2009 Dennis Gilmore <dennis@ausil.us> - 1:1.97.1-2
- update filelists

* Tue Nov 10 2009 Dennis Gilmore <dennis@ausil.us> - 1:1.97.1-1
- update to 1.97.1 release
- introduce epoch for upgrades

* Tue Nov 10 2009 Dennis Gilmore <dennis@ausil.us> - 1.98-0.7.20090911svn
- fix BR

* Fri Sep 11 2009 Dennis Gilmore <dennis@ausil.us> - 1.98-0.6.20090911svn
- update to new svn snapshot
- add sparc support

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98-0.6.20080827svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 01 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.98-0.4.20080827svn
- Add missing BR

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.98-0.4.20080827svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 27 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.98-0.3.20080827svn
- Updated SVN snapshot
- Added huge fat warnings

* Fri Aug 08 2008 Lubomir Rintel <lkundrak@v3.sk> - 1.98-0.2.20080807svn
- Correct scriptlet dependencies, trigger on kernel-PAE (thanks to Till Maas)
- Fix build on x86_64 (thanks to Marek Mahut)

* Thu Aug 07 2008 Lubomir Rintel <lkundrak@v3.sk> 1.98-0.1.20080807svn
- Another snapshot
- And much more!

* Mon May 12 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.97-0.1.20080512cvs
- CVS snapshot
- buildid patch upstreamed

* Sat Apr 12 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.96-2
- Pull in 32 bit glibc
- Fix builds on 64 bit

* Sun Mar 16 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.96-1
- New upstream release
- More transformation fixes
- Generate -debuginfo from modules again. This time for real.
- grubby stub
- Make it possible to do configuration changes directly in grub.cfg
- grub.cfg symlink in /etc

* Thu Feb 14 2008 Lubomir Kundrak <lkundrak@redhat.com> 1.95.cvs20080214-3
- Update to latest trunk
- Manual pages
- Add pci.c to DISTLIST

* Mon Nov 26 2007 Lubomir Kundrak <lkundrak@redhat.com> 1.95.cvs20071119-2
- Fix program name transformation in utils
- Moved the modules to /lib
- Generate -debuginfo from modules again

* Sun Nov 18 2007 Lubomir Kundrak <lkundrak@redhat.com> 1.95.cvs20071119-1
- Synchronized with CVS, major specfile cleanup

* Mon Jan 30 2007 Lubomir Kundrak <lkundrak@skosi.org> 1.95-lkundrak1
- Removed redundant filelist entries

* Mon Jan 29 2007 Lubomir Kundrak <lkundrak@skosi.org> 1.95-lkundrak0
- Program name transformation
- Bump to 1.95
- grub-probefs -> grub-probe
- Add modules to -debuginfo

* Tue Sep 12 2006 Lubomir Kundrak <lkundrak@skosi.org> 1.94-lkundrak0
- built the package
