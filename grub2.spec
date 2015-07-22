%undefine _hardened_build

# Modules always contain just 32-bit code
%define _libdir %{_exec_prefix}/lib

# 64bit intel machines use 32bit boot loader
# (We cannot just redefine _target_cpu, as we'd get i386.rpm packages then)
%ifarch x86_64
%define _target_platform i386-%{_vendor}-%{_target_os}%{?_gnu}
%endif
# sparc is always compiled 64 bit
%ifarch %{sparc}
%define _target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif

%if ! 0%{?efi}

%global efi_only aarch64
%global efiarchs %{ix86} x86_64 ia64 %{efi_only}

%ifarch %{ix86}
%global grubefiarch i386-efi
%global grubefiname grubia32.efi
%global grubeficdname gcdia32.efi
%endif
%ifarch x86_64
%global grubefiarch %{_arch}-efi
%global grubefiname grubx64.efi
%global grubeficdname gcdx64.efi
%endif
%ifarch aarch64
%global grubefiarch arm64-efi
%global grubefiname grubaa64.efi
%global grubeficdname gcdaa64.efi
%endif

# Figure out the right file path to use
%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed -e 's/^ID=//' -e 's/rhel/redhat/'))

%endif

%global tarversion 2.02~beta2
%undefine _missing_build_ids_terminate_build

Name:           grub2
Epoch:          1
Version:        2.02
Release:        0.17%{?dist}
Summary:        Bootloader with support for Linux, Multiboot and more

Group:          System Environment/Base
License:        GPLv3+
URL:            http://www.gnu.org/software/grub/
Obsoletes:	grub < 1:0.98
Source0:        ftp://alpha.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
#Source0:	ftp://ftp.gnu.org/gnu/grub/grub-%{tarversion}.tar.xz
Source4:	http://unifoundry.com/unifont-5.1.20080820.pcf.gz
Source5:	theme.tar.bz2
Source6:	gitignore

