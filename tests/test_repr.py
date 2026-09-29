from czml3 import Packet, Point


def test_repr_shows_only_set_properties():
    assert repr(Packet(id="a", point=Point(pixelSize=5))) == (
        "Packet(id='a', point=Point(pixelSize=5.0))"
    )
