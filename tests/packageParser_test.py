import pytest
from application.packageParser import parsePackages,findDependants

correctPackages = [
    "java-common",
    "libaspectj-java",
    "libbsf-java",
    "libplexus-sec-dispatcher-java",
    "libslf4j-java",
    "libtext-charwidth-perl",
    "libtext-wrapi18n-perl",
    "libws-commons-util-java",
    "python-pkg-resources",
    "tcpd"
]

@pytest.fixture
def parsedPackages():
    return parsePackages("testStatus")

def findCorrectPackage(parsedPackages,name):
    return  next(package for package in parsedPackages if
                                      package.name ==
                                      name)

def test_packagesAreSortedCorrectly(parsedPackages):
    temporaryCorrectPackages = correctPackages
    temporaryCorrectPackages.sort()
    print(temporaryCorrectPackages)
    assert(all([a == b.name for a, b in zip(temporaryCorrectPackages,
                                            parsedPackages)]))

def test_packagesHaveCorrectLength(parsedPackages):
    assert(len(correctPackages) == len(parsedPackages))

def test_packagewithnodepenciescontainsnodependencies(parsedPackages):
    testPackage = findCorrectPackage(parsedPackages, "libws-commons-util-java")
    testPackageDepencies = testPackage.dependencies
    assert(len(testPackageDepencies) == 0)

def test_packageContainsCorrectDependencies(parsedPackages):
    testPackage = findCorrectPackage(parsedPackages, "tcpd")
    testPackageDepencies = testPackage.dependencies
    correctDependencies = [
        "libc6",
        "libwrap0"
    ]

    assert(len(testPackageDepencies) == len(correctDependencies))
    assert(all(a == b for a,b in
               zip(correctDependencies, testPackageDepencies)))

def test_packageDependantsAreCorrect(parsedPackages):
    findDependants(parsedPackages)
    testPackage = findCorrectPackage(parsedPackages, "libtext-charwidth-perl")
    assert(testPackage.dependants[0] == "libtext-wrapi18n-perl")