from os import getenv
from sys import stdin

__all__ = [
    "env_flag",
    "env_text",
    "unattended",
]

TRUE_VALUES = {
    "1",
    "true",
    "yes",
    "y",
    "on",
}

FALSE_VALUES = {
    "0",
    "false",
    "no",
    "n",
    "off",
}


def env_text(name: str, default: str = "") -> str:
    """读取文本型环境变量，未设置或内容为空白时返回默认值"""
    value = getenv(name)
    return value.strip() if value and value.strip() else default


def env_flag(name: str, default: bool = False) -> bool:
    """读取布尔型环境变量，未设置或无法识别时返回默认值"""
    value = env_text(name).lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False
    return default


def unattended() -> bool:
    """
    是否处于无人值守模式

    优先读取环境变量 DOUK_UNATTENDED；未设置时，根据是否分配交互终端判断，
    容器、CI 等非交互环境默认启用，避免启动流程阻塞在输入提示上。
    """
    if getenv("DOUK_UNATTENDED") is not None:
        return env_flag("DOUK_UNATTENDED", True)
    try:
        return not stdin.isatty()
    except (AttributeError, ValueError):
        return True
