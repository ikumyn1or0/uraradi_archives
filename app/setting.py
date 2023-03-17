import streamlit as st


import Chat as myChat
import config as myconfig
import Radio as myRadio
import Transcript as myTranscript


def set_site_config():
    st.set_page_config(page_title=myconfig.PAGE_TITLE, page_icon=myconfig.PAGE_ICON)
    st.title(myconfig.SITE_TITLE)


def load_RadioList():
    if "radiolist" not in st.session_state:
        st.session_state.radiolist = myRadio.RadioList()
        print("RadioList loaded.")
    return st.session_state.radiolist


def load_TranscriptList():
    if "transcriptlist" not in st.session_state:
        st.session_state.transcriptlist = myTranscript.TranscriptList()
        print("TranscriptList loaded.")
    return st.session_state.transcriptlist


def load_ChatList():
    if "chatlist" not in st.session_state:
        st.session_state.chatlist = myChat.ChatList()
        print("ChatList loaded.")
    return st.session_state.chatlist