Patch0001: 0001-fix-EFI-detection-on-Windows.patch
Patch0002: 0002-grub-core-kern-arm-cache_armv6.S-Remove-.arch-direct.patch
Patch0003: 0003-INSTALL-Cross-compiling-the-GRUB-Fix-some-spelling-m.patch
Patch0004: 0004-NEWS-First-draft-of-2.02-entry.patch
Patch0005: 0005-NEWS-The-cmosclean-command-in-fact-dates-back-to-1.9.patch
Patch0006: 0006-remove-unused-error.h-from-kern-emu-misc.c.patch
Patch0007: 0007-Don-t-abort-on-unavailable-coreboot-tables-if-not-ru.patch
Patch0008: 0008-NEWS-Add-few-missing-entries.-Correct-existing-ones.patch
Patch0009: 0009-strip-.eh_frame-section-from-arm64-efi-kernel.patch
Patch0010: 0010-use-grub-boot-aa64.efi-for-boot-images-on-AArch64.patch
Patch0011: 0011-fix-32-bit-compilation-on-MinGW-w64.patch
Patch0012: 0012-Change-grub-mkrescue-to-use-bootaa64.efi-too.patch
Patch0013: 0013-arm64-set-correct-length-of-device-path-end-entry.patch
Patch0014: 0014-Makefile.util.def-grub-macbless-Change-mansection-to.patch
Patch0015: 0015-add-part_apple-to-EFI-rescue-image-to-fix-missing-pr.patch
Patch0016: 0016-freebsd-hostdisk.c-is-only-ever-compiled-on-FreeBSD.patch
Patch0017: 0017-Prefer-more-portable-test-1-constructs.patch
Patch0018: 0018-NEWS-Add-few-missing-entries.patch
Patch0019: 0019-grub-core-kern-efi-efi.c-Ensure-that-the-result-star.patch
Patch0020: 0020-util-grub-mount.c-Extend-GCC-warning-workaround-to-g.patch
Patch0021: 0021-reintroduce-BUILD_LDFLAGS-for-the-cross-compile-case.patch
Patch0022: 0022-grub-core-term-terminfo.c-Recognize-keys-F1-F12.patch
Patch0023: 0023-Fix-ChangeLog-date.patch
Patch0024: 0024-Use-_W64-to-detect-MinGW-W64-32-instead-of-_FILE_OFF.patch
Patch0025: 0025-add-BUILD_EXEEXT-support-to-fix-make-clean-on-Window.patch
Patch0026: 0026-fix-include-loop-on-MinGW-due-to-libintl.h-pulling-s.patch
Patch0027: 0027-grub-core-commands-macbless.c-Rename-FILE-and-DIR-to.patch
Patch0028: 0028-Makefile.util.def-Link-grub-ofpathname-with-zfs-libs.patch
Patch0029: 0029-Makefile.am-default_payload.elf-Add-modules.patch
Patch0030: 0030-fix-removal-of-cpu-machine-links-on-mingw-msys.patch
Patch0031: 0031-grub-core-normal-main.c-read_config_file-Buffer-conf.patch
Patch0032: 0032-util-grub-install.c-Fix-a-typo.patch
Patch0033: 0033-use-MODULE_FILES-for-genemuinit-instead-of-MOD_FILES.patch
Patch0034: 0034-Ignore-EPERM-when-modifying-kern.geom.debugflags.patch
Patch0035: 0035-change-stop-condition-to-avoid-infinite-loops.patch
Patch0036: 0036-increase-network-try-interval-gradually.patch
Patch0037: 0037-look-for-DejaVu-also-in-usr-share-fonts-truetype.patch
Patch0038: 0038-Show-detected-path-to-DejaVuSans-in-configure-summar.patch
Patch0039: 0039-add-GRUB_WINDOWS_EXTRA_DIST-to-allow-shipping-runtim.patch
Patch0040: 0040-util-grub-install.c-write_to_disk-Add-an-info-messag.patch
Patch0041: 0041-util-grub-install.c-List-available-targets.patch
Patch0042: 0042-Fix-several-translatable-strings.patch
Patch0043: 0043-do-not-set-default-prefix-in-grub-mkimage.patch
Patch0044: 0044-fix-Mingw-W64-32-cross-compile-failure-due-to-printf.patch
Patch0045: 0045-grub-core-term-serial.c-grub_serial_register-Fix-inv.patch
Patch0046: 0046-grub-install-support-for-partitioned-partx-loop-devi.patch
Patch0047: 0047-grub-core-term-at_keyboard.c-Tolerate-missing-keyboa.patch
Patch0048: 0048-.gitignore-add-missing-files-and-.exe-variants.patch
Patch0049: 0049-util-grub-mkfont.c-Downgrade-warnings-about-unhandle.patch
Patch0050: 0050-grub-core-disk-ahci.c-Do-not-enable-I-O-decoding-and.patch
Patch0051: 0051-grub-core-disk-ahci.c-Allocate-and-clean-space-for-a.patch
Patch0052: 0052-grub-core-disk-ahci.c-Add-safety-cleanups.patch
Patch0053: 0053-grub-core-disk-ahci.c-Properly-handle-transactions-w.patch
Patch0054: 0054-grub-core-disk-ahci.c-Increase-timeout.-Some-SSDs-ta.patch
Patch0055: 0055-util-grub-mkfont.c-Build-fix-for-argp.h-with-older-g.patch
Patch0056: 0056-util-grub-mkrescue.c-Build-fix-for-argp.h-with-older.patch
Patch0057: 0057-add-grub_env_set_net_property-function.patch
Patch0058: 0058-add-bootpath-parser-for-open-firmware.patch
Patch0059: 0059-grub-core-disk-ahci.c-Ignore-NPORTS-field-and-rely-o.patch
Patch0060: 0060-grub-core-kern-i386-coreboot-mmap.c-Filter-out-0xa00.patch
Patch0061: 0061-grub-core-loader-i386-multiboot_mbi.c-grub_multiboot.patch
Patch0062: 0062-grub-core-mmap-i386-uppermem.c-lower_hook-COREBOOT-I.patch
Patch0063: 0063-grub-core-kern-i386-pc-mmap.c-Fallback-to-EISA-memor.patch
Patch0064: 0064-include-grub-i386-openbsd_bootarg.h-Add-addr-and-fre.patch
Patch0065: 0065-ieee1275-check-for-IBM-pseries-emulated-machine.patch
Patch0066: 0066-grub-core-loader-arm64-linux.c-Remove-redundant-0x.patch
Patch0067: 0067-grub-core-lib-relocator.c-Fix-the-case-when-end-of-l.patch
Patch0068: 0068-Fix-grub-probe-0-option.patch
Patch0069: 0069-Fix-partmap-cryptodisk-and-abstraction-handling-in-g.patch
Patch0070: 0070-btrfs-fix-get_root-key-comparison-failures-due-to-en.patch
Patch0071: 0071-grub-core-osdep-linux-getroot.c-grub_util_part_to_di.patch
Patch0072: 0072-Replace-few-instances-of-memcmp-memcpy-in-the-code-t.patch
Patch0073: 0073-include-grub-libgcc.h-Remove-ctzsi2-and-ctzdi2.-They.patch
Patch0074: 0074-Add-missing-endif.patch
Patch0075: 0075-grub-core-lib-syslinux_parse.c-Fix-timeout-quoting.patch
Patch0076: 0076-Improve-LVM-logical_volumes-string-matching.patch
Patch0077: 0077-Tolerate-devices-with-no-filesystem-UUID-returned-by.patch
Patch0078: 0078-Allow-loading-old-kernels-by-placing-GDT-in-conventi.patch
Patch0079: 0079-grub-core-kern-misc.c-__bzero-Don-t-compile-in-GRUB_.patch
Patch0080: 0080-grub-core-commands-verify.c-grub_pubkey_open-Fix-mem.patch
Patch0081: 0081-grub-core-commands-verify.c-grub_pubkey_open-Trust-p.patch
Patch0082: 0082-util-grub-gen-asciih.c-add_glyph-Fix-uninitialised-v.patch
Patch0083: 0083-grub-core-commands-efi-lsefisystab.c-grub_cmd_lsefis.patch
Patch0084: 0084-grub-core-loader-i386-bsd.c-grub_netbsd_boot-Pass-po.patch
Patch0085: 0085-util-grub-install.c-Fix-handling-of-disk-module.patch
Patch0086: 0086-grub-core-commands-loadenv.c-check_blocklists-Fix-ov.patch
Patch0087: 0087-docs-grub-dev.texi-Finding-your-way-around-The-build.patch
Patch0088: 0088-Fix-an-infinite-loop-in-grub-mkconfig.patch
Patch0089: 0089-grub-core-fs-cbfs.c-Don-t-probe-disks-of-unknow-size.patch
Patch0090: 0090-Fix-Changelog.patch
Patch0091: 0091-grub-core-disk-i386-pc-biosdisk.c-grub_biosdisk_rw-A.patch
Patch0092: 0092-grub-core-kern-disk_common.c-Clump-disk-size-to-1EiB.patch
Patch0093: 0093-grub-core-term-at_keyboard.c-Retry-probing-keyboard-.patch
Patch0094: 0094-Fix-typo-gettext_print-instead-of-gettext_printf.patch
Patch0095: 0095-grub-core-kern-mips-arc-init.c-grub_machine_get_boot.patch
Patch0096: 0096-configure.ac-Remove-several-unnecessary-semicolons.patch
Patch0097: 0097-Support-grub-emu-on-x32-ILP32-but-with-x86-64-instru.patch
Patch0098: 0098-Fix-incorrect-address-reference-in-btrfs.patch
Patch0099: 0099-Fix-build-with-glibc-2.20.patch
Patch0100: 0100-Tidy-up-ChangeLog-formatting.patch
Patch0101: 0101-Initialized-initrd_ctx-so-we-don-t-free-a-random-poi.patch
Patch0102: 0102-grub-core-osdep-unix-config.c-Remove-extraneous-comm.patch
Patch0103: 0103-Fix-wrong-commit.patch
Patch0104: 0104-grub-core-gmodule.pl.in-Accept-newer-binutils-which-.patch
Patch0105: 0105-grub-core-commands-keylayouts.c-Ignore-unknown-keys.patch
Patch0106: 0106-grub-core-normal-main.c-Don-t-drop-to-rescue-console.patch
Patch0107: 0107-ACPIhalt-Add-more-ACPI-opcodes.patch
Patch0108: 0108-Revert-Use-Wl-no-relax-rather-than-mno-relax-for-uni.patch
Patch0109: 0109-cleanup-grub_cpu_to_XXX_compile_time-for-constants.patch
Patch0110: 0110-Add-a-new-none-platform-that-only-builds-utilities.patch
Patch0111: 0111-Fix-in-tree-platform-none.patch
Patch0112: 0112-Use-full-initializer-for-initrd_ctx-to-avoid-fatal-w.patch
Patch0113: 0113-icmp6-fix-no-respond-to-neighbor-solicit-message.patch
Patch0114: 0114-efi-check-path-non-null-before-grub_strrchr.patch
Patch0115: 0115-Fix-date-in-last-ChangeLog-entry.patch
Patch0116: 0116-grub-fs-tester-consistently-print-output-of-grub-ls-.patch
Patch0117: 0117-send-router-solicitation-for-ipv6-address-autoconf-v.patch
Patch0118: 0118-grub-mkstandalone-out-of-bound-access-to-tar-header-.patch
Patch0119: 0119-grub-install-common-avoid-out-of-bound-access-when-r.patch
Patch0120: 0120-grub-core-disk-luks.c-fix-use-after-free-and-memory-.patch
Patch0121: 0121-Use-ssize_t-for-grub_util_fd_read-result.patch
Patch0122: 0122-grub-core-disk-geli.c-fix-memory-leaks-in-error-path.patch
Patch0123: 0123-Fix-ChangeLog.patch
Patch0124: 0124-grub-core-disk-lzopio.c-fix-double-free-in-error-pat.patch
Patch0125: 0125-grub-core-lib-syslinux_parse.c-do-not-free-array.patch
Patch0126: 0126-grub-core-fs-zfs-zfsinfo.c-memory-leak-in-print_vdev.patch
Patch0127: 0127-grub-core-loader-i386-xen_fileXX.c-memory-leak-in-gr.patch
Patch0128: 0128-grub-shell-support-files-also-for-net-boot.patch
Patch0129: 0129-add-file-filters-tests.patch
Patch0130: 0130-fix-memory-corruption-in-pubkey-filter-over-network.patch
Patch0131: 0131-fix-double-free-in-grub_net_recv_tcp_packet.patch
Patch0132: 0132-Avoid-use-of-non-portable-echo-n-in-grub-mkconfig.patch
Patch0133: 0133-grub-core-fs-ext2.c-grub_ext2_read_block-Support-lar.patch
Patch0134: 0134-grub-core-kern-arm-misc.S-fix-unaligned-grub_uint64_.patch
Patch0135: 0135-Fix-serial-rtscts-option-processing.patch
Patch0136: 0136-Support-GELI-v6-and-v7.patch
Patch0137: 0137-Replace-explicit-sizeof-divisions-by-ARRAY_SIZE.patch
Patch0138: 0138-grub_script_lexer_yywrap-Update-len-synchronously-wi.patch
Patch0139: 0139-grub_fshelp_read_file-Don-t-attempt-to-read-past-the.patch
Patch0140: 0140-grub-core-fs-minix.c-grub_minix_read_file-Avoid-read.patch
Patch0141: 0141-grub_cmd_play-Avoid-division-by-zero.patch
Patch0142: 0142-grub-core-disk-AFSplitter.c-AF_merge-Check-that-mdle.patch
Patch0143: 0143-grub_ata_setaddress-Check-that-geometry-is-sane-when.patch
Patch0144: 0144-Reject-NILFS2-superblocks-with-over-1GiB-blocks.patch
Patch0145: 0145-grub_ufs_mount-Check-that-sblock.ino_per_group-is-no.patch
Patch0146: 0146-grub-core-fs-ext2.c-grub_ext2_mount-Additional-check.patch
Patch0147: 0147-grub-core-fs-minix.c-Additional-filesystem-sanity-ch.patch
Patch0148: 0148-grub-core-fs-hfs.c-grub_hfs_mount-Additional-filesys.patch
Patch0149: 0149-grub_dmraid_nv_detect-Do-not-divide-by-zero.patch
Patch0150: 0150-grub-core-disk-ieee1275-nand.c-grub_nand_open-Check-.patch
Patch0151: 0151-grub-core-disk-i386-pc-biosdisk.c-Check-disk-size-sa.patch
Patch0152: 0152-osdep-linux-blocklist.c-grub_install_get_blocklist-C.patch
Patch0153: 0153-grub-core-lib-pbkdf2.c-grub_crypto_pbkdf2-Check-that.patch
Patch0154: 0154-grub-core-fs-btrfs.c-Avoid-divisions-by-zero.patch
Patch0155: 0155-grub-core-fs-zfs.c-Avoid-divisions-by-zero.patch
Patch0156: 0156-term.h-Avoid-returining-0-sized-terminal-as-it-may-l.patch
Patch0157: 0157-grub-core-disk-diskfilter.c-Validate-volumes-to-avoi.patch
Patch0158: 0158-grub-core-video-readers-jpeg.c-Avoid-division-by-zer.patch
Patch0159: 0159-Avoid-division-by-zero-in-serial.patch
Patch0160: 0160-grub-core-term-gfxterm.c-Avoid-division-by-zero.patch
Patch0161: 0161-include-grub-misc.h-grub_div_roundup-Remove-as-it-s-.patch
Patch0162: 0162-grub-core-kern-i386-tsc.c-calibrate_tsc-Ensure-that.patch
Patch0163: 0163-grub-core-loader-i386-xnu.c-guessfsb-Avoid-division-.patch
Patch0164: 0164-rtc_get_time_ms.c-grub_rtc_get_time_ms-Avoid-divisio.patch
Patch0165: 0165-haiku-getroot.c-grub_util_find_partition_start_os-Av.patch
Patch0166: 0166-grub-core-kern-efi-mm.c-grub_efi_get_memory_map-Neve.patch
Patch0167: 0167-unix-cputime.c-Cache-sc_clk_tck-and-check-it-for-san.patch
Patch0168: 0168-grub_menu_init_page-Avoid-returning-0-geometry-to-av.patch
Patch0169: 0169-Remove-potential-division-by-0-in-gfxmenu.patch
Patch0170: 0170-Remove-direct-_llseek-code-and-require-long-filesyst.patch
Patch0171: 0171-accept-also-hdX-as-alias-to-native-Xen-disk-name.patch
Patch0172: 0172-Mention-platform-none-in-NEWS.patch
Patch0173: 0173-tests-file_filter-file-Really-add-missing-file.patch
Patch0174: 0174-Autogenerate-ChangeLog-from-git-changelog.patch
Patch0175: 0175-conf-Makefile.common-Remove-unused-LD-C-FLAGS_CPU.patch
Patch0176: 0176-util-grub-mkrescue.c-Always-include-part_msdos-and-p.patch
Patch0177: 0177-efidisk-Return-the-determined-root-disk-even-if-part.patch
Patch0178: 0178-Makefile.am-Fix-Changelog-cutoff-address.patch
Patch0179: 0179-Generate-empty-ChangeLog-if-no-.git-is-available.patch
Patch0180: 0180-Always-add-msoft-float-to-avoid-compiler-generating-.patch
Patch0181: 0181-uhci-Fix-null-pointer-dereference.patch
Patch0182: 0182-commands-acpi-Use-ALIGN_UP-rather-than-manual-expres.patch
Patch0183: 0183-commands-file-Change-the-confusing-loop-stop-conditi.patch
Patch0184: 0184-commands-fileXX-Fix-memory-leak.patch
Patch0185: 0185-gptsync-Add-missing-device_close.patch
Patch0186: 0186-commands-hdparm-Add-missing-grub_disk_close.patch
Patch0187: 0187-zfs-Fix-disk-matching-logic.patch
Patch0188: 0188-commands-legacycfg-Fix-resource-leaks.patch
Patch0189: 0189-commands-macbless-Remove-incorrect-grub_free.patch
Patch0190: 0190-commands-macbless-Fix-potential-overflow.patch
Patch0191: 0191-commands-macbless-Handle-device-opening-errors-corre.patch
Patch0192: 0192-commands-nativedisk-Add-missing-device_close.patch
Patch0193: 0193-commands-parttool-Add-missing-device-close.patch
Patch0194: 0194-commands-syslinux-Add-missing-free.patch
Patch0195: 0195-commands-tr-Simplify-and-fix-missing-parameter-test.patch
Patch0196: 0196-commands-verify-Fix-sha1-context-zeroing-out.patch
Patch0197: 0197-commands-wildcard-Add-missing-free.patch
Patch0198: 0198-disk-AFsplitter-check-argument-validity-before-doing.patch
Patch0199: 0199-disk-ahci-Fix-device_map_range-argument.patch
Patch0200: 0200-disk-cryptodisk-Add-missing-error-check.patch
Patch0201: 0201-disk-diskfilter-Add-missing-lv-presence-check.patch
Patch0202: 0202-disk-geli-Add-missing-seek-success-check.patch
Patch0203: 0203-disk-geli-Add-missing-free.patch
Patch0204: 0204-biosdisk-Add-missing-cast.patch
Patch0205: 0205-font-Add-missing-free.patch
Patch0206: 0206-fs-cbfs-Add-missing-free.patch
Patch0207: 0207-fs-cpio_common-Add-a-sanity-check-on-namesize.patch
Patch0208: 0208-fs-fat-Fix-codepath-to-properly-free-on-error.patch
Patch0209: 0209-fs-hfs-hfs_open-Check-that-mount-succeeded.patch
Patch0210: 0210-fs-hfs-Add-pointer-sanity-checks.patch
Patch0211: 0211-commands-fileXX-Fix-remaining-memory-leak.patch
Patch0212: 0212-grub_iso9660_read-Explicitly-check-read_node-return-.patch
Patch0213: 0213-fs-minix-Fix-sector-promotion-to-64-bit.patch
Patch0214: 0214-fs-ntfs-Add-missing-free.patch
Patch0215: 0215-fs-ntfs-Add-sizes-sanity-checks.patch
Patch0216: 0216-fs-reiserfs-Fix-sector-count-overflow.patch
Patch0217: 0217-fs-sfs-Fix-error-check-and-add-sanity-check.patch
Patch0218: 0218-configure.ac-Always-add-D_FILE_OFFSET_BITS-64.patch
Patch0219: 0219-fs-ufs-Add-missing-error-check.patch
Patch0220: 0220-gfxmenu-icon_manager-Fix-null-pointer-dereference.patch
Patch0221: 0221-gfxmenu-theme_loader-Add-missing-allos-error-check.patch
Patch0222: 0222-i386-pc-mmap-Fix-memset-size.patch
Patch0223: 0223-lib-syslinux_parse-Add-missing-alloc-check.patch
Patch0224: 0224-lib-syslinux_parse-Fix-memory-leak.patch
Patch0225: 0225-lib-syslinux_parse-Add-missing-error-check.patch
Patch0226: 0226-bsd-Add-missing-null-pointer-check.patch
Patch0227: 0227-multiboot-Simplify-to-avoid-confusing-assignment.patch
Patch0228: 0228-plan9-Add-missing-grub_device_close.patch
Patch0229: 0229-xnu-Add-missing-error-check.patch
Patch0230: 0230-normal-main-Fix-error-handling.patch
Patch0231: 0231-normal-misc-Close-device-on-all-pathes.patch
Patch0232: 0232-devmapper-getroot-Fix-memory-leak.patch
Patch0233: 0233-linux-blocklist-Fix-memory-leak.patch
Patch0234: 0234-linux-getroot-Fix-error-handling.patch
Patch0235: 0235-unix-password-Fix-file-descriptor-leak.patch
Patch0236: 0236-vbe-Fix-incorrect-register-usage.patch
Patch0237: 0237-util-getroot-Add-missing-grub_disk_close.patch
Patch0238: 0238-grub-install-common-Fix-sizeof-usage.patch
Patch0239: 0239-grub-install-Fix-memory-leak.patch
Patch0240: 0240-grub-macbless-Fix-resource-leak.patch
Patch0241: 0241-util-misc.c-Check-ftello-return-value.patch
Patch0242: 0242-linux-getroot-fix-descriptor-leak.patch
Patch0243: 0243-linux-ofpath-fix-various-memory-leaks.patch
Patch0244: 0244-util-setup-fix-memory-leak.patch
Patch0245: 0245-util-install-fix-memory-leak.patch
Patch0246: 0246-linux-getroot-fix-memory-leak.patch
Patch0247: 0247-util-grub-install-rearrange-code-to-avoid-memory-lea.patch
Patch0248: 0248-util-grub-mkstandalone-fix-memory-leak.patch
Patch0249: 0249-util-grub-mount-fix-descriptor-leak.patch
Patch0250: 0250-util-mkimage-fix-memory-leaks.patch
Patch0251: 0251-util-setup-fix-memory-leak.patch
Patch0252: 0252-commands-acpi-Use-ALIGN_UP-rather-than-manual-expres.patch
Patch0253: 0253-fs-cbfs-cpio-Remove-useless-check-if-mode-is-NULL.patch
Patch0254: 0254-fs-zfs-Fix-error-handling.patch
Patch0255: 0255-fs-zfscrypt-Add-missing-explicit-cast.patch
Patch0256: 0256-linux-hostdisk-Limit-strcpy-size-to-buffer-size.patch
Patch0257: 0257-linux-ofpath-Fix-error-handling.patch
Patch0258: 0258-Document-intentional-fallthroughs.patch
Patch0259: 0259-linux-hostdisk-use-strncpy-instead-of-strlcpy.patch
Patch0260: 0260-linux-ofpath-fix-descriptor-leak.patch
Patch0261: 0261-fs-zfs-zfs.c-fix-memory-leak.patch
Patch0262: 0262-commands-parttool-fix-memory-leak.patch
Patch0263: 0263-fs-zfs-zfscrypt.c-fix-memory-leaks.patch
Patch0264: 0264-fs-zfs-zfscrypt.c-fix-indentation.patch
Patch0265: 0265-fs-hfsplus-fix-memory-leak.patch
Patch0266: 0266-util-grub-probe-fix-memory-leaks.patch
Patch0267: 0267-loader-xnu-fix-memory-leak.patch
Patch0268: 0268-Change-quotes-to-match-overall-style-in-NEWS.patch
Patch0269: 0269-syslinux_parse-fix-memory-leak.patch
Patch0270: 0270-script-execute.c-fix-memory-leak.patch
Patch0271: 0271-configure.ac-don-t-use-msoft-float-for-arm64.patch
Patch0272: 0272-test-do-not-stop-after-first-file-test-or-closing-br.patch
Patch0273: 0273-test-fix-previous-commit-we-need-to-return-from-sube.patch
Patch0274: 0274-test-consistently-use-TMPDIR-and-same-name-pattern-f.patch
Patch0275: 0275-tests-add-test-command-file-tests.patch
Patch0276: 0276-net-ip-check-result-of-grub_netbuff_push.patch
Patch0277: 0277-grub-mkimage-fix-potential-NULL-pointer-dereference.patch
Patch0278: 0278-net-pxe-fix-error-condition.patch
Patch0279: 0279-grub-fstest-fix-descriptor-leak.patch
Patch0280: 0280-setup-fix-blocklist-size-calculation.patch
Patch0281: 0281-arm-implement-additional-relocations-generated-by-gc.patch
Patch0282: 0282-util-mkimage-fix-gcc5-build-failure.patch
Patch0283: 0283-diskfilter-fix-crash-in-validate_lv-for-mdraid-array.patch
Patch0284: 0284-diskfilter-fix-double-free-of-lv-names-for-mdraid.patch
Patch0285: 0285-multiboot2-Fix-information-request-tag-size-calculat.patch
Patch0286: 0286-disk-lvm-Use-zalloc-to-ensure-that-segments-are-init.patch
Patch0287: 0287-diskfilter_make_raid-more-memory-leaks-in-failure-pa.patch
Patch0288: 0288-syslinux_parse-Always-output-comments-even-if-no-ent.patch
Patch0289: 0289-Don-t-remove-initrd-parameter.patch
Patch0290: 0290-Add-test-for-syslinux-converter.patch
Patch0291: 0291-build-sys-add-syslinux-test-files-to-tarball.patch
Patch0292: 0292-tests-remove-hardcoded-paths-from-syslinux_test.patch
Patch0293: 0293-ext2-Support-META_BG.patch
Patch0294: 0294-ext2-Ignore-INCOMPAT_MMP.patch
Patch0295: 0295-configure-Add-missing-comma.patch
Patch0296: 0296-configure-Move-adding-of-include-options-to-the-very.patch
Patch0297: 0297-Strip-.MIPS.abiflags-which-causes-compile-failure.patch
Patch0298: 0298-INSTALL-Fix-names-of-host-flags-to-match-actual-beha.patch
Patch0299: 0299-div_test-Don-t-try-to-divide-by-zero.patch
Patch0300: 0300-Provide-__aeabi_mem-cpy-set.patch
Patch0301: 0301-mips-startup_raw-Use-more-portable-.asciz.patch
Patch0302: 0302-configure-Add-msoft-float-to-CCASFLAGS.patch
Patch0303: 0303-ofdisk-Exclude-floppies-from-scanning.patch
Patch0304: 0304-wildcard-Mark-unused-argument-as-such.patch
Patch0305: 0305-zfs-mzap_lookup-Fix-argument-types.patch
Patch0306: 0306-INSTALL-clarify-that-clang-support-is-experimental.patch
Patch0307: 0307-Test-which-flags-make-our-asm-compile.patch
Patch0308: 0308-i386-Move-from-explicit-ADDR32-DATA32-prefixes-to-in.patch
Patch0309: 0309-Change-dot-assignmnet-to-more-portable-.org.patch
Patch0310: 0310-i386-pc-boot-Explicitly-mark-kernel_address-_high-as.patch
Patch0311: 0311-i386-Remove-needless-ADDR32-prefixes-when-address-is.patch
Patch0312: 0312-Remove-obsolete-ADDR32-and-DATA32-checks.patch
Patch0313: 0313-Remove-realmode.S-from-coreboot-and-qemu.patch
Patch0314: 0314-qemu-Fix-compilation.patch
Patch0315: 0315-qemu-Fix-GateA20-enabling.patch
Patch0316: 0316-qemu-Switch-to-more-portable-.org.patch
Patch0317: 0317-Relax-requirements-on-asm-for-non-BIOS-i386-platform.patch
Patch0318: 0318-kernel-8086-Switch-to-more-portable-.org.patch
Patch0319: 0319-sparc64-Switch-to-more-portable-.org.patch
Patch0320: 0320-mips-Switch-to-more-portable-.org.patch
Patch0321: 0321-Discover-which-option-provides-soft-float-on-configu.patch
Patch0322: 0322-Experimental-support-for-clang-for-sparc64.patch
Patch0323: 0323-i386-tsc-Fix-unused-function-warning-on-xen.patch
Patch0324: 0324-configure.ac-Add-ia64-specific-way-to-disable-floats.patch
Patch0325: 0325-acpi-Fix-unused-function-warning.patch
Patch0326: 0326-Supply-signed-division-to-fix-ARM-compilation.patch
Patch0327: 0327-arm64-Fix-compilation-failure.patch
Patch0328: 0328-Allow-clang-compilation-for-thumb-with-mthumb-interw.patch
Patch0329: 0329-Add-missing-grub_-prefix-in-memcpy-invocation.patch
Patch0330: 0330-mips-Fix-soft-float-handling.patch
Patch0331: 0331-minilzo-Skip-parts-tha-we-don-t-need.patch
Patch0332: 0332-bitmap_scale-Optimize-by-moving-division-out-of-the-.patch
Patch0333: 0333-fbblit-Optimize-by-replacing-division-with-additions.patch
Patch0334: 0334-Add-missing-lib-division.c.patch
Patch0335: 0335-png-Optimize-by-avoiding-divisions.patch
Patch0336: 0336-jpeg-Optimise-by-replacing-division-with-shifts.patch
Patch0337: 0337-crypto-restrict-cipher-block-size-to-power-of-2.patch
Patch0338: 0338-dmraid_nvidia-Fix-division-by-0-and-missing-byte-swa.patch
Patch0339: 0339-raid6-Optimize-by-removing-division.patch
Patch0340: 0340-gzio-Optimize-by-removing-division.patch
Patch0341: 0341-arm-dl-Fix-handling-of-nonstandard-relocation-sizes.patch
Patch0342: 0342-emu-cache-Change-declaration-of-__clear_cache-to-mat.patch
Patch0343: 0343-ntfs_test-Skip-is-setfattr-is-unavailable.patch
Patch0344: 0344-grub-shell-Add-missing-locale-directory.patch
Patch0345: 0345-grub-probe-Mark-a-default-for-translation.patch
Patch0346: 0346-exclude.pot-Add-new-technical-strings.patch
Patch0347: 0347-grub-probe-free-temporary-variable.patch
Patch0348: 0348-Don-t-continue-to-query-block-size-if-disk-doesn-t-h.patch
Patch0349: 0349-configure.ac-Set-CPPFLAGS-when-checking-for-no_app_r.patch
Patch0350: 0350-types.h-Use-__builtin_bswap-with-clang.patch
Patch0351: 0351-Remove-libgcc-dependency.patch
Patch0352: 0352-configure.ac-Remove-unused-COND_clang.patch
Patch0353: 0353-Remove-emu-libusb-support.patch
Patch0354: 0354-Fix-canonicalize_file_name-clash.patch
Patch0355: 0355-configure.ac-Fix-the-name-of-pciaccess-header.patch
Patch0356: 0356-syslinux_parse-Fix-the-case-of-unknown-localboot.patch
Patch0357: 0357-update-m4-extern-inline.m4-to-upstream-version-to-fi.patch
Patch0358: 0358-update-gnulib-argp-help.c-to-fix-garbage-in-grub-mkn.patch
Patch0359: 0359-autogen.sh-Allow-overriding-the-python-to-be-used-by.patch
Patch0360: 0360-hfsplus-Fix-potential-access-to-uninited-memory-on-i.patch
Patch0361: 0361-grub-fs-tester-better-estimation-of-filesystem-time-.patch
Patch0362: 0362-grub-fs-tester-explicitly-set-segment-type-for-LVM-m.patch
Patch0363: 0363-core-add-LVM-RAID1-support.patch
Patch0364: 0364-grub-fs-tester-add-LVM-RAID1-support.patch
Patch0365: 0365-cacheinfo-Add-missing-license-information.patch
Patch0366: 0366-grub-mkrescue-pass-all-unrecognized-options-unchange.patch
Patch0367: 0367-fddboot_test-Add-no-pad-to-xorriso.patch
Patch0368: 0368-emunet-Fix-init-error-checking.patch
Patch0369: 0369-compiler-rt-emu-Add-missing-file.patch
Patch0370: 0370-hostfs-Drop-unnecessary-feature-test-macros.patch
Patch0371: 0371-arp-icmp-Fix-handling-in-case-of-oversized-or-invali.patch
Patch0372: 0372-Makefile.core.def-Remove-obsolete-LDADD_KERNEL.patch
Patch0373: 0373-modinfo.sh.in-Add-missing-config-variables.patch
Patch0374: 0374-util-mkimage-Use-stable-timestamp-when-generating-bi.patch
Patch0375: 0375-Make-Makefile.util.def-independent-of-platform.patch
Patch0376: 0376-efinet-Check-for-immediate-completition.patch
Patch0377: 0377-dl_helper-Cleanup.patch
Patch0378: 0378-Add-missing-initializers-to-silence-suprious-warning.patch
Patch0379: 0379-Recognize-EFI-platform-even-in-case-of-mismatch-betw.patch
Patch0380: 0380-syslinux-Support-vesa-menu.c32.patch
Patch0381: 0381-net-trivial-grub_cpu_to_XX_compile_time-cleanup.patch
Patch0382: 0382-grub-core-loader-i386-xen.c-Initialized-initrd_ctx-s.patch
Patch0383: 0383-do-not-emit-cryptomount-without-crypto-UUID.patch
Patch0384: 0384-core-avoid-NULL-derefrence-in-grub_divmod64s.patch
Patch0385: 0385-docs-grub.texi-Fix-spelling-of-cbfstool.patch
Patch0386: 0386-core-partmap-rename-sun-to-avoid-clash-with-predefin.patch
Patch0387: 0387-getroot-include-sys-mkdev.h-for-makedev.patch
Patch0388: 0388-Remove-V-in-grub-mkrescue.c.patch
Patch0389: 0389-grub-mkconfig-use-pkgdatadir-in-scripts.patch
Patch0390: 0390-zfs-com.delphix-hole_birth-feature-support.patch
Patch0391: 0391-zfs-com.delphix-embedded_data-feature-support.patch
Patch0392: 0392-zfs-add-missing-NULL-check-and-fix-incorrect-buffer-.patch
Patch0393: 0393-efinet-memory-leak-on-module-removal.patch
Patch0394: 0394-efinet-cannot-free-const-char-pointer.patch
Patch0395: 0395-Revert-efinet-memory-leak-on-module-removal.patch
Patch0396: 0396-arm64-Export-useful-functions-from-linux.c.patch
Patch0397: 0397-fdt.h-Add-grub_fdt_set_reg64-macro.patch
Patch0398: 0398-Revert-parts-accidentally-committed-2-commits-ago.patch
Patch0399: 0399-linux.c-Ensure-that-initrd-is-page-aligned.patch
Patch0400: 0400-grub-mkrescue-Recognize-output-as-an-alias-of-output.patch
Patch0401: 0401-grub-install-common-Increase-buf-size-to-8192-as-mod.patch
Patch0402: 0402-i386-relocator-Remove-unused-extern-grub_relocator64.patch
Patch0403: 0403-loader-linux-do-not-pad-initrd-with-zeroes-at-the-en.patch
Patch0404: 0404-convert-to-not-from-CPU-byte-order-in-DNS-receive-fu.patch
Patch0405: 0405-efidisk-move-device-path-helpers-in-core-for-efinet.patch
Patch0406: 0406-efinet-skip-virtual-IPv4-and-IPv6-devices-when-enume.patch
Patch0407: 0407-efinet-open-Simple-Network-Protocol-exclusively.patch
Patch0408: 0408-util-grub-mkrescue-Fix-compilation.patch
Patch0409: 0409-Add-asm-tests-to-tarball.patch
Patch0410: 0410-acpi-do-not-skip-BIOS-scan-if-EBDA-length-is-zero.patch
Patch0411: 0411-xfs-Fix-termination-loop-for-directory-iteration.patch
Patch0412: 0412-xfs-Convert-inode-numbers-to-cpu-endianity-immediate.patch
Patch0413: 0413-remove-extra-newlines-in-grub_util_-strings.patch
Patch0414: 0414-zfs-fix-integer-truncation-in-zap_lookup.patch
Patch0415: 0415-hostdisk-fix-crash-with-NULL-device.map.patch
Patch0416: 0416-bootp-ignore-gateway_ip-relay-field.patch
Patch0417: 0417-cb_timestamps.c-Add-new-time-stamp-descriptions.patch
Patch0418: 0418-disk-ahci-Use-defines-GRUB_ATA_STATUS_BUSY-and-GRUB_.patch
Patch0419: 0419-multiboot1-never-place-modules-in-low-memory.patch
Patch0420: 0420-zfs-extensible_dataset-and-large_blocks-feature-supp.patch
Patch0421: 0421-Correct-spelling-of-scheduled.patch
Patch0422: 0422-Clarify-use-of-superusers-variable-and-menu-entry-ac.patch
Patch0423: 0423-disk-ahci.c-Add-port-number-to-port-debug-messages.patch
Patch0424: 0424-arm64-setjmp-Add-missing-license-macro.patch
Patch0425: 0425-configure.ac-clean-up-arm64-soft-float-handling.patch
Patch0426: 0426-multiboot_header_tag_module_align-fix-to-confirm-mul.patch
Patch0427: 0427-xfs-Add-helpers-for-inode-size.patch
Patch0428: 0428-xfs-V5-filesystem-format-support.patch
Patch0429: 0429-NEWS-XFS-v5-support.patch
Patch0430: 0430-disk-ahci.c-Use-defines-GRUB_AHCI_HBA_PORT_CMD_SPIN_.patch
Patch0431: 0431-Fix-exit-to-EFI-firmware.patch
Patch0432: 0432-Migrate-PPC-from-Yaboot-to-Grub2.patch
Patch0433: 0433-Add-fw_path-variable-revised.patch
Patch0434: 0434-Add-support-for-linuxefi.patch
Patch0435: 0435-Use-linuxefi-and-initrdefi-where-appropriate.patch
Patch0436: 0436-Don-t-allow-insmod-when-secure-boot-is-enabled.patch
Patch0437: 0437-Pass-x-hex-hex-straight-through-unmolested.patch
Patch0438: 0438-Fix-crash-on-http.patch
Patch0439: 0439-IBM-client-architecture-CAS-reboot-support.patch
Patch0440: 0440-Add-vlan-tag-support.patch
Patch0441: 0441-Add-X-option-to-printf-functions.patch
Patch0442: 0442-DHCP-client-ID-and-UUID-options-added.patch
Patch0443: 0443-Search-for-specific-config-file-for-netboot.patch
Patch0444: 0444-blscfg-add-blscfg-module-to-parse-Boot-Loader-Specif.patch
Patch0445: 0445-Move-bash-completion-script-922997.patch
Patch0446: 0446-for-ppc-reset-console-display-attr-when-clear-screen.patch
Patch0447: 0447-Don-t-write-messages-to-the-screen.patch
Patch0448: 0448-Don-t-print-GNU-GRUB-header.patch
Patch0449: 0449-Don-t-add-to-highlighted-row.patch
Patch0450: 0450-Message-string-cleanups.patch
Patch0451: 0451-Fix-border-spacing-now-that-we-aren-t-displaying-it.patch
Patch0452: 0452-Use-the-correct-indentation-for-the-term-help-text.patch
Patch0453: 0453-Indent-menu-entries.patch
Patch0454: 0454-Fix-margins.patch
Patch0455: 0455-Add-support-for-UEFI-operating-systems-returned-by-o.patch
Patch0456: 0456-Disable-GRUB-video-support-for-IBM-power-machines.patch
Patch0457: 0457-Use-2-instead-of-1-for-our-right-hand-margin-so-line.patch
Patch0458: 0458-Use-linux16-when-appropriate-880840.patch
Patch0459: 0459-Enable-pager-by-default.-985860.patch
Patch0460: 0460-F10-doesn-t-work-on-serial-so-don-t-tell-the-user-to.patch
Patch0461: 0461-Don-t-say-GNU-Linux-in-generated-menus.patch
Patch0462: 0462-Don-t-draw-a-border-around-the-menu.patch
Patch0463: 0463-Use-the-standard-margin-for-the-timeout-string.patch
Patch0464: 0464-Fix-grub_script_execute_sourcecode-usage-on-ppc.patch
Patch0465: 0465-Add-.eh_frame-to-list-of-relocations-stripped.patch
Patch0466: 0466-Make-10_linux-work-with-our-changes-for-linux16-and-.patch
Patch0467: 0467-Don-t-print-during-fdt-loading-method.patch
Patch0468: 0468-Honor-a-symlink-when-generating-configuration-by-gru.patch
Patch0469: 0469-Don-t-munge-raw-spaces-when-we-re-doing-our-cmdline-.patch
Patch0470: 0470-Don-t-require-a-password-to-boot-entries-generated-b.patch
Patch0471: 0471-Don-t-emit-Booting-.-message.patch
Patch0472: 0472-Make-CTRL-and-ALT-keys-work-as-expected-on-EFI-syste.patch
Patch0473: 0473-May-as-well-try-it.patch
Patch0474: 0474-use-fw_path-prefix-when-fallback-searching-for-grub-.patch
Patch0475: 0475-Try-mac-guid-etc-before-grub.cfg-on-tftp-config-file.patch
Patch0476: 0476-trim-arp-packets-with-abnormal-size.patch
Patch0477: 0477-Fix-convert-function-to-support-NVMe-devices.patch
Patch0478: 0478-Fix-bad-test-on-GRUB_DISABLE_SUBMENU.patch
Patch0479: 0479-Switch-to-use-APM-Mustang-device-tree-for-hardware-t.patch
Patch0480: 0480-Use-the-default-device-tree-from-the-grub-default-fi.patch
Patch0481: 0481-reopen-SNP-protocol-for-exclusive-use-by-grub.patch
Patch0482: 0482-Reduce-timer-event-frequency-by-10.patch
Patch0483: 0483-always-return-error-to-UEFI.patch
Patch0484: 0484-Add-powerpc-little-endian-ppc64le-flags.patch
Patch0485: 0485-Files-reorganization-and-include-some-libgcc-fuction.patch
Patch0486: 0486-Suport-for-bi-endianess-in-elf-file.patch
Patch0487: 0487-Add-grub_util_readlink.patch
Patch0488: 0488-Make-editenv-chase-symlinks-including-those-across-d.patch
Patch0489: 0489-Generate-OS-and-CLASS-in-10_linux-from-etc-os-releas.patch
Patch0490: 0490-Fix-GRUB_DISABLE_SUBMENU-one-more-time.patch
Patch0491: 0491-Minimize-the-sort-ordering-for-.debug-and-rescue-ker.patch
Patch0492: 0492-Add-GRUB_DISABLE_UUID.patch
Patch0493: 0493-Allow-fallback-to-include-entries-by-title-not-just-.patch
Patch0494: 0494-Load-arm-with-SB-enabled.patch
Patch0495: 0495-Try-prefix-if-fw_path-doesn-t-work.patch
Patch0496: 0496-Try-to-emit-linux16-initrd16-and-linuxefi-initrdefi-.patch
Patch0497: 0497-Update-to-minilzo-2.08.patch
Patch0498: 0498-Make-grub2-mkconfig-construct-titles-that-look-like-.patch
Patch0499: 0499-Make-rescue-and-debug-entries-sort-right-again-in-gr.patch
Patch0500: 0500-Make-.gitignore-suck-way-less.patch
Patch0501: 0501-Update-info-with-grub.cfg-netboot-selection-order-11.patch
Patch0502: 0502-Use-Distribution-Package-Sort-for-grub2-mkconfig-112.patch
Patch0503: 0503-Add-friendly-grub2-password-config-tool-985962.patch
Patch0504: 0504-Make-exit-take-a-return-code.patch
Patch0505: 0505-Add-some-__unused__-where-gcc-5.x-is-more-picky-abou.patch
Patch0506: 0506-Fix-race-in-EFI-validation.patch

