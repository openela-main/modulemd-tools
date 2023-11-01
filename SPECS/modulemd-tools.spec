Name: modulemd-tools
Version: 0.7
Release: 6%{?dist}
Summary: Collection of tools for parsing and generating modulemd YAML files
License: MIT
BuildArch: noarch

URL: https://github.com/rpm-software-management/modulemd-tools
Source0: https://github.com/rpm-software-management/modulemd-tools/archive/%{version}/%{name}-%{version}.tar.gz
Patch0: modulemd-tools-0.7-1-to-modulemd-tools-0.7-6.patch

BuildRequires: createrepo_c
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-libmodulemd >= 2.9.3
BuildRequires: python3-dnf
BuildRequires: python3-hawkey
BuildRequires: python3-createrepo_c
BuildRequires: python3-pyyaml
BuildRequires: python3-pytest

Requires: createrepo_c
Requires: python3-dnf
Requires: python3-hawkey
Requires: python3-createrepo_c
Requires: python3-pyyaml
Requires: python3-libmodulemd >= 2.9.3


%description
Tools provided by this package:

repo2module - Takes a YUM repository on its input and creates modules.yaml
    containing YAML module definitions generated for each package.

dir2module - Generates a module YAML definition based on essential module
    information provided via command-line parameters. The packages provided by
    the module are found in a specified directory or a text file containing
    their list.

createrepo_mod - A small wrapper around createrepo_c and modifyrepo_c to provide
    an easy tool for generating module repositories.

modulemd-merge - Merge several modules.yaml files into one. This is useful for
    example if you have several yum repositories and want to merge them into one.

modulemd-generate-macros - Generate module-build-macros SRPM package, which is
    a central piece for building modules. It should be present in the buildroot
    before any other module packages are submitted to be built.

bld2repo - Simple tool for dowloading build required RPMs of a modular build from koji.


%prep
%setup -q
%patch0 -p1


%build
cd repo2module
%py3_build
cd ..

cd dir2module
%py3_build
cd ..

cd createrepo_mod
%py3_build
cd ..

cd modulemd-merge
%py3_build
cd ..

cd modulemd_tools
%py3_build
cd ..


%install
cd repo2module
%py3_install
cd ..

cd dir2module
%py3_install
cd ..

cd createrepo_mod
%py3_install
cd ..

cd modulemd-merge
%py3_install
cd ..

cd modulemd_tools
%py3_install
cd ..

cp modulemd-generate-macros/modulemd-generate-macros.py \
    %{buildroot}%{_bindir}/modulemd-generate-macros

