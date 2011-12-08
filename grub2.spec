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
Release:        13%{?dist}
Summary:        Bootloader with support for Linux, Multiboot and more

Group:          System Environment/Base
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Obsoletes:	grub < 1:0.98
Source0:        ftp://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
Source1:        90_persistent
Source2:        grub.default
Source3:        README.Fedora
Patch0:		grub-1.99-handle-fwrite-return.patch
Patch1:		grub-1.99-grub_test_assert_printf.patch
Patch2:		grub-1.99-just-say-linux.patch
Patch3:		grub-1.99-Workaround-for-variable-set-but-not-used-issue.patch
Patch4:		grub2-handle-initramfs-on-xen.patch
Patch5:		grub2-1.99-handle-more-dmraid.patch
Patch6:		grub2-gfxpayload-efi.patch
# https://savannah.gnu.org/bugs/index.php?35018
Patch7:		grub-1.99-fix_grub-probe_call.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  flex bison binutils python
BuildRequires:  ncurses-devel xz-devel
BuildRequires:  freetype-devel libusb-devel
%ifarch %{sparc} x86_64
BuildRequires:  /usr/lib64/crt1.o glibc-static
%else
BuildRequires:  /usr/lib/crt1.o glibc-static
%endif
BuildRequires:  autoconf automake autogen device-mapper-devel
BuildRequires:	freetype-devel gettext-devel git
BuildRequires:	texinfo

Requires:	gettext os-prober which
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
cd grub-%{version}
cp %{SOURCE3} .
git init
git config user.email "pjones@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches}
cd ..
mv grub-%{version} grub-efi-%{version}
%endif
%setup -D -q -T -a 0 -n grub-%{version}
cd grub-%{version}
cp %{SOURCE3} .
git init
git config user.email "pjones@fedoraproject.org"
git config user.name "Fedora Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches}


%build
%ifarch %{efi}
cd grub-efi-%{version}
./autogen.sh
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-fstack-protector//g'			\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-fasynchronous-unwind-tables//g' )"	\
	TARGET_LDFLAGS=-static					\
        --with-platform=efi					\
        --program-transform-name=s,grub,%{name}-efi,		\
        --sbindir=/sbin
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

cd grub-%{version}
./autogen.sh
# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
%ifarch %{sparc} ppc ppc64
PLATFORM=ieee1275
%else
PLATFORM=pc
%endif
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-fstack-protector//g'			\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-m64//g'					\
		-e 's/-fasynchronous-unwind-tables//g' )"	\
	TARGET_LDFLAGS=-static					\
        --with-platform=$PLATFORM				\
        --program-transform-name=s,grub,%{name},		\
        --sbindir=/sbin

make %{?_smp_mflags}

sed -i -e 's,(grub),(%{name}),g' \
	-e 's,grub.info,%{name}.info,g' \
	-e 's,\* GRUB:,* GRUB2:,g' \
	-e 's,/boot/grub/,/boot/%{name}/,g' \
	-e 's,grub-,%{name}-,g' \
	docs/grub.info
sed -i -e 's,grub-dev,%{name}-dev,g' docs/grub-dev.info

%install
set -e
rm -fr $RPM_BUILD_ROOT

%ifarch %{efi}
cd grub-efi-%{version}
make DESTDIR=$RPM_BUILD_ROOT install
mv $RPM_BUILD_ROOT/etc/bash_completion.d/grub $RPM_BUILD_ROOT/etc/bash_completion.d/grub-efi

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

cd grub-%{version}
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
mv $RPM_BUILD_ROOT%{_infodir}/grub-dev.info $RPM_BUILD_ROOT%{_infodir}/grub2-dev.info
rm $RPM_BUILD_ROOT%{_infodir}/dir

