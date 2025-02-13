import aqt
from aqt.qt import QWizard, Qt

from . import util
from . import config
from .settings_widgets import TUTORIAL_WIDGETS

class WelcomeWizard(QWizard):
    INITIAL_SIZE = (625, 440)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)

        self.setWindowTitle("Welcome! - Migaku Anki")
        self.setWindowIcon(util.default_icon())

        self.setMinimumSize(*self.INITIAL_SIZE)
        self.resize(*self.INITIAL_SIZE)

        self.pages = []
        for wcls in TUTORIAL_WIDGETS:
            page = wcls.wizard_page()
            self.addPage(page)
            self.pages.append(page)

        self.finished.connect(self.save)

    def save(self):
        for page in self.pages:
            page.save()
        config.set("first_run", False, do_write=True)

    @classmethod
    def check_show_modal(cls):
        if (
            config.get("first_run", True)
            or aqt.mw.app.queryKeyboardModifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            wizard = cls()
            return wizard.exec()


aqt.gui_hooks.profile_did_open.append(WelcomeWizard.check_show_modal)
