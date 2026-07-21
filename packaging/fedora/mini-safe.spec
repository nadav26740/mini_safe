Name:           mini-safe
Version:        1.0.0
Release:        1%{?dist}
Summary:        Password and data safe with CLI and TUI interfaces
License:        Apache-2.0
URL:            https://github.com/nadav26740/mini_safe
Source0:        mini_safe-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

BuildRequires:  python3-wheel

Requires:       python3-bcrypt
Requires:       python3-cryptography
Requires:       python3-pyperclip
Requires:       python3-rich
Requires:       python3-textual

# Ignore PyPI generated dependencies from dist-info
%global __requires_exclude ^python3\\.14dist\\(.*\\)

%description
A small Python utility for securely storing sensitive data with
password-based encryption. It provides both a command-line interface
and a terminal user interface.

%prep
%autosetup -n mini_safe-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{_bindir}/mini-safe-cli
%{_bindir}/mini-safe
%{python3_sitelib}/mini_safe-*.dist-info/
%pycached %{python3_sitelib}/CLI_Main.py
%pycached %{python3_sitelib}/TUI_main.py
%{python3_sitelib}/core/
%{python3_sitelib}/tui/

%changelog
* Tue Jul 21 2026 Nadav Mordechai <nadav@example.com> - 1.0.0-1
- Initial release