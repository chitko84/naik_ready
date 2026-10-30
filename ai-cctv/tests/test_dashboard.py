from pathlib import Path
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]
def test_dashboard():
    app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
    assert not app.exception
    app.select_slider[0].set_value('Car Blocking').run()
    assert not app.exception
    assert any('POTENTIAL OBSTRUCTION' in x.value for x in app.markdown)
def test_zone_config():
    app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
    app.sidebar.radio[0].set_value('Zone Configuration').run()
    assert not app.exception
    assert app.slider[0].value==10
    app.text_area[0].set_value('[[0,0],[0,0]]').run()
    assert app.error