# Defaults
install -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/default/grub
# TODO: rename locale files to grub2 and make sure gettext works correctly
rm $RPM_BUILD_ROOT/usr/share/locale/*/LC_MESSAGES/grub.mo

%clean    
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/grub2.info.gz || :
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/grub2-dev.info.gz || :
fi

%triggerun -- grub2 < 1:1.99-4
# grub2 < 1.99-4 removed a number of essential files in postun. To fix upgrades
# from the affected grub2 packages, we first back up the files in triggerun and
# later restore them in triggerpostun.
# https://bugzilla.redhat.com/show_bug.cgi?id=735259

# Back up the files before uninstalling old grub2
mkdir -p /boot/grub2.tmp &&
mv -f /boot/grub2/*.mod \
      /boot/grub2/*.img \
      /boot/grub2/*.lst \
      /boot/grub2/device.map \
      /boot/grub2.tmp/ || :

%triggerpostun -- grub2 < 1:1.99-4
# ... and restore the files.
test ! -f /boot/grub2/device.map &&
test -d /boot/grub2.tmp &&
mv -f /boot/grub2.tmp/*.mod \
      /boot/grub2.tmp/*.img \
      /boot/grub2.tmp/*.lst \
      /boot/grub2.tmp/device.map \
      /boot/grub2/ &&
rm -r /boot/grub2.tmp/ || :

%preun
if [ "$1" = 0 ]; then
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/grub2.info.gz || :
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/grub2-dev.info.gz || :
fi

%files
%defattr(-,root,root,-)
/etc/bash_completion.d/grub
%{_libdir}/%{name}
%{_libdir}/grub/
/sbin/%{name}-mkconfig
/sbin/%{name}-mkdevicemap
/sbin/%{name}-mknetdir
/sbin/%{name}-install
/sbin/%{name}-probe
/sbin/%{name}-reboot
/sbin/%{name}-set-default
%ifarch %{ix86} x86_64 %{sparc}
/sbin/%{name}-setup
%endif
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
/sbin/%{name}-ofpathname
%endif
%{_bindir}/%{name}-script-check
%dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/default/grub
%dir /boot/%{name}
%ghost %config(noreplace) /boot/%{name}/grub.cfg
%doc grub-%{version}/COPYING grub-%{version}/INSTALL grub-%{version}/NEWS
%doc grub-%{version}/README grub-%{version}/THANKS grub-%{version}/TODO
%doc grub-%{version}/ChangeLog grub-%{version}/README.Fedora
%exclude %{_mandir}
%{_infodir}/grub2*

%ifarch %{efi}
%files efi
%defattr(-,root,root,-)
%attr(0755,root,root)/boot/efi/EFI/redhat
/etc/bash_completion.d/grub-efi
%{_libdir}/grub2-efi
%{_libdir}/grub/
/sbin/grub2-efi-mkconfig
/sbin/grub2-efi-mkdevicemap
/sbin/grub2-efi-mknetdir
/sbin/grub2-efi-install
/sbin/grub2-efi-probe
/sbin/grub2-efi-reboot
/sbin/grub2-efi-set-default
#/sbin/grub2-efi-setup
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
%ifnarch %{sparc} ppc ppc64
%{_bindir}/grub2-efi-mkrescue
%endif
%ifarch %{sparc} ppc ppc64
/sbin/grub2-efi-ofpathname
%endif
%{_bindir}/grub2-efi-script-check
%dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%config(noreplace) %{_sysconfdir}/grub2-efi.cfg
%config(noreplace) %{_sysconfdir}/default/grub
%dir /boot/grub2-efi
%ghost %config(noreplace) /boot/grub2-efi/grub.cfg
%doc grub-%{version}/COPYING grub-%{version}/INSTALL grub-%{version}/NEWS
%doc grub-%{version}/README grub-%{version}/THANKS grub-%{version}/TODO
%doc grub-%{version}/ChangeLog grub-%{version}/README.Fedora
%exclude %{_mandir}
%{_infodir}/grub2*
%endif

%changelog
* Thu Dec 08 2011 Adam Williamson <awilliam@redhat.com> - 1.99-13
- fix hardwired call to grub-probe in 30_os-prober (rhbz#737203)

* Mon Nov 07 2011 Peter Jones <pjones@redhat.com> - 1.99-12
- Lots of .spec fixes from Mads Kiilerich:
  Remove comment about update-grub - it isn't run in any scriptlets
  patch info pages so they can be installed and removed correctly when renamed
  fix references to grub/grub2 renames in info pages (#743964)
  update README.Fedora (#734090)
  fix comments for the hack for upgrading from grub2 < 1.99-4
  fix sed syntax error preventing use of $RPM_OPT_FLAGS (#704820)
  make /etc/grub2*.cfg %config(noreplace)
  make grub.cfg %ghost - an empty file is of no use anyway
  create /etc/default/grub more like anaconda would create it (#678453)
  don't create rescue entries by default - grubby will not maintain them anyway
  set GRUB_SAVEDEFAULT=true so saved defaults works (rbhz#732058)
  grub2-efi should have its own bash completion
  don't set gfxpayload in efi mode - backport upstream r3402
- Handle dmraid better. Resolves: rhbz#742226

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.99-11
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Adam Williamson <awilliam@redhat.com> - 1.99-10
- /etc/default/grub is explicitly intended for user customization, so
  mark it as config(noreplace)

* Tue Oct 11 2011 Peter Jones <pjones@redhat.com> - 1.99-9
- grub has an epoch, so we need that expressed in the obsolete as well.
  Today isn't my day.

* Tue Oct 11 2011 Peter Jones <pjones@redhat.com> - 1.99-8
- Fix my bad obsoletes syntax.

* Thu Oct 06 2011 Peter Jones <pjones@redhat.com> - 1.99-7
- Obsolete grub
  Resolves: rhbz#743381

* Wed Sep 14 2011 Peter Jones <pjones@redhat.com> - 1.99-6
- Use mv not cp to try to avoid moving disk blocks around for -5 fix
  Related: rhbz#735259
- handle initramfs on xen better (patch from Marko Ristola)
  Resolves: rhbz#728775

* Sat Sep 03 2011 Kalev Lember <kalevlember@gmail.com> - 1.99-5
- Fix upgrades from grub2 < 1.99-4 (#735259)

* Fri Sep 02 2011 Peter Jones <pjones@redhat.com> - 1.99-4
- Don't do sysadminny things in %preun or %post ever. (#735259)
- Actually include the changelog in this build (sorry about -3)

* Thu Sep 01 2011 Peter Jones <pjones@redhat.com> - 1.99-2
- Require os-prober (#678456) (patch from Elad Alfassa)
- Require which (#734959) (patch from Elad Alfassa)

* Thu Sep 01 2011 Peter Jones <pjones@redhat.com> - 1.99-1
- Update to grub-1.99 final.
- Fix crt1.o require on x86-64 (fix from Mads Kiilerich)
- Various CFLAGS fixes (from Mads Kiilerich)
  - -fexceptions and -m64
- Temporarily ignore translations (from Mads Kiilerich)

* Thu Jul 21 2011 Peter Jones <pjones@redhat.com> - 1.99-0.3
- Use /sbin not /usr/sbin .

* Thu Jun 23 2011 Peter Lemenkov <lemenkov@gmail.com> - 1:1.99-0.2
- Fixes for ppc and ppc64

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
