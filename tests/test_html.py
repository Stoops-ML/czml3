import html
import re

from czml3 import CZML_VERSION, Document, Packet

DOC = Document(
    packets=[
        Packet(id="document", name="My <scene>", version=CZML_VERSION),
        Packet(id="a", description="<b>bold</b></script><script>alert(1)</script>"),
    ]
)


def test_to_html_loads_requested_cesium_version():
    page = DOC.to_html(cesium_version="1.125")
    assert "cesiumjs/releases/1.125/Build/Cesium/Cesium.js" in page
    assert "<title>My &lt;scene&gt;</title>" in page


def test_to_html_cannot_break_out_of_the_script_element():
    page = DOC.to_html()
    script = re.search(r"<script>\n(.*?)</script>", page, re.DOTALL)
    assert script is not None
    assert "alert(1)" in script.group(1)
    assert page.count("</script>") == 2  # Cesium.js tag and the inline script


def test_ion_token_is_embedded_only_when_given():
    assert 'const ionToken = "";' in DOC.to_html()
    assert 'const ionToken = "abc";' in DOC.to_html(ion_token="abc")


def test_repr_html_embeds_page_in_sandboxed_iframe():
    frame = DOC._repr_html_()
    assert frame.startswith("<iframe srcdoc=")
    assert 'sandbox="allow-scripts"' in frame
    assert html.escape(DOC.to_html(), quote=True) in frame


def test_save_html(tmp_path):
    path = tmp_path / "scene.html"
    DOC.save_html(path, cesium_version="1.125")
    assert path.read_text(encoding="utf-8") == DOC.to_html(cesium_version="1.125")


def test_default_cesium_version_is_used():
    from czml3._html import DEFAULT_CESIUM_VERSION

    assert DEFAULT_CESIUM_VERSION == "1.145"
    assert f"releases/{DEFAULT_CESIUM_VERSION}/Build/Cesium/" in DOC.to_html()