BuildRequires:  flex bison binutils python
BuildRequires:  ncurses-devel xz-devel bzip2-devel
BuildRequires:  freetype-devel libusb-devel
%ifarch %{sparc} x86_64 aarch64 ppc64le
# sparc builds need 64 bit glibc-devel - also for 32 bit userland
BuildRequires:  /usr/lib64/crt1.o glibc-static
%else
# ppc64 builds need the ppc crt1.o
BuildRequires:  /usr/lib/crt1.o glibc-static
%endif
BuildRequires:  autoconf automake autogen device-mapper-devel
BuildRequires:	freetype-devel gettext-devel git
BuildRequires:	texinfo
BuildRequires:	dejavu-sans-fonts
BuildRequires:	help2man
%ifarch %{efiarchs}
%ifnarch aarch64
BuildRequires:	pesign >= 0.99-8
%endif
%endif

Requires:	gettext which file
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Requires:	os-prober >= 1.58-11
Requires(pre):  dracut
Requires(post): dracut

ExcludeArch:	s390 s390x %{arm}
Obsoletes:	grub2 <= 1:2.00-20%{?dist}

%description
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for PC BIOS systems.

%ifarch %{efiarchs}
%package efi
Summary:	GRUB for EFI systems.
Group:		System Environment/Base
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Obsoletes:	grub2-efi <= 1:2.00-20%{?dist}

