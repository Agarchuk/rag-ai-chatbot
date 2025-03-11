from ui.components.chat.attach_library_document import AttachLibraryDocument
from ui.components.sidebar.base_sidebar import BaseSidebar
from ui.components.chat.rag.chat_documents import ChatDocuments
from ui.components.sidebar.model_settings import ModelSettingsUI
from ui.components.sidebar.new_chat_button import NewChatButton
from ui.components.sidebar.system_prompt import SystemPrompt


class RagChatSidebar(BaseSidebar):
    def __init__(self):
        super().__init__()

        self.add_component(NewChatButton())
        self.add_component(AttachLibraryDocument())
        self.add_component(ChatDocuments())
        self.add_component(ModelSettingsUI())
        self.add_component(SystemPrompt())

