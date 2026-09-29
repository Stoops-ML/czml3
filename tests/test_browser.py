"""Render the HTML preview in headless Chrome and check the viewer comes up.

The page loads CesiumJS from cesium.com and imagery from OpenStreetMap, so
these tests need a Chrome/Chromium/Edge binary and internet access; they are
skipped otherwise. Set CZML3_BROWSER to the browser executable to choose one.

Pages are served over a local HTTP server, as Jupyter and web servers serve
them. Opened from ``file://``, browsers block Cesium's web workers, which is
recorded as an expected failure below.
"""

import functools
import http.server
import os
import re
import shutil
import socket
import subprocess
import threading
from collections.abc import Iterator
from pathlib import Path

import pytest

from czml3 import CZML_VERSION, Document, Packet, Point, Polyline, Position
from czml3.properties import PositionList

_CANDIDATES = [
    os.environ.get("CZML3_BROWSER"),
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
    shutil.which("chrome"),
    shutil.which("msedge"),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
BROWSER = next((c for c in _CANDIDATES if c and Path(c).is_file()), None)


def _online(host: str = "cesium.com") -> bool:
    try:
        socket.create_connection((host, 443), timeout=5).close()
    except OSError:
        return False
    return True


pytestmark = [
    pytest.mark.browser,
    pytest.mark.skipif(BROWSER is None, reason="no Chrome/Chromium/Edge found"),
    pytest.mark.skipif(not _online(), reason="cesium.com is unreachable"),
]

DOC = Document(
    packets=[
        Packet(id="document", name="browser test", version=CZML_VERSION),
        Packet(
            id="a",
            position=Position(cartographicDegrees=[34.8, 32.1, 0]),
            point=Point(pixelSize=10),
        ),
        Packet(
            id="b",
            position=Position(cartographicDegrees=[35.2, 31.8, 0]),
            point=Point(pixelSize=10),
        ),
        Packet(
            id="link",
            polyline=Polyline(
                positions=PositionList(references=["a#position", "b#position"])
            ),
        ),
    ]
)
ENTITIES = 3  # the "document" packet configures the scene and is not an entity

# Reads the status the embedded viewer posts, so it can be checked from outside.
NOTEBOOK_TPL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin: 0">
{frame}
<script>
window.addEventListener("message", (event) => {{
    Object.assign(document.body.dataset, event.data.czml3 || {{}});
}});
</script>
</body></html>
"""


@pytest.fixture
def site(tmp_path: Path) -> Iterator[str]:
    """Serve ``tmp_path`` on localhost; yields the base URL."""
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(tmp_path)
    )
    handler.log_message = lambda *args: None  # type: ignore[attr-defined]
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()


def _render(url: str, profile: Path) -> str:
    """Load ``url`` in headless Chrome and return the DOM after scripts ran."""
    assert BROWSER is not None
    result = subprocess.run(
        [
            BROWSER,
            "--headless=new",
            "--no-first-run",
            "--disable-extensions",
            # Software WebGL, so no GPU is needed.
            "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader",
            f"--user-data-dir={profile}",
            "--virtual-time-budget=30000",
            "--dump-dom",
            url,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
        check=False,
    )
    assert result.returncode == 0, result.stderr[-2000:]
    return result.stdout


def _body_status(dom: str) -> dict[str, str]:
    """The data-czml3-* status the page recorded on <body>."""
    body = re.search(r"<body[^>]*>", dom)
    assert body is not None, dom[:2000]
    return dict(re.findall(r'data-czml3-(\w+)="([^"]*)"', body.group(0)))


def test_standalone_page_renders_the_document(tmp_path: Path, site: str) -> None:
    DOC.save_html(tmp_path / "scene.html")

    dom = _render(f"{site}/scene.html", tmp_path / "profile")

    assert _body_status(dom) == {"entities": str(ENTITIES)}
    assert 'class="cesium-widget' in dom
    assert re.search(r"<canvas[^>]+width=\"[1-9]", dom), "no sized WebGL canvas"
    assert "cesium-widget-errorPanel" not in dom


def test_jupyter_iframe_renders_the_document(tmp_path: Path, site: str) -> None:
    (tmp_path / "notebook.html").write_text(
        NOTEBOOK_TPL.format(frame=DOC._repr_html_()), encoding="utf-8"
    )

    dom = _render(f"{site}/notebook.html", tmp_path / "profile")

    assert _body_status(dom) == {"entities": str(ENTITIES)}


@pytest.mark.xfail(
    strict=True,
    reason="browsers block Cesium's web workers on file:// pages; serve the page over HTTP",
)
def test_standalone_page_opened_from_file(tmp_path: Path) -> None:
    page = tmp_path / "scene.html"
    DOC.save_html(page)

    dom = _render(page.resolve().as_uri(), tmp_path / "profile")

    assert _body_status(dom) == {"entities": str(ENTITIES)}