%description efi
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for EFI systems.

%package efi-modules
Summary:	Modules used to build custom grub.efi images
Group:		System Environment/Base
Requires:	%{name}-tools = %{epoch}:%{version}-%{release}
Obsoletes:	grub2-efi <= 1:2.00-20%{?dist}

%description efi-modules
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides support for rebuilding your own grub.efi on EFI systems.
%endif

%package tools
Summary:	Support tools for GRUB.
Group:		System Environment/Base
Requires:	gettext os-prober which file system-logos

%description tools
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides tools for support of all platforms.

%package starfield-theme
Summary:	An example theme for GRUB.
Group:		System Environment/Base
Requires:	system-logos
Obsoletes:	grub2 <= 1:2.00-20%{?dist}
Obsoletes:	grub2-efi <= 1:2.00-20%{?dist}

%description starfield-theme
The GRand Unified Bootloader (GRUB) is a highly configurable and customizable
bootloader with modular architecture.  It support rich varietyof kernel formats,
file systems, computer architectures and hardware devices.  This subpackage
provides an example theme for the grub screen.

%prep
%setup -T -c -n grub-%{tarversion}
%ifarch %{efiarchs}
%setup -D -q -T -a 0 -n grub-%{tarversion}
cd grub-%{tarversion}
# place unifont in the '.' from which configure is run
cp %{SOURCE4} unifont.pcf.gz
cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name
cd ..
mv grub-%{tarversion} grub-efi-%{tarversion}
%endif

