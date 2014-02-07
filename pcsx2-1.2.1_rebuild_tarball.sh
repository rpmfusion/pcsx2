
#!/bin/sh
#This is a Modification of a script by Gregory Hainaut
#Purpose is to strip any copyrighted etc. material
#from the publicly available tarball so make suitable for linux distribution

mkdir ~/pcsx2-1.2.1
cd ~/pcsx2-1.2.1
wget https://github.com/PCSX2/pcsx2/archive/v1.2.1.tar.gz
tar xvfz v1.2.1.tar.gz
rm v1.2.1.tar.gz
 
mkdir -p temporary_pcsx2;
(   cp pcsx2-1.2.1/CMakeLists.txt temporary_pcsx2/CMakeLists.txt;
    cp -r pcsx2-1.2.1/common temporary_pcsx2/common;
    cp -r pcsx2-1.2.1/cmake temporary_pcsx2/cmake;
    cp -r pcsx2-1.2.1/locales temporary_pcsx2/locales;
    cp -r pcsx2-1.2.1/pcsx2 temporary_pcsx2/pcsx2;
    cp -r pcsx2-1.2.1/debian-unstable-upstream temporary_pcsx2/debian-unstable-upstream;
    cp -r pcsx2-1.2.1/linux_various temporary_pcsx2/linux_various;)

# separate bin to avoid retaining the .mo file
mkdir -p temporary_pcsx2/bin;
(   cp pcsx2-1.2.1/bin/GameIndex.dbf temporary_pcsx2/bin/GameIndex.dbf;
    cp pcsx2-1.2.1/bin/cheats_ws.zip temporary_pcsx2/bin/cheats_ws.zip;
    cp -r pcsx2-1.2.1/bin/cheats temporary_pcsx2/bin/cheats;
    cp -r pcsx2-1.2.1/bin/docs temporary_pcsx2/bin/docs;)

# Note: Other plugins exist but they are not 100% copyright free, so remove them.
# Note: some plugins are more or less deprecated CDVDisoEFP, CDVDlinuz, Zerogs, Zeropad ...";
mkdir -p temporary_pcsx2/plugins;
(   cp pcsx2-1.2.1/plugins/CMakeLists.txt temporary_pcsx2/plugins/CMakeLists.txt;
    cp -r pcsx2-1.2.1/plugins/CDVDnull temporary_pcsx2/plugins/CDVDnull;
    # Potential copyright issue. Optional anyway
    cp -r pcsx2-1.2.1/plugins/onepad temporary_pcsx2/plugins/onepad;
    cp -r pcsx2-1.2.1/plugins/spu2-x temporary_pcsx2/plugins/spu2-x;
    cp -r pcsx2-1.2.1/plugins/zzogl-pg temporary_pcsx2/plugins/zzogl-pg;
    cp -r pcsx2-1.2.1/plugins/zzogl-pg-cg temporary_pcsx2/plugins/zzogl-pg-cg;
    cp -r pcsx2-1.2.1/plugins/GSdx temporary_pcsx2/plugins/GSdx;
    cp -r pcsx2-1.2.1/plugins/dev9null temporary_pcsx2/plugins/dev9null;
    cp -r pcsx2-1.2.1/plugins/FWnull temporary_pcsx2/plugins/FWnull;
    cp -r pcsx2-1.2.1/plugins/USBnull temporary_pcsx2/plugins/USBnull;)


## Installation
# Copy the dir
rm -fr pcsx2-1.2.1
cp -r temporary_pcsx2 pcsx2-1.2.1

echo "Remove .svn directories"
find pcsx2-1.2.1 -name ".svn" -type d -exec rm -fr {} \; 2> /dev/null
echo "Remove windows files (useless & potential copyright issues)"
# => pcsx2/windows
# Copyright header must be updated
find pcsx2-1.2.1 -iname "windows" -type d -exec rm -fr {} \; 2> /dev/null
# => ./plugins/zzogl-pg*/opengl/Win32 (reduced to the current linux plugins)
find pcsx2-1.2.1 -name "Win32" -type d -exec rm -fr {} \; 2> /dev/null

echo "Remove useless files (copyright issues)"
rm -fr "pcsx2-1.2.1/plugins/zzogl-pg/opengl/ZeroGSShaders"
rm -fr "pcsx2-1.2.1/common/src/Utilities/x86/MemcpyFast.cpp"
rm -fr "pcsx2-1.2.1/plugins/GSdx/baseclasses"

## BUILD
echo "Build the tar.gz file"
tar -czf v1.2.1.tar.gz pcsx2-1.2.1

## Clean
rm -fr pcsx2-1.2.1
rm -fr temporary_pcsx2

