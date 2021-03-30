from conans import ConanFile, CMake
import os

channel = "stable"
username = "zyq"

class VTKReuseConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "VTK/8.0.1@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        print("cd: " + self.source_folder)
        self.run('cmake . %s %s' % (self.source_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        self.run("cd bin && .%smyvtk" % os.sep)
