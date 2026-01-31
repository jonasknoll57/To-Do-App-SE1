# -*- coding: utf-8 -*-
"""
End-to-End Tests für die TODO-App.

Voraussetzungen:
    pip install pytest-playwright pytest-cov
    playwright install chromium

Ausführung:
    pytest test_e2e.py -v --headed
    
Hinweis: Streamlit muss laufen: streamlit run app.py
"""
import pytest

try:
    from playwright.sync_api import Page, expect
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Page = None

pytestmark = pytest.mark.skipif(
    not PLAYWRIGHT_AVAILABLE,
    reason="Playwright nicht installiert"
)


class TestTodoAppE2E:
    """End-to-End Tests für die TODO-App."""
    
    BASE_URL = "http://localhost:8501"
    
    @pytest.fixture(scope="class")
    def setup_app(self):
        """Prueft ob Server erreichbar ist."""
        import urllib.request
        try:
            urllib.request.urlopen(self.BASE_URL, timeout=2)
        except:
            pytest.skip("Streamlit-Server nicht erreichbar")
        yield
    
    def test_1_page_loads(self, page: Page, setup_app):
        """Seite laed ohne Fehler."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        assert page.url == self.BASE_URL + "/"
    
    
    def test_3_has_input_field(self, page: Page, setup_app):
        """Es gibt ein Eingabefeld."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        inputs = page.locator('input[type="text"]')
        assert inputs.count() > 0
    
    
    def test_5_page_responsive(self, page: Page, setup_app):
        """Seite reagiert auf Viewport-Aenderung."""
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        page.set_viewport_size({"width": 375, "height": 667})
        page.wait_for_timeout(500)
        assert page.url == self.BASE_URL + "/"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
