Summary:	SIFT Feature Detection implementation
Summary(pl.UTF-8):	Implementacja algorytmu SIFT do wykrywania cech obrazu
Name:		autopano-sift-C
Version:	2.5.1
Release:	2
License:	GPL v2, but SIFT algorithm may require license in some countries
Group:		Applications/Graphics
Source0:	http://downloads.sourceforge.net/hugin/%{name}-%{version}.tar.gz
# Source0-md5:	b9bade07e8c4f2ea383c22a082c260e0
Patch0:		link.patch
URL:		http://wiki.panotools.org/Autopano-sift-C
BuildRequires:	cmake >= 2.4
BuildRequires:	libjpeg-devel
BuildRequires:	libpano13-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.471
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SIFT algorithm provides the capability to identify key feature
points within arbitrary images. It further extracts highly distinct
information for each such point and allows to characterize the point
invariant to a number of modifications to the image. It is invariant
to contrast/brightness changes, to rotation, scaling and partially
invariant to other kinds of transformations. The algorithm can be
flexibly used to create input data for image matching, object
identification and other computer vision related algorithms.

autopano-sift-C is a C port of the C# software autopano-sift. It is
somewhat faster and doesn't require a C# runtime. Additionally,
autopano-sift-C has experimental modifications to perform feature
identification in conformal image space, this helps with wide angle or
fisheye Projection photographs.

%description -l pl.UTF-8
Algorytm SIFT daje możliwość określenia kluczowych punktów
charakterystycznych na dowolnych zdjęciach. Następnie wydobywa
informacje wyodrębniające dla każdego takiego punktu i pozwala
scharakteryzować ten punkt niezależnie od liczby modyfikacji obrazu.
Jest niezależny od zmian kontrastu/jasności, obrotów, skalowania i
częściowo niezależny od innych rodzajów przekształceń. Algorytm może
być elastycznie używany do tworzenia danych wejściowych do
dopasowywania obrazów, identyfikowania obiektów i innych algorytmów
związanych z grafiką komputerową.

autopano-sift-C to port C programu autopano-sift napisanego w C#.
Jest nieco szybszy i nie wymaga środowiska uruchomieniowego C#.
Ponadto zawiera nieco eksperymentalnych modyfikacji w celu
przeprowadzania identyfikacji punktów w wiernokątnej przestrzeni
obrazu, co pomaga przy zdjęciach obiektywami szerokokątnymi lub
"rybim okiem".

%prep
%setup -q 
%patch -P0 -p1

%build
install -d build
cd build
# CMAKE_AR is a hack, cmake is unable to find it otherwise :/
%cmake .. \
	-DCMAKE_AR=/usr/bin/ar \
	-DCMAKE_BUILD_TYPE=%{?debug:Debug}%{!?debug:Release} \
	-DCMAKE_C_FLAGS_RELEASE="-DNDEBUG" \
	-DCMAKE_CXX_FLAGS_RELEASE="-DNDEBUG" \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
%if "%{_lib}" == "lib64"
	-DLIB_SUFFIX=64
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# resolve conflict with autopano-sift
mv $RPM_BUILD_ROOT%{_mandir}/man1/autopano{,-c}.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/generatekeys{,-c}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README README.1ST
%attr(755,root,root) %{_bindir}/autopano
%attr(755,root,root) %{_bindir}/autopano-c-complete.sh
%attr(755,root,root) %{_bindir}/autopano-sift-c
%attr(755,root,root) %{_bindir}/generatekeys
%{_mandir}/man1/autopano-c.1*
%{_mandir}/man1/autopano-c-complete.1*
%{_mandir}/man1/generatekeys-c.1*
%{_mandir}/man7/autopano-sift-c.7*
