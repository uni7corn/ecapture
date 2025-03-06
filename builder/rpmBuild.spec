Name:       ecapture
Version:    v0.0.1
Release:    2023%{?dist}
Summary:    Capture SSL/TLS plaintext content without CA certificates using eBPF
License:    Apache-2.0
URL:        https://ecapture.cc
Source0:    %{name}-%{version}.tar.gz

%global _missing_build_ids_terminate_build 0
%define debug_package %{nil}


%description
SSL/TLS plaintext capture,
supports OpenSSL, LibreSSL, BoringSSL, GnuTLS, and NSPR (NSS) libraries.

GoTLS plaintext support for the Go TLS library, which refers to encrypted

communication in HTTPS/TLS programs written in the Go language.

Bash audit captures bash commands for Host Security Audit.
Zsh audit captures zsh commands for Host Security Audit.
MySQL query SQL audit supports MySQL 5.6/5.7/8.0 and MariaDB.

%prep
%setup -c

%build
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/local/bin/
install -m 755 bin/ecapture %{buildroot}/usr/local/bin/ecapture
eu-strip %{buildroot}/usr/local/bin/ecapture

%post
echo "eCapture has been installed in the /usr/local/bin directory."
echo "Please ensure that /usr/local/bin is in your \$PATH, or use /usr/local/bin/ecapture directly."

%files
/usr/local/bin/ecapture

%changelog
* Sat Dec 30 2023 CFC4N <cfc4ncs@gmail.com> - 0.7.0-1
- Split `nss/gnutls/openssl` into three separate submodules. Corresponding to the `./ecapture nss`, `./ecapture gnutls`, `ecapture tls` commands.
- Support `keylog` mode, equivalent to the functionality of the `SSLKEYLOGFILE` environment variable. Captures SSL/TLS communication keys directly without the need for changes in the target process.
- Refactor the mode parameters supported by the `openssl`(aka tls) module using the `-m`parameter, with values `text`, `pcap`,`keylog`.
  - `pcap` mode: Set with `-m pcap` or `-m pcapng` parameters. When using this mode, it is necessary to specify `--pcapfile` and `-i` parameters. The default value for the `--pcapfile` parameter is `ecapture_openssl.pcapng`.
  - `keylog` mode: Set with `-m keylog` or `-m key` parameters. When using this mode, it is necessary to specify `--keylogfile`, defaulting to `ecapture_masterkey.log`.
  - `text` mode: Default mode when `-m` parameter is unspecified. Outputs all plaintext packets in text form. (As of v0.7.0, no longer captures communication keys, please use `keylog` mode instead.)
- Refactor the mode parameters supported by the `gotls` module, similar to the `openssl` module, without further details.
- Optimize the memory size of eBPF Map, specify with the `--mapsize` parameter, defaulting to 5120 KB.
- Remove the `-w` parameter, use `--pcapfile` parameter instead.
- Change `log-addr` parameter to `logaddr`, with unchanged functionality.