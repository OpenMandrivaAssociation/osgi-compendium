Name:		osgi-compendium
Version:	6.0.0
Release:	4.1
Summary:	OSGi Compendium API
Group:		Development/Java
License:	ASL 2.0
URL:		https://www.osgi.org/
# Sources jar. The previous lookaside was the binary cmpn jar.
Source0:	https://repo1.maven.org/maven2/org/osgi/osgi.cmpn/%{version}/osgi.cmpn-%{version}-sources.jar
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	osgi-core
BuildRequires:	mvn(org.osgi:org.osgi.annotation.versioning)
BuildRequires:	mvn(javax.servlet:javax.servlet-api)
BuildSystem:	maven
BuildOption(install):	--file-name %{name} --alias org.osgi:org.osgi.compendium

%description
OSGi Compendium Release 6 service interfaces. The J2ME Connector Service
and the JPA EntityManager factory are left out: nothing in cooker
provides javax.microedition or javax.persistence, and no package here
imports those classes.

%prep
%setup -q -c -T
# The builders' rpmuncompress passes a sources jar to tar.
python - %{SOURCE0} <<'PY'
import sys
import zipfile
zipfile.ZipFile(sys.argv[1]).extractall(".")
PY
mkdir -p src/main/java
mv org src/main/java/
# Connector Service is J2ME. The JPA helper needs javax.persistence.
rm -rf src/main/java/org/osgi/service/io src/main/java/org/osgi/service/jpa
python - %{version} <<'PY'
import sys
from pathlib import Path
version = sys.argv[1]
Path("pom.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.osgi</groupId>
  <artifactId>osgi.cmpn</artifactId>
  <version>{version}</version>
  <packaging>jar</packaging>
  <name>OSGi Compendium</name>
  <dependencies>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>osgi.core</artifactId>
      <version>{version}</version>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>org.osgi</groupId>
      <artifactId>org.osgi.annotation.versioning</artifactId>
      <scope>provided</scope>
    </dependency>
    <dependency>
      <groupId>javax.servlet</groupId>
      <artifactId>javax.servlet-api</artifactId>
      <scope>provided</scope>
    </dependency>
  </dependencies>
</project>
""")
PY

%files -f .mfiles
%doc LICENSE about.html