%ifarch %{efi_only}
ln -s grub-efi-%{tarversion} grub-%{tarversion}
%else
%setup -D -q -T -a 0 -n grub-%{tarversion}
cd grub-%{tarversion}
# place unifont in the '.' from which configure is run
cp %{SOURCE4} unifont.pcf.gz
cp %{SOURCE6} .gitignore
git init
echo '![[:digit:]][[:digit:]]_*.in' > util/grub.d/.gitignore
echo '!*.[[:digit:]]' > util/.gitignore
git config user.email "%{name}-owner@fedoraproject.org"
git config user.name "Fedora Ninjas"
git config gc.auto 0
git add .
git commit -a -q -m "%{tarversion} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name
%endif

%build
%ifarch %{efiarchs}
cd grub-efi-%{tarversion}
./autogen.sh
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-O.//g'					\
		-e 's/-fstack-protector[[:alpha:]-]\+//g'	\
		-e 's/-Wp,-D_FORTIFY_SOURCE=[[:digit:]]\+//g'	\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-fasynchronous-unwind-tables//g'		\
		-e 's/^/ -fno-strict-aliasing /' )"		\
	TARGET_LDFLAGS=-static					\
        --with-platform=efi					\
	--with-grubdir=%{name}					\
        --program-transform-name=s,grub,%{name},		\
	--disable-grub-mount					\
	--disable-werror
