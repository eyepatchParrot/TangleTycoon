load(":rules.bzl", "tangle_tycoon")
tangle_tycoon(
    name = "hello_world",
    srcs = ["hello-world.md"],
    streams = {
        "cpp": "default.cpp",
        "header": "foo.h",
        "impl": "foo.cpp",
        "python": "foo.py",
        "text": "out.txt",
    })

cc_binary(
    name = "TangleTycoon",
    srcs = [":default.cpp", ":foo.cpp", ":foo.h"],
    data = [":hello_world"],
)

py_test(
    name = "test",
    srcs = [":test.py", ":tangletycoon.py"],
)

tangle_tycoon(
    name = "README",
    srcs = ["README.md"],
    streams = {
        "foo.cpp": "bar.cpp",
        "cpp": "main.cpp",
        "lib": "lib.py",
        "test": "test.py",
        "sh": "README.sh",
    })

sh_test(
    name="example-run",
    srcs=["README.sh"],
    args=["$(location README.md)", "$(location :tangletycoon.py)"],
    data=["README.md", "tangletycoon.py"],
)
