from backend.facades.chat_facade import ChatFacade
import streamlit as st
from ui.utils.session_config import SessionConfig
from ui.utils.session_state_service import SessionStateService
from utils.logger import log_info, log_error

class AssistantResponse:
    def __init__(self):
        try:
            self.chat_facade: ChatFacade = SessionStateService().get_or_create_chat_facade()
        except ValueError as e:
            log_error(f"Error creating model service", e)
            st.error(str(e))
            st.stop()
        
    def stream_response(self):
        chat_id = SessionStateService().get(SessionConfig.CHAT_ID)
        user_id = SessionStateService().get(SessionConfig.USER_ID)

        log_info(f"Streaming response for chat: {chat_id}, user_id: {user_id}")

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # collection_name = SessionStateService().get(SessionConfig.COLLECTION_NAME)

            messages = self.chat_facade.get_user_chat_history(chat_id)
            
            if "partial_response" not in st.session_state:
                st.session_state.partial_response = ""
                
            if "stop_generation" not in st.session_state:
                st.session_state.stop_generation = False
                
            stop_button_container = st.empty()
            
            def stop_generation_clicked():
                st.session_state.stop_generation = True
                st.session_state.partial_response = full_response
            
            stop_button_container.button("Stop Generation", key="stop_button", on_click=stop_generation_clicked)
            
            model_service = SessionStateService().get_or_create_model_service()
            assistant_response = self.chat_facade.get_assistant_response(model_service, 
                                                                         messages, 
                                                                         chat_id)
            
            if st.session_state.stop_generation and st.session_state.partial_response:
                log_info(f"Using saved partial response: {st.session_state.partial_response[:100]}...")
                full_response = st.session_state.partial_response
                message_placeholder.markdown(full_response)
                
                # Clear the saved partial response and reset stop flag
                st.session_state.partial_response = ""
                st.session_state.stop_generation = False
                stop_button_container.empty()
                
                return full_response
            
            for response_chunk in assistant_response.response_chunks:
                if st.session_state.stop_generation:
                    log_info("Answer generation stopped by user")
                    st.session_state.partial_response = full_response
                    message_placeholder.markdown(full_response)
                    break
                full_response += response_chunk
                message_placeholder.markdown(full_response + "▌")
            
            st.session_state.stop_generation = False
            st.session_state.partial_response = ""
            stop_button_container.empty()
            
            message_placeholder.markdown(full_response)
            return full_response