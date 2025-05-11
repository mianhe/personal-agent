"""CLI 初始化模块。"""

import asyncio
from core.chat.chat_service_impl import ChatServiceImpl


def create_chat_service():
    """创建聊天服务实例。"""
    return ChatServiceImpl()
