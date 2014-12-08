#
# Conditional build:
%bcond_with	tests		# build without tests
%bcond_without	doc			# don't build ri/rdoc

%define pkgname haml
Summary:	An elegant, structured XHTML/XML templating engine
Name:		ruby-%{pkgname}
Version:	4.0.5
Release:	2
License:	MIT and WTFPL
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	60c17bbec24a4c8e44568380c96f60ad
URL:		http://haml-lang.com/
# from https://github.com/haml/haml/commit/5017d332604a9b77b19401f6d2bcbef6479c3210
# slightly modified to apply against current release
Patch0:		5017d332-Add-Haml-TestCase.patch
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
%if %{with tests}
BuildRequires:	rubygem(erubis)
BuildRequires:	rubygem(minitest)
BuildRequires:	rubygem(nokogiri)
BuildRequires:	rubygem(rails)
BuildRequires:	rubygem(sass)
BuildRequires:	rubygems-devel
%endif
Requires:	rubygem(erubis)
Requires:	rubygem(sass)
Requires:	rubygem(tilt)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Haml (HTML Abstraction Markup Language) is a layer on top of XHTML or
XML that's designed to express the structure of XHTML or XML documents
in a non-repetitive, elegant, easy way, using indentation rather than
closing tags and allowing Ruby to be embedded with ease. It was
originally envisioned as a plugin for Ruby on Rails, but it can
function as a stand-alone templating engine.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
ruby -Ilib:test test/*_test.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc MIT-LICENSE CHANGELOG.md FAQ.md REFERENCE.md README.md
%attr(755,root,root) %{_bindir}/haml
%{ruby_vendorlibdir}/haml.rb
%{ruby_vendorlibdir}/haml
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