install -d %{buildroot}%{_mandir}/man1
cp man/*.1 %{buildroot}%{_mandir}/man1/


%check
export PATH={buildroot}%{_bindir}:$PATH

cd repo2module
%{python3} -m pytest -vv
cd ..

cd dir2module
%{python3} -m pytest -vv
cd ..

cd createrepo_mod
%{python3} -m pytest -vv
cd ..

cd modulemd-merge
%{python3} -m pytest -vv -s
cd ..

cd modulemd_tools
%{python3} -m pytest -vv
cd ..


%files
%doc README.md
%license LICENSE
%{python3_sitelib}/repo2module
%{python3_sitelib}/repo2module-*.egg-info/
%{python3_sitelib}/dir2module
%{python3_sitelib}/dir2module-*.egg-info/
%{python3_sitelib}/createrepo_mod
%{python3_sitelib}/createrepo_mod-*.egg-info/
%{python3_sitelib}/modulemd_merge
%{python3_sitelib}/modulemd_merge-*.egg-info/
%{python3_sitelib}/modulemd_tools
%{python3_sitelib}/modulemd_tools-*.egg-info/
%{_bindir}/repo2module
%{_bindir}/dir2module
%{_bindir}/createrepo_mod
%{_bindir}/modulemd-merge
%{_bindir}/modulemd-generate-macros

%{_mandir}/man1/repo2module.1*
%{_mandir}/man1/dir2module.1*
%{_mandir}/man1/createrepo_mod.1*
%{_mandir}/man1/modulemd-merge.1*
%{_mandir}/man1/modulemd-generate-macros.1.*
%{_mandir}/man1/bld2repo.1.*


%changelog
* Fri Aug 27 2021 Jakub Kadlcik <jkadlcik@redhat.com> 0.7-6
- Do not install bld2repo as RHEL8 doesn't have python3-koji
  (jkadlcik@redhat.com)
- Drop the Patch1 and make the change directly in this repository
  (jkadlcik@redhat.com)
- Use UpstreamBuilder instead of DistributionBuilder (jkadlcik@redhat.com)
- Skip some tests because they require binary files (jkadlcik@redhat.com)

* Thu Aug 26 2021 Jakub Kadlcik <jkadlcik@redhat.com> 0.7-5
- Update to new upstream version

* Mon Aug 23 2021 Jakub Kadlcik <frostyx@email.cz> 0.11-1
- modulemd_tools: compatibility for upgrade_ext on EPEL8 (frostyx@email.cz)
- modulemd_tools: compatibility for read_packager_string on EPEL8
  (frostyx@email.cz)
- dir2module: generate also profiles and modulemd-defaults file
  (frostyx@email.cz)
- modulemd_tools: use upgrade_ext instead of upgrade (frostyx@email.cz)
- modulemd_tools: use read_packager_string instead of read_string
  (frostyx@email.cz)
- Add installation instructions (frostyx@email.cz)
- bld2repo: do not create empty repos when --result-dir is used
  (kdudka@redhat.com)
- bld2repo: print status in a more intuitive format (kdudka@redhat.com)
- tito: stop releasing for Fedora 32 (frostyx@email.cz)

* Mon Jun 14 2021 Jakub Kadlcik <frostyx@email.cz> 0.10-1
- Added bld2repo (mcurlej@redhat.com)

* Fri Apr 09 2021 Jakub Kadlcik <frostyx@email.cz> 0.9-1
- repo2module: drop python-click dependency (frostyx@email.cz)

* Tue Apr 06 2021 Jakub Kadlcik <frostyx@email.cz> 0.8-1
- modulemd_tools: drop python3-parameterized dependency (frostyx@email.cz)
- Package modulemd_tools helper lib (fvalder@redhat.com)
- Add modulemd-merge tests (fvalder@redhat.com)
- Add createrepo_mod tests (fvalder@redhat.com)
- Replace master in fedora releaser to rawhide (frostyx@email.cz)

* Tue Mar 02 2021 Jakub Kadlčík <jkadlcik@redhat.com> - 0.7-4
- Rebuild for 8.5.0

* Thu Feb 11 2021 Jakub Kadlčík <jkadlcik@redhat.com> - 0.7-3
- Bump spec to rebuild with gating enabled

* Tue Feb 09 2021 Jakub Kadlčík <jkadlcik@redhat.com> - 0.7-2
- Do not generate manpages on the fly
- Drop python-parameterized dependency
- Fix python3 macro for running tests

* Tue Feb 09 2021 Jakub Kadlcik <frostyx@email.cz> 0.7-1
- Generate manpages on the fly
- Automated test builds incl. Docker/Travis
- Fix PEP8 in all tools
- modulemd_tools: temporarily skip some tests on EPEL8 or Fedora
- Drop libmodulemd dependency in favor of python3-libmodulemd

* Sun Nov 22 2020 Jakub Kadlcik <frostyx@email.cz> 0.6-1
- Generate manpages for all tools in this repository
- modulemd-generate-macros: add a tool for generating module-build-macros
- modulemd_tools: add the first pieces of a python library (for internal usage only)

* Thu Nov 05 2020 Jakub Kadlcik <frostyx@email.cz> 0.5-1
- Release for epel8 as well (frostyx@email.cz)
- Require createrepo_c for the createrepo_mod package (frostyx@email.cz)
- modulemd-merge: improve README.md file (frostyx@email.cz)
- repo2module: improve README.md file (frostyx@email.cz)
- dir2module: improve README.md file (frostyx@email.cz)
- Improve README.md file (frostyx@email.cz)
- createrepo_mod: improve README.md file (frostyx@email.cz)
- Loosen the python3-libmodulemd dependency to just libmodulemd
  (frostyx@email.cz)
- createrepo_mod: use just createrepo_c if it has built-in module support
  (frostyx@email.cz)
- Explicitly depend on python3-setuptools (frostyx@email.cz)
- createrepo_mod: dump modules.yaml into the correct directory
  (frostyx@email.cz)

* Mon Aug 10 2020 Jakub Kadlcik <frostyx@email.cz> 0.4-1
- createrepo_mod: support also non-module repositories (frostyx@email.cz)

* Wed Jul 29 2020 Jakub Kadlcik <frostyx@email.cz> 0.3-1
- Add createrepo_mod and modulemd-merge scripts

* Sun Jul 26 2020 Jakub Kadlčík <jkadlcik@redhat.com> - 0.2-1
- Add createrepo_mod tool
- Add modulemd-merge tool
- Drop Source1, it is not needed anymore

* Tue Jun 09 2020 Jakub Kadlčík <jkadlcik@redhat.com> - 0.1-1
- Initial package
