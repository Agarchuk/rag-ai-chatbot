from ui.ui_render import App
import atexit
from ui.utils.service_initializer import ServiceInitializer

atexit.register(ServiceInitializer().cleanup_db)

App().render()
