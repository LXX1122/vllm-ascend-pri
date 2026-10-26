# SPDX-License-Identifier: Apache-2.0

import importlib.util
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def link_checker():
    path = Path(__file__).resolve().parents[3] / ".github/workflows/scripts/check_md_links.py"
    spec = importlib.util.spec_from_file_location("check_md_links", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("indent", ["", "    ", "        ", "\t"], ids=["root", "tab", "nested-list", "tab-char"])
@pytest.mark.parametrize("fence", ["```", "~~~"], ids=["backticks", "tildes"])
def test_extract_urls_skips_fenced_and_inline_code(link_checker, indent, fence):
    content = (
        "[Before](https://example.com/before)\n\n"
        f"{indent}{fence}shell\n"
        f"{indent}curl http://<SERVICE_IP>:8000\n"
        f"{indent}{fence}\n\n"
        f"{indent}Send requests to `http://<PREFILL_NODE_IP>:1999`.\n"
        f"{indent}[After](https://example.com/after)\n"
    )

    assert link_checker.extract_urls(content) == {
        "https://example.com/before",
        "https://example.com/after",
    }
