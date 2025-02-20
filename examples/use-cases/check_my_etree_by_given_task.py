import os
import time

from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.browser import BrowserContextConfig
from dotenv import load_dotenv

load_dotenv()

import asyncio

task="""
Verify navigation between the main interface and the certificates page
Step 1: Open the browser and navigate to the edge://wallet page.
Step 2: Click on the ETree widget in the bottom left corner of the edge://wallet page.
Step 3: Ensure that a pop-up window opens, displaying the main ETree interface.
Step 4: From the ETree main interface, click the medal icon to open the certificates page.
Step 5: Verify that the user can navigate back to the main ETree interface from the certificates page by clicking a designated back button on the top left corner of the certificates page.
Expected Result: The user should be able to easily navigate between the main interface and the certificates page.
"""

initial_actions = [
    # switch to wallet page if internal page cannot be loaded
	{'switch_tab': {'page_id': '0'}},
]

browser = Browser(
	config=BrowserConfig(
		headless=False,
		disable_security=True,
		chrome_instance_path='C:\\Users\\wjia\\AppData\\Local\\Microsoft\\Edge SxS\\Application\\msedge.exe',
		extra_chromium_args=['--profile-directory=Profile 1'] + ['--user-data-dir=C:\\Users\\wjia\\AppData\\Local\\Microsoft\\Edge SxS\\User Data\\'],
        # new_context_config=BrowserContextConfig(
        #     trace_path='./tmp/check_my_etree_trace',
        #     save_recording_path='./tmp/check_my_etree_recording',
        #     no_viewport=False,
		# 	browser_window_size={
		# 		'width': 1280,
		# 		'height': 1100,
		# 	},
		# ),
    )
)

agent = Agent(
    task=task,
    initial_actions=initial_actions,
    llm=ChatOpenAI(model="gpt-4o"),
    use_vision=True,
    browser=browser,
    max_actions_per_step=10,
    generate_gif=os.path.join('.\\tmp\\gif\\', f"{int(time.time())}.gif")
    )

async def main():
    history = await agent.run(max_steps=50)
    history_file = os.path.join('.\\tmp\\history\\', f"{agent.state.agent_id}.json")
    agent.save_history(history_file)
    result = history.final_result()
    if result:
        print(f'{result}')
    else:
        print('No result')

    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())