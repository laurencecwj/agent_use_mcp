import os
import sys
import json
from typing import Dict, Optional, Union

from qwen_agent.agents import FnCallAgent
from qwen_agent.tools.base import BaseTool, register_tool


@register_tool("UserDatabase")
class UserDatabase(BaseTool):
    description = "企业员工数据库，包含员工的性别、生日、职位信息"
    name = "UserDatabase"
    parameters: list = [
        {
            "name": "name",
            "type": "string",
            "description": "员工名字，所属查阅信息的员工姓名，如`张三",
            "required": True,
        }
    ]

    def __init__(self, cfg: Optional[Dict] = None):
        super().__init__(cfg)

        # 数据库存有员工基本信息
        self.database = {
            "李四": {"性别": "女", "生日": "10月3日", "职位": "画师"},
            "张三": {"性别": "男", "生日": "5月5日", "职位": "业务员"},
            "王五": {"性别": "男", "生日": "12月19日", "职位": "业务经理"},
        }

    def call(self, params: Union[str, dict], **kwargs) -> str:
        params = self._verify_json_format_args(params)

        name = params["name"]
        # 输入姓名返回员工信息
        return json.dumps(self.database.get(name, "查无此人"), ensure_ascii=False)


llm_config = {
    "model": "qwen3:8b",
    "model_server": "http://localhost:11434/v1/",
    "api_key": "ollama",
}
function_list = ["UserDatabase"]
bot = FnCallAgent(function_list=function_list, llm=llm_config)

for response in bot.run(
        messages=[{'role': 'user', 'content': "职工张三的生日是在今年10月份吗？现在是2月份，距离张三的生日还有几个月？"}]
):
    #print(response)
    print(".")
print()
print(response[-1])

