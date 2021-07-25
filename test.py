from textwrap import dedent
from collections import namedtuple
import pytest

import tangletycoon as tt


def test_code_blocks():
    text = dedent(r"""
        ```cpp
        #include "foo.h"
        ```

        ```cpp stream=header
        void hello_world();
        ```

        ```cpp stream=impl name=impl-body dep=impl-def
            std::cout << "Hello world\n";
        }
        ```

        ```cpp stream=impl name=impl-inc
        #include "foo.h"
        #include <iostream>
        ```

        ```cpp stream=impl name=impl-def dep=impl-inc
        void hello_world() {
        ```

        ```
        ```
        """)
    result = list(tt.code_blocks(text))
    assert ([{
        "stream": block["stream"],
        "name": block["name"] if not isinstance(block["name"], int) else "",
        "dep": block["dep"],
        "content": block["content"],
    } for block in result] == [{
        "stream": "cpp",
        "name": "",
        "dep": [],
        "content": '#include "foo.h"\n'
    }, {
        "stream": "header",
        "name": "",
        "dep": [],
        "content": 'void hello_world();\n'
    }, {
        "stream": "impl",
        "name": "impl-body",
        "dep": ["impl-def"],
        "content": dedent(r"""
                std::cout << "Hello world\n";
            }
            """[1:])
    }, {
        "stream": "impl",
        "name": "impl-inc",
        "dep": [],
        "content": dedent("""
            #include "foo.h"
            #include <iostream>
            """[1:])
    }, {
        "stream": "impl",
        "name": "impl-def",
        "dep": ["impl-inc"],
        "content": "void hello_world() {\n"
    }, {
        "stream": "text",
        "name": "",
        "dep": [],
        "content": ''
    }])


def test_blocks_order():
    blocks = [{"dep": ["a"], "name": 0}, {"name": "a", "dep": []}]
    assert [1, 0] == tt.blocks_order(blocks)

    blocks = [{"dep": [], "name": 0}]
    assert [0] == tt.blocks_order(blocks)
    blocks.append({"name": 1, "dep": []})
    assert [0, 1] == tt.blocks_order(blocks)
    blocks.append({
        "name": "impl-body",
        "dep": ["impl-def"],
    })
    with pytest.raises(AssertionError):
        tt.blocks_order(blocks)
    blocks.append({
        "name": "impl-inc",
        "dep": [],
    })
    with pytest.raises(AssertionError):
        tt.blocks_order(blocks)
    blocks.append({
        "name": "impl-def",
        "dep": ["impl-inc"],
    })
    assert [0, 1, 3, 4, 2] == tt.blocks_order(blocks)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
