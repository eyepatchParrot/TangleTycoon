def tangle_tycoon(name, srcs, streams):
    native.genrule(
        name = name,
        cmd = "cat $(SRCS) | $(location :tangletycoon.py) " + " ".join([
            "--{} $(location :{})".format(stream, out)
            for stream, out in streams.items()
        ]),
        srcs = srcs,
        tools = ["tangletycoon.py"],
        outs = streams.values(),
    )
