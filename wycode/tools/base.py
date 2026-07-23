
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".tox", ".mypy_cache"}

MAX_OUTPUT_CHARS = 10000


"""
工具分类：
- read：只读工具，通常用于获取信息或数据，不会修改系统状态。
- write：写入工具，通常用于修改系统状态或数据。
- command：命令工具，通常用于执行特定的操作或命令，可能会修改系统状态。
"""
ToolCategory = Literal["read", "write", "command"]


@dataclass
class ToolResult:
    output: str
    is_error: bool = False


"""
参数说明：
- name: 工具的名称，用于标识工具。
- description: 工具的描述，说明工具的功能和用途。
- params_model: 工具参数的 Pydantic 模型类型，用于验证和解析工具的输入参数。
- category: 工具的分类，表示工具的类型（只读、写入或命令）。
- is_concurrency_safe: 是否支持并发执行，如果为 True，表示工具可以在多个线程或进程中安全地执行。
- is_system_tool: 是否为系统工具，如果为 True，表示工具是系统级别的工具，通常用于系统管理或维护。
- should_defer: 是否应该延迟执行，如果为 True，表示工具的执行可以被延迟，通常用于需要等待某些条件满足后再执行的工具。
"""

class Tool(ABC):
    name: str
    description: str
    params_model: type[BaseModel]
    category: ToolCategory = "read"
    is_concurrency_safe: bool = False
    is_system_tool: bool = False
    should_defer: bool = False

    @property
    def is_read_only(self) -> bool:
        return self.category == "read"


    def get_schema(self) -> dict[str, Any]:
        schema = self.params_model.model_json_schema()
        schema.pop("title", None)
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": schema,
        }

    @abstractmethod
    async def execute(self, params: BaseModel) -> ToolResult: ...


# --- 流式事件 ---


@dataclass
class TextDelta:
    text: str


@dataclass
class ToolCallStart:
    tool_name: str
    tool_id: str


@dataclass
class ToolCallDelta:
    text: str


@dataclass
class ToolCallComplete:
    tool_id: str
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class ThinkingDelta:
    text: str


@dataclass
class ThinkingComplete:
    thinking: str
    signature: str


@dataclass
class StreamEnd:
    stop_reason: str
    input_tokens: int = 0
    output_tokens: int = 0
    # API 返回的 prompt cache 用量。Anthropic 把缓存前缀 token 分为
    # "read"（cache 命中，按 10% 计费）和 "creation"（cache 写入）。
    # input_tokens 已排除这两部分，因此实际 prompt 大小 =
    # input + cache_read + cache_creation。OpenAI 系列只暴露
    # cache_read（通过 *_tokens_details.cached_tokens），没有 creation
    # 计数，所以 cache_creation 在那边始终为 0。
    cache_read: int = 0
    cache_creation: int = 0


StreamEvent = TextDelta | ThinkingDelta | ThinkingComplete | ToolCallStart | ToolCallDelta | ToolCallComplete | StreamEnd
