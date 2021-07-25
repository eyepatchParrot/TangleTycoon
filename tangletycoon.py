#!/usr/bin/env python3
from sys import stdin
import fire
from logging import error


def code_blocks(text):
    return (block(i, e) for i, e in enumerate(text.split("```")) if i % 2 == 1)


def block(seq, text):
    lines = text.split("\n")
    header = lines[0].split()
    block = {
        "stream": [],
        "name": [seq],
        "dep": [],
        "content": "\n".join(lines[1:]),
    }
    # Use lang as steam if the first argument isn't positional
    positional = ["stream", "name", "dep"]
    if len(header) > 0 and all(p not in header[0] for p in positional):
        block["stream"].append(header[0])
        header = header[1:]
    for h in header:
        k, v = h.split("=")
        block[k].append(v)
    if not block["stream"]:
        block["stream"] = ["text"]
    block["stream"] = block["stream"][-1]
    block["name"] = block["name"][-1]
    return block


def invert_multimap(kv):
    rv = {}
    for k, v in kv.items():
        for x in v:
            rv.setdefault(x, []).append(k)
    return rv


def blocks_order(blocks):
    """ TODO Iteration over diff should be sorted by sequence """
    rdeps = invert_multimap({block["name"]: block["dep"] for block in blocks})
    pushed = set()
    rindex = {block["name"]: i for i, block in enumerate(blocks)}
    order = []
    for i, seq_block in enumerate(blocks):
        diff = [seq_block]
        while diff:
            next_diff = []
            for block in diff:
                if any(dep not in pushed
                       for dep in block["dep"]) or block["name"] in pushed:
                    continue
                pushed.add(block["name"])
                order.append(rindex[block["name"]])
                next_diff.extend(blocks[rindex[dep]]
                                 for dep in rdeps.get(block["name"], []))
            diff = next_diff
    assert pushed == rindex.keys()
    return order


def tangle(force=False, **streams):
    stream_blocks = {}
    for block in code_blocks(stdin.read()):
        stream_blocks.setdefault(block["stream"], []).append(block)
    if not force:
        assert streams.keys() == stream_blocks.keys()
    for stream, blocks in stream_blocks.items():
        with open(streams[stream], "w") as f:
            f.write("".join(
                [blocks[i]["content"] for i in blocks_order(blocks)]))


if __name__ == '__main__':
    fire.Fire(tangle)

# Include both dependencies and reverse dependencies so that when a new
# snippet is encountered, you can identify all of the ones which have
# come before.  Each one should include a number indicating when it came
# in the file.
# lang stream name dep...
