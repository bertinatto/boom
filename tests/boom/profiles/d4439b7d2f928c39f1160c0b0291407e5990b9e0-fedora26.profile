BOOM_OS_ID="d4439b7d2f928c39f1160c0b0291407e5990b9e0"
BOOM_OS_NAME="Fedora"
BOOM_OS_SHORT_NAME="fedora"
BOOM_OS_VERSION="26 (Workstation Edition)"
BOOM_OS_VERSION_ID="26"
BOOM_OS_UNAME_PATTERN="fc26"
BOOM_OS_KERNEL_PATTERN="/vmlinuz-%{version}"
BOOM_OS_INITRAMFS_PATTERN="/initramfs-%{version}.img"
BOOM_OS_ROOT_OPTS_LVM2="rd.lvm.lv=%{lvm_root_lv}"
BOOM_OS_ROOT_OPTS_BTRFS="rootflags=%{btrfs_subvolume}"
BOOM_OS_OPTIONS="BOOT_IMAGE=%{kernel} root=%{root_device} ro %{root_opts}"