make %{?_smp_mflags}

GRUB_MODULES="	all_video boot btrfs cat chain configfile echo \
		efifwsetup efinet ext2 fat font gfxmenu gfxterm gzio halt \
		hfsplus iso9660 jpeg loadenv loopback lvm mdraid09 mdraid1x \
		minicmd normal part_apple part_msdos part_gpt \
		password_pbkdf2 png \
		reboot search search_fs_uuid search_fs_file search_label \
		serial sleep syslinuxcfg test tftp video xfs"
%ifarch aarch64
GRUB_MODULES+=" linux "
%else
GRUB_MODULES+=" backtrace usb usbserial_common "
GRUB_MODULES+=" usbserial_pl2303 usbserial_ftdi usbserial_usbdebug "
GRUB_MODULES+=" linuxefi multiboot2 multiboot "
%endif
./grub-mkimage -O %{grubefiarch} -o %{grubefiname}.orig -p /EFI/%{efidir} \
		-d grub-core ${GRUB_MODULES}
./grub-mkimage -O %{grubefiarch} -o %{grubeficdname}.orig -p /EFI/BOOT \
		-d grub-core ${GRUB_MODULES}
%ifarch aarch64
mv %{grubefiname}.orig %{grubefiname}
mv %{grubeficdname}.orig %{grubeficdname}
%else
%pesign -s -i %{grubeficdname}.orig -o %{grubeficdname}
%pesign -s -i %{grubefiname}.orig -o %{grubefiname}
%endif
cd ..
%endif

cd grub-%{tarversion}
%ifnarch %{efi_only}
./autogen.sh
# -static is needed so that autoconf script is able to link
# test that looks for _start symbol on 64 bit platforms
%ifarch %{sparc} ppc ppc64 ppc64le
%define platform ieee1275
%else
%define platform pc
%endif
%configure							\
	CFLAGS="$(echo $RPM_OPT_FLAGS | sed			\
		-e 's/-O.//g'					\
		-e 's/-fstack-protector[[:alpha:]-]\+//g'	\
		-e 's/-Wp,-D_FORTIFY_SOURCE=[[:digit:]]\+//g'	\
		-e 's/--param=ssp-buffer-size=4//g'		\
		-e 's/-mregparm=3/-mregparm=4/g'		\
		-e 's/-fexceptions//g'				\
		-e 's/-m64//g'					\
		-e 's/-fasynchronous-unwind-tables//g'		\
		-e 's/-mcpu=power7/-mcpu=power6/g'		\
		-e 's/^/ -fno-strict-aliasing /' )"		\
	TARGET_LDFLAGS=-static					\
        --with-platform=%{platform}				\
	--with-grubdir=%{name}					\
        --program-transform-name=s,grub,%{name},		\
	--disable-grub-mount					\
	--disable-werror

make %{?_smp_mflags}
%endif

sed -i -e 's,(grub),(%{name}),g' \
	-e 's,grub.info,%{name}.info,g' \
	-e 's,\* GRUB:,* GRUB2:,g' \
	-e 's,/boot/grub/,/boot/%{name}/,g' \
	-e 's,\([^-]\)grub-\([a-z]\),\1%{name}-\2,g' \
	docs/grub.info
sed -i -e 's,grub-dev,%{name}-dev,g' docs/grub-dev.info

/usr/bin/makeinfo --html --no-split -I docs -o grub-dev.html docs/grub-dev.texi
/usr/bin/makeinfo --html --no-split -I docs -o grub.html docs/grub.texi
sed -i	-e 's,/boot/grub/,/boot/%{name}/,g' \
	-e 's,\([^-]\)grub-\([a-z]\),\1%{name}-\2,g' \
	grub.html

%install
set -e
rm -fr $RPM_BUILD_ROOT

%ifarch %{efiarchs}
cd grub-efi-%{tarversion}
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -iname "*.module" -exec chmod a-x {} \;

# Ghost config file
install -m 755 -d $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/
touch $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/grub.cfg
ln -s ../boot/efi/EFI/%{efidir}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}-efi.cfg

install -m 755 %{grubefiname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubefiname}
install -m 755 %{grubeficdname} $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/%{grubeficdname}
install -D -m 644 unicode.pf2 $RPM_BUILD_ROOT/boot/efi/EFI/%{efidir}/fonts/unicode.pf2
cd ..
%endif

cd grub-%{tarversion}
%ifnarch %{efi_only}
make DESTDIR=$RPM_BUILD_ROOT install

# Ghost config file
install -d $RPM_BUILD_ROOT/boot/%{name}
touch $RPM_BUILD_ROOT/boot/%{name}/grub.cfg
ln -s ../boot/%{name}/grub.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg
%endif

cp -a $RPM_BUILD_ROOT%{_datarootdir}/locale/en\@quot $RPM_BUILD_ROOT%{_datarootdir}/locale/en

mv $RPM_BUILD_ROOT%{_infodir}/grub.info $RPM_BUILD_ROOT%{_infodir}/%{name}.info
mv $RPM_BUILD_ROOT%{_infodir}/grub-dev.info $RPM_BUILD_ROOT%{_infodir}/%{name}-dev.info
rm $RPM_BUILD_ROOT%{_infodir}/dir

