Name:           mini-safe
Version:        1.0.0
Release:        1%{?dist}
Summary:        Password and data safe with CLI and TUI interfaces
License:        Apache-2.0
URL:            https://github.com/nadav26740/mini_safe
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

%description
A small Python utility for securely storing sensitive data with
password-based encryption. It provides both a command-line interface
and a terminal user interface.

%prep
%autosetup -n %{name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install

%files
%license LICENSE
%doc README.md
%{_bindir}/mini-safe-cli
%{_bindir}/mini-safe-tui
%{python3_sitelib}/mini_safe-*.dist-info/
%{python3_sitelib}/CLI_Main.py*
%{python3_sitelib}/TUI_main.py*
%{python3_sitelib}/core/
%{python3_sitelib}/tui/
