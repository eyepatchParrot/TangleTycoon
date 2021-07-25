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