# Defaults
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/default
touch ${RPM_BUILD_ROOT}%{_sysconfdir}/default/grub
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub \
	${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/grub

cd ..
%find_lang grub

# Fedora theme in /boot/grub2/themes/system/
cd $RPM_BUILD_ROOT
tar xjf %{SOURCE5}
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub2/themes/system/DejaVuSans-10.pf2      -s 10 /usr/share/fonts/dejavu/DejaVuSans.ttf # "DejaVu Sans Regular 10"
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub2/themes/system/DejaVuSans-12.pf2      -s 12 /usr/share/fonts/dejavu/DejaVuSans.ttf # "DejaVu Sans Regular 12"
$RPM_BUILD_ROOT%{_bindir}/%{name}-mkfont -o boot/grub2/themes/system/DejaVuSans-Bold-14.pf2 -s 14 /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf # "DejaVu Sans Bold 14"

# Make selinux happy with exec stack binaries.
mkdir ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/
cat << EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/grub2.conf
# these have execstack, and break under selinux
-b /usr/bin/grub2-script-check
-b /usr/bin/grub2-mkrelpath
-b /usr/bin/grub2-fstest
-b /usr/sbin/grub2-bios-setup
-b /usr/sbin/grub2-probe
-b /usr/sbin/grub2-sparc64-setup
EOF

%ifarch %{efiarchs}
mkdir -p boot/efi/EFI/%{efidir}/
ln -s /boot/efi/EFI/%{efidir}/grubenv boot/grub2/grubenv
%endif

# Don't run debuginfo on all the grub modules and whatnot; it just
# rejects them, complains, and slows down extraction.
%global finddebugroot "%{_builddir}/%{?buildsubdir}/debug"
mkdir -p %{finddebugroot}/usr
cp -a ${RPM_BUILD_ROOT}/usr/bin %{finddebugroot}/usr/bin
cp -a ${RPM_BUILD_ROOT}/usr/sbin %{finddebugroot}/usr/sbin

%global dip RPM_BUILD_ROOT=%{finddebugroot} %{__debug_install_post}
%define __debug_install_post ( %{dip}					\
	install -m 0755 -d %{buildroot}/usr/lib/ %{buildroot}/usr/src/	\
	cp -al %{finddebugroot}/usr/lib/debug/				\\\
		%{buildroot}/usr/lib/debug/				\
	cp -al %{finddebugroot}/usr/src/debug/				\\\
		%{buildroot}/usr/src/debug/ )

%clean    
rm -rf $RPM_BUILD_ROOT

%post tools
if [ "$1" = 1 ]; then
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz || :
	/sbin/install-info --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info.gz || :
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

%preun tools
if [ "$1" = 0 ]; then
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz || :
	/sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}-dev.info.gz || :
fi

