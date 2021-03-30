import os
from conans import ConanFile, CMake, tools
from conans.tools import SystemPackageTool

class VTKConan(ConanFile):
    name = "VTK"
    description = "Visualization Toolkit by Kitware"
    version = "8.0.1"
    version_split = version.split('.')
    short_version = "%s.%s" % (version_split[0], version_split[1])
    SHORT_VERSION = short_version
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    url = "https://github.com/zyq759316417/conan-vtk"
    options = {
        "shared": [True, False], 
        "qt": [True, False], 
        "mpi": [True, False], 
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True, 
        "qt": False, 
        "mpi": False, 
        "fPIC": False
    }
    exports = ["CMakeLists.txt", "FindVTK.cmake"]
    license="http://www.vtk.org/licensing/"
    short_paths=True
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        if self.options.qt == True:
            # conan-transit / Qt:osechet
            self.requires("Qt/5.6.1-1@osechet/testing")

    def system_requirements(self):
        pack_names = None
        if tools.os_info.linux_distro == "ubuntu":
            pack_names = [
                "freeglut3-dev",
                "mesa-common-dev",
                "mesa-utils-extra",
                "libgl1-mesa-dev",
                "libglapi-mesa"]
            print("names: " + str(pack_names))

            if self.settings.arch == "x86":
                full_pack_names = []
                for pack_name in pack_names:
                    full_pack_names += [pack_name + ":i386"]
                pack_names = full_pack_names


        installer = SystemPackageTool()
        # installer.update() # Update the package database
        to_be_installed = ""
        for pkg in pack_names:
            if not installer.installed(pkg):
                to_be_installed += " " + pkg
        if to_be_installed:
            print("pkg will be installed: " + to_be_installed)
            installer.install(to_be_installed)

    def config_options(self):
        # First configuration step. Only settings are defined. Options can be removed
        # according to these settings
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake is not None:
            return self._cmake
        self._cmake = CMake(self)

        self._cmake.definitions["BUILD_TESTING"] = "OFF"
        self._cmake.definitions["BUILD_EXAMPLES"] = "OFF"

        if self.options.shared == False:
            self._cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
        if self.options.qt == True:
            self._cmake.definitions["VTK_Group_Qt"] = "ON"
            self._cmake.definitions["VTK_QT_VERSION"] = "5"
            self._cmake.definitions["VTK_BUILD_QT_DESIGNER_PLUGIN"] = "OFF"
        if self.options.mpi == True:
            self._cmake.definitions["VTK_Group_MPI"] = "ON"

        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            self._cmake.definitions["CMAKE_DEBUG_POSTFIX"] = "_d"

        if self.settings.compiler != "Visual Studio":
            if not self.options.shared:
                if self.options.fPIC:
                    self._cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON"

        self._cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()
        # tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))


    def package_info(self):
        LIB_POSTFIX = ""
        if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
            LIB_POSTFIX = "_d"
        libs = [
            "vtkalglib-%s" % self.short_version + LIB_POSTFIX,
            "vtkChartsCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonColor-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonComputationalGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonDataModel-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonExecutionModel-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonMath-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonMisc-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonSystem-%s" % self.short_version + LIB_POSTFIX,
            "vtkCommonTransforms-%s" % self.short_version + LIB_POSTFIX,
            "vtkDICOMParser-%s" % self.short_version + LIB_POSTFIX,
            "vtkDomainsChemistry-%s" % self.short_version + LIB_POSTFIX,
            "vtkDomainsChemistryOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkexoIIc-%s" % self.short_version + LIB_POSTFIX,
            "vtkexpat-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersAMR-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersExtraction-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersFlowPaths-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeneral-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeneric-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersHybrid-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersHyperTree-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersImaging-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersModeling-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersParallel-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersParallelImaging-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersPoints-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersProgrammable-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersSelection-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersSMP-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersSources-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersStatistics-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersTexture-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersTopology-%s" % self.short_version + LIB_POSTFIX,
            "vtkFiltersVerdict-%s" % self.short_version + LIB_POSTFIX,
            "vtkfreetype-%s" % self.short_version + LIB_POSTFIX,
            "vtkGeovisCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkgl2ps-%s" % self.short_version + LIB_POSTFIX,
            "vtkglew-%s" % self.short_version + LIB_POSTFIX,
            "vtkhdf5_hl-%s" % self.short_version + LIB_POSTFIX,
            "vtkhdf5-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingColor-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingFourier-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingGeneral-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingHybrid-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingMath-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingMorphological-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingSources-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingStatistics-%s" % self.short_version + LIB_POSTFIX,
            "vtkImagingStencil-%s" % self.short_version + LIB_POSTFIX,
            "vtkInfovisCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkInfovisLayout-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionStyle-%s" % self.short_version + LIB_POSTFIX,
            "vtkInteractionWidgets-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOAMR-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOEnSight-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOExodus-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOExport-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOExportOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOGeometry-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOImport-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOInfovis-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOLegacy-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOLSDyna-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOMINC-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOMovie-%s" % self.short_version + LIB_POSTFIX,
            "vtkIONetCDF-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOParallel-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOParallelXML-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOPLY-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOSQL-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOTecplotTable-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOVideo-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOXML-%s" % self.short_version + LIB_POSTFIX,
            "vtkIOXMLParser-%s" % self.short_version + LIB_POSTFIX,
            "vtkjpeg-%s" % self.short_version + LIB_POSTFIX,
            "vtkjsoncpp-%s" % self.short_version + LIB_POSTFIX,
            "vtklibharu-%s" % self.short_version + LIB_POSTFIX,
            "vtklibxml2-%s" % self.short_version + LIB_POSTFIX,
            "vtklz4-%s" % self.short_version + LIB_POSTFIX,
            "vtkmetaio-%s" % self.short_version + LIB_POSTFIX,
            "vtkNetCDF-%s" % self.short_version + LIB_POSTFIX,
            "vtknetcdf_c++" + LIB_POSTFIX,
            "vtkoggtheora-%s" % self.short_version + LIB_POSTFIX,
            "vtkParallelCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkpng-%s" % self.short_version + LIB_POSTFIX,
            "vtkproj4-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingAnnotation-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingContext2D-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingContextOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingFreeType-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingGL2PSOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingImage-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingLabel-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingLOD-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingVolume-%s" % self.short_version + LIB_POSTFIX,
            "vtkRenderingVolumeOpenGL2-%s" % self.short_version + LIB_POSTFIX,
            "vtksqlite-%s" % self.short_version + LIB_POSTFIX,
            "vtksys-%s" % self.short_version + LIB_POSTFIX,
            "vtktiff-%s" % self.short_version + LIB_POSTFIX,
            "vtkverdict-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsContext2D-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsCore-%s" % self.short_version + LIB_POSTFIX,
            "vtkViewsInfovis-%s" % self.short_version + LIB_POSTFIX,
            "vtkzlib-%s" % self.short_version + LIB_POSTFIX,
        ]
        if self.options.qt:
            libs.append("vtkGUISupportQt-%s" % self.short_version + LIB_POSTFIX)
            libs.append("vtkGUISupportQtSQL-%s" % self.short_version + LIB_POSTFIX)
        if self.options.mpi:
            libs.append("vtkParallelCore-%s" % self.short_version + LIB_POSTFIX)
            libs.append("vtkParallelMPI-%s" % self.short_version + LIB_POSTFIX)
            libs.append("vtkIOParallel-%s" % self.short_version + LIB_POSTFIX)
            libs.append("vtkIOParallelXML-%s" % self.short_version + LIB_POSTFIX)
            libs.append("vtkIOParallelNetCDF-%s" % self.short_version + LIB_POSTFIX)
            # vtkFiltersParallelDIY2;vtkFiltersParallelGeometry;vtkFiltersParallelMPI;vtkIOMPIImage;vtkIOMPIParallel;vtkIOParallelNetCDF;vtkParallelMPI;vtkdiy2
        self.cpp_info.libs = libs
        self.cpp_info.includedirs = [
            "include/vtk-%s" % self.short_version,
            "include/vtk-%s/vtknetcdf/include" % self.short_version,
            "include/vtk-%s/vtknetcdfcpp" % self.short_version
        ]
