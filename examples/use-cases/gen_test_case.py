import openai
import json
import os

from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class TestCaseGenerator:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required, please set OPENAI_API_KEY in environment variable or dotenv file")
        self.model = model
        self.client = openai.OpenAI(api_key=self.api_key)
        self.messages = []

    def generate_test_case(self, use_case_description: str) -> Dict[str, Any]:
        # Add system prompt
        system_prompt = """
        You are a product expert and testing expert.
        You are good at designing test cases from a given use case description or product feature description.
        I'm building a Web Agent by leveraging LLM and other frameworks like browser-use, it can help me to test functionality of a web product.
        You'll be given a use case description or product feature description and you need to generate test cases as following JSON format.
        ```
        [
            {
                "test_case_name": "a brief test case name",
                "test_case_description": "test case description",
                "steps": [
                    {
                        "step_name": "a brief step name",
                        "step_description": "step description, like how to do, what to see, what to click, what to input, etc.",
                        "expected_result": "expected result if has"
                    }
                ]
            }
        ]
        ```
        Other hints may be usefule are:
        - All use case descriptions or product feature descriptions are written in natural language, either in English or Simplified Chinese.
        - All test steps should be able to act on a web page.
        - Carefully consider how to design the test steps according to each functionality.
        - Carefully consider edge cases and corner cases
        - Also consider the behavior or interaction on the web page.
        """

        # Add user prompt
        user_prompt = f"""
        Use case description:
        {use_case_description}
        """
        self.messages.append({"role": "system", "content": system_prompt})
        self.messages.append({"role": "user", "content": user_prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            if content is None:
                return {"error": "No content received from API"}
            return json.loads(content)
        except Exception as e:
            return {
                "error": str(e)
            }

def main():
    test_case_generator = TestCaseGenerator()
    test_cases = test_case_generator.generate_test_case("""
- 该功能名为电子树（ETree），它是虚拟的植树活动，鼓励用户完成一些任务，提升等级，并且获得对应的证书或徽章。
- 该功能的入口位于 edge://wallet 页面左下角，它是一个悬浮的小组件，组件中会显示一棵树，同时下方会展示用户当前的等级（Level）。
- 点击该悬浮组件，会打开一个窗口，是该功能的主要界面。里面包含：
- 页面在左上角显示用户的昵称
- 页面背景有一幅绿意盎然的图片以及一棵小树苗
- 页面下方则展示了用户的每日任务（today's tasks），任务有简单的描述信息以及对应的奖励
- 页面左上方用户昵称下有一个奖章图标，点击该图标将打开证书（certificates）页面，里面将展示用户当前获得的证书或奖章，包含名称，以及当前进度。
- 从证书页面可以返回到主页面
    """)
    print(json.dumps(test_cases, indent=2))

if __name__ == "__main__":
    main()