%ifnarch %{efi_only}
%files -f grub.lang
%defattr(-,root,root,-)
%{_libdir}/grub/*-%{platform}/
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%ghost %config(noreplace) /boot/%{name}/grub.cfg
%doc grub-%{tarversion}/COPYING
%config(noreplace) %ghost /boot/grub2/grubenv
%endif

%ifarch %{efiarchs}
%files efi
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}-efi.cfg
%attr(0755,root,root)/boot/efi/EFI/%{efidir}
%attr(0755,root,root)/boot/efi/EFI/%{efidir}/fonts
%ghost %config(noreplace) /boot/efi/EFI/%{efidir}/grub.cfg
%doc grub-%{tarversion}/COPYING
/boot/grub2/grubenv
# I know 0700 seems strange, but it lives on FAT so that's what it'll
# get no matter what we do.
%config(noreplace) %ghost %attr(0700,root,root)/boot/efi/EFI/%{efidir}/grubenv

%files efi-modules
%defattr(-,root,root,-)
%{_libdir}/grub/%{grubefiarch}
%endif

%files tools -f grub.lang
%defattr(-,root,root,-)
%dir %{_libdir}/grub/
%dir %{_datarootdir}/grub/
%dir %{_datarootdir}/grub/themes
%{_datarootdir}/grub/*
%{_sbindir}/%{name}-bios-setup
%{_sbindir}/%{name}-install
%{_sbindir}/%{name}-macbless
%{_sbindir}/%{name}-mkconfig
%{_sbindir}/%{name}-ofpathname
%{_sbindir}/%{name}-probe
%{_sbindir}/%{name}-reboot
%{_sbindir}/%{name}-set-default
%{_sbindir}/%{name}-sparc64-setup
%{_bindir}/%{name}-editenv
%{_bindir}/%{name}-file
%{_bindir}/%{name}-fstest
%{_bindir}/%{name}-glue-efi
%{_bindir}/%{name}-kbdcomp
%{_bindir}/%{name}-menulst2cfg
%{_bindir}/%{name}-mkfont
%{_bindir}/%{name}-mkimage
%{_bindir}/%{name}-mklayout
%{_bindir}/%{name}-mknetdir
%{_bindir}/%{name}-mkpasswd-pbkdf2
%{_bindir}/%{name}-mkrelpath
%ifnarch %{sparc}
%{_bindir}/%{name}-mkrescue
%endif
%{_bindir}/%{name}-mkstandalone
%{_bindir}/%{name}-render-label
%{_bindir}/%{name}-script-check
%{_bindir}/%{name}-syslinux2cfg
%{_datarootdir}/bash-completion/completions/grub
%{_sysconfdir}/prelink.conf.d/grub2.conf
%attr(0700,root,root) %dir %{_sysconfdir}/grub.d
%config %{_sysconfdir}/grub.d/??_*
%{_sysconfdir}/grub.d/README
%attr(0644,root,root) %ghost %config(noreplace) %{_sysconfdir}/default/grub
%{_sysconfdir}/sysconfig/grub
%dir /boot/%{name}
%dir /boot/%{name}/themes/
%dir /boot/%{name}/themes/system
%exclude /boot/%{name}/themes/system/*
%exclude %{_datarootdir}/grub/themes/
%{_infodir}/%{name}*
%{_datadir}/man/man?/*
%doc grub-%{tarversion}/COPYING grub-%{tarversion}/INSTALL
%doc grub-%{tarversion}/NEWS grub-%{tarversion}/README
%doc grub-%{tarversion}/THANKS grub-%{tarversion}/TODO
%doc grub-%{tarversion}/grub.html
%doc grub-%{tarversion}/grub-dev.html grub-%{tarversion}/docs/font_char_metrics.png
%doc grub-%{tarversion}/themes/starfield/COPYING.CC-BY-SA-3.0

%files starfield-theme
%dir /boot/%{name}/themes/
/boot/%{name}/themes/system
%dir %{_datarootdir}/grub/themes
%{_datarootdir}/grub/themes/starfield

%changelog
* Sun Jul 19 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.02-0.17
- Don't build hardened (fixes FTBFS)

* Tue Apr 28 2015 Peter Jones <pjones@redhat.com> - 2.02-0.16
- Make grub2-mkconfig produce the kernel titles we actually want.
  Resolves: rhbz#1215839

* Sat Feb 21 2015 Till Maas <opensource@till.name>
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Jan 05 2015 Peter Jones <pjones@redhat.com> - 2.02-0.15
- Bump release to rebuild with Ralf Corsépius's fixes.

* Sun Jan 04 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.02-0.14
- Move grub2.info/grub2-dev.info install-info scriptlets into *-tools package.
- Use sub-shell in %%__debug_install_post (RHBZ#1168732).
- Cleanup grub2-starfield-theme packaging.

* Thu Dec 04 2014 Peter Jones <pjones@redhat.com> - 2.02-0.13
- Update minilzo to 2.08 for CVE-2014-4607
  Resolves: rhbz#1131793

* Thu Nov 13 2014 Peter Jones <pjones@redhat.com> - 2.02-0.12
- Make backtrace and usb conditional on !arm
- Make sure gcdaa64.efi is packaged.
  Resolves: rhbz#1163481

* Fri Nov 07 2014 Peter Jones <pjones@redhat.com> - 2.02-0.11
- fix a copy-paste error in patch 0154.
  Resolves: rhbz#964828

* Mon Oct 27 2014 Peter Jones <pjones@redhat.com> - 2.02-0.10
- Try to emit linux16/initrd16 and linuxefi/initrdefi when appropriate
  in 30_os-prober.
  Resolves: rhbz#1108296
- If $fw_path doesn't work to find the config file, try $prefix as well
  Resolves: rhbz#1148652

* Mon Sep 29 2014 Peter Jones <pjones@redhat.com> - 2.02-0.9
- Clean up the build a bit to make it faster
- Make grubenv work right on UEFI machines
  Related: rhbz#1119943
- Sort debug and rescue kernels later than normal ones
  Related: rhbz#1065360
- Allow "fallback" to include entries by title as well as number.
  Related: rhbz#1026084
- Fix a segfault on aarch64.
- Load arm with SB enabled if available.
- Add some serial port options to GRUB_MODULES.

* Tue Aug 19 2014 Peter Jones <pjones@redhat.com> - 2.02-0.8
- Add ppc64le support.
  Resolves: rhbz#1125540

* Thu Jul 24 2014 Peter Jones <pjones@redhat.com> - 2.02-0.7
- Enabled syslinuxcfg module.

* Wed Jul 02 2014 Peter Jones <pjones@redhat.com> - 2.02-0.6
- Re-merge RHEL 7 changes and ARM works in progress.

* Mon Jun 30 2014 Peter Jones <pjones@redhat.com> - 2.02-0.5
- Avoid munging raw spaces when we're escaping command line arguments.
  Resolves: rhbz#923374

* Tue Jun 24 2014 Peter Jones <pjones@redhat.com> - 2.02-0.4
- Update to latest upstream.

* Thu Mar 13 2014 Peter Jones <pjones@redhat.com> - 2.02-0.3
- Merge in RHEL 7 changes and ARM works in progress.

* Mon Jan 06 2014 Peter Jones <pjones@redhat.com> - 2.02-0.2
- Update to grub-2.02~beta2

* Sat Aug 10 2013 Peter Jones <pjones@redhat.com> - 2.00-25
- Last build failed because of a hardware error on the builder.

* Mon Aug 05 2013 Peter Jones <pjones@redhat.com> - 2.00-24
- Fix compiler flags to deal with -fstack-protector-strong

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.00-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Dennis Gilmore <dennis@ausil.us> - 2.00-23
- add epoch to obsoletes

* Fri Jun 21 2013 Peter Jones <pjones@redhat.com> - 2.00-22
- Fix linewrapping in edit menu.
  Resolves: rhbz #976643

* Thu Jun 20 2013 Peter Jones <pjones@redhat.com> - 2.00-21
- Fix obsoletes to pull in -starfield-theme subpackage when it should.

* Fri Jun 14 2013 Peter Jones <pjones@redhat.com> - 2.00-20
- Put the theme entirely ento the subpackage where it belongs (#974667)

* Wed Jun 12 2013 Peter Jones <pjones@redhat.com> - 2.00-19
- Rebase to upstream snapshot.
- Fix PPC build error (#967862)
- Fix crash on net_bootp command (#960624)
- Reset colors on ppc when appropriate (#908519)
- Left align "Loading..." messages (#908492)
- Fix probing of SAS disks on PPC (#953954)
- Add support for UEFI OSes returned by os-prober
- Disable "video" mode on PPC for now (#973205)
- Make grub fit better into the boot sequence, visually (#966719)

* Fri May 10 2013 Matthias Clasen <mclasen@redhat.com> - 2.00-18
- Move the starfield theme to a subpackage (#962004)
- Don't allow SSE or MMX on UEFI builds (#949761)

* Wed Apr 24 2013 Peter Jones <pjones@redhat.com> - 2.00-17.pj0
- Rebase to upstream snapshot.

* Thu Apr 04 2013 Peter Jones <pjones@redhat.com> - 2.00-17
- Fix booting from drives with 4k sectors on UEFI.
- Move bash completion to new location (#922997)
- Include lvm support for /boot (#906203)

* Thu Feb 14 2013 Peter Jones <pjones@redhat.com> - 2.00-16
- Allow the user to disable submenu generation
- (partially) support BLS-style configuration stanzas.

* Tue Feb 12 2013 Peter Jones <pjones@redhat.com> - 2.00-15.pj0
- Add various config file related changes.

* Thu Dec 20 2012 Dennis Gilmore <dennis@ausil.us> - 2.00-15
- bump nvr

* Mon Dec 17 2012 Karsten Hopp <karsten@redhat.com> 2.00-14
- add bootpath device to the device list (pfsmorigo, #886685)

* Tue Nov 27 2012 Peter Jones <pjones@redhat.com> - 2.00-13
- Add vlan tag support (pfsmorigo, #871563)
- Follow symlinks during PReP installation in grub2-install (pfsmorigo, #874234)
- Improve search paths for config files on network boot (pfsmorigo, #873406)

* Tue Oct 23 2012 Peter Jones <pjones@redhat.com> - 2.00-12
- Don't load modules when grub transitions to "normal" mode on UEFI.

* Mon Oct 22 2012 Peter Jones <pjones@redhat.com> - 2.00-11
- Rebuild with newer pesign so we'll get signed with the final signing keys.

* Thu Oct 18 2012 Peter Jones <pjones@redhat.com> - 2.00-10
- Various PPC fixes.
- Fix crash fetching from http (gustavold, #860834)
- Issue separate dns queries for ipv4 and ipv6 (gustavold, #860829)
- Support IBM CAS reboot (pfsmorigo, #859223)
- Include all modules in the core image on ppc (pfsmorigo, #866559)

* Mon Oct 01 2012 Peter Jones <pjones@redhat.com> - 1:2.00-9
- Work around bug with using "\x20" in linux command line.
  Related: rhbz#855849

* Thu Sep 20 2012 Peter Jones <pjones@redhat.com> - 2.00-8
- Don't error on insmod on UEFI/SB, but also don't do any insmodding.
- Increase device path size for ieee1275
  Resolves: rhbz#857936
- Make network booting work on ieee1275 machines.
  Resolves: rhbz#857936

* Wed Sep 05 2012 Matthew Garrett <mjg@redhat.com> - 2.00-7
- Add Apple partition map support for EFI

* Thu Aug 23 2012 David Cantrell <dcantrell@redhat.com> - 2.00-6
- Only require pesign on EFI architectures (#851215)

* Tue Aug 14 2012 Peter Jones <pjones@redhat.com> - 2.00-5
- Work around AHCI firmware bug in efidisk driver.
- Move to newer pesign macros
- Don't allow insmod if we're in secure-boot mode.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com>
- Split module lists for UEFI boot vs UEFI cd images.
- Add raid modules for UEFI image (related: #750794)
- Include a prelink whitelist for binaries that need execstack (#839813)
- Include fix efi memory map fix from upstream (#839363)

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 2.00-4
- Correct grub-mkimage invocation to use efidir RPM macro (jwb)
- Sign with test keys on UEFI systems.
- PPC - Handle device paths with commas correctly.
  Related: rhbz#828740

* Wed Jul 25 2012 Peter Jones <pjones@redhat.com> - 2.00-3
- Add some more code to support Secure Boot, and temporarily disable
  some other bits that don't work well enough yet.
  Resolves: rhbz#836695

* Wed Jul 11 2012 Matthew Garrett <mjg@redhat.com> - 2.00-2
- Set a prefix for the image - needed for installer work
- Provide the font in the EFI directory for the same reason

* Thu Jun 28 2012 Peter Jones <pjones@redhat.com> - 2.00-1
- Rebase to grub-2.00 release.

* Mon Jun 18 2012 Peter Jones <pjones@redhat.com> - 2.0-0.37.beta6
- Fix double-free in grub-probe.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.36.beta6
- Build with patch19 applied.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.35.beta6
- More ppc fixes.

* Wed Jun 06 2012 Peter Jones <pjones@redhat.com> - 2.0-0.34.beta6
- Add IBM PPC fixes.

* Mon Jun 04 2012 Peter Jones <pjones@redhat.com> - 2.0-0.33.beta6
- Update to beta6.
- Various fixes from mads.

* Fri May 25 2012 Peter Jones <pjones@redhat.com> - 2.0-0.32.beta5
- Revert builddep change for crt1.o; it breaks ppc build.

* Fri May 25 2012 Peter Jones <pjones@redhat.com> - 2.0-0.31.beta5
- Add fwsetup command (pjones)
- More ppc fixes (IBM)

* Tue May 22 2012 Peter Jones <pjones@redhat.com> - 2.0-0.30.beta5
- Fix the /other/ grub2-tools require to include epoch.

* Mon May 21 2012 Peter Jones <pjones@redhat.com> - 2.0-0.29.beta5
- Get rid of efi_uga and efi_gop, favoring all_video instead.

* Mon May 21 2012 Peter Jones <pjones@redhat.com> - 2.0-0.28.beta5
- Name grub.efi something that's arch-appropriate (kiilerix, pjones)
- use EFI/$SOMETHING_DISTRO_BASED/ not always EFI/redhat/grub2-efi/ .
- move common stuff to -tools (kiilerix)
- spec file cleanups (kiilerix)

* Mon May 14 2012 Peter Jones <pjones@redhat.com> - 2.0-0.27.beta5
- Fix module trampolining on ppc (benh)

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 2.0-0.27.beta5
- Fix license of theme (mizmo)
  Resolves: rhbz#820713
- Fix some PPC bootloader detection IBM problem
  Resolves: rhbz#820722

* Thu May 10 2012 Peter Jones <pjones@redhat.com> - 2.0-0.26.beta5
- Update to beta5.
- Update how efi building works (kiilerix)
- Fix theme support to bring in fonts correctly (kiilerix, pjones)

* Wed May 09 2012 Peter Jones <pjones@redhat.com> - 2.0-0.25.beta4
- Include theme support (mizmo)
- Include locale support (kiilerix)
- Include html docs (kiilerix)

* Thu Apr 26 2012 Peter Jones <pjones@redhat.com> - 2.0-0.24
- Various fixes from Mads Kiilerich

* Thu Apr 19 2012 Peter Jones <pjones@redhat.com> - 2.0-0.23
- Update to 2.00~beta4
- Make fonts work so we can do graphics reasonably

* Thu Mar 29 2012 David Aquilina <dwa@redhat.com> - 2.0-0.22
- Fix ieee1275 platform define for ppc

* Thu Mar 29 2012 Peter Jones <pjones@redhat.com> - 2.0-0.21
- Remove ppc excludearch lines (dwa)
- Update ppc terminfo patch (hamzy)

* Wed Mar 28 2012 Peter Jones <pjones@redhat.com> - 2.0-0.20
- Fix ppc64 vs ppc exclude according to what dwa tells me they need
- Fix version number to better match policy.

* Tue Mar 27 2012 Dan Horák <dan[at]danny.cz> - 1.99-19.2
- Add support for serial terminal consoles on PPC by Mark Hamzy

* Sun Mar 25 2012 Dan Horák <dan[at]danny.cz> - 1.99-19.1
- Use Fix-tests-of-zeroed-partition patch by Mark Hamzy

* Thu Mar 15 2012 Peter Jones <pjones@redhat.com> - 1.99-19
- Use --with-grubdir= on configure to make it behave like -17 did.

* Wed Mar 14 2012 Peter Jones <pjones@redhat.com> - 1.99-18
- Rebase from 1.99 to 2.00~beta2

* Wed Mar 07 2012 Peter Jones <pjones@redhat.com> - 1.99-17
- Update for newer autotools and gcc 4.7.0
  Related: rhbz#782144
- Add /etc/sysconfig/grub link to /etc/default/grub
  Resolves: rhbz#800152
- ExcludeArch s390*, which is not supported by this package.
  Resolves: rhbz#758333

* Fri Feb 17 2012 Orion Poplawski <orion@cora.nwra.com> - 1:1.99-16
- Build with -Os (bug 782144)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.99-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Matthew Garrett <mjg@redhat.com> - 1.99-14
- fix up various grub2-efi issues

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
