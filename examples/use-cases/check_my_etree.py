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
   ### Prompt for Testing Agent - Check My ETree level, daily tasks, and certificates

**Objective:**  
Visit [Wallet Homepage](edge://wallet), open ETree widget, check current level, today's tasks, and certificates.

**Important:**
- Make sure that you accurately check the elements I specified on the page.
- If you open any 2nd-level window of ETree widget, you can go back by clicking the '<' button of the top left. This will help you navigate easier.
---

### Step 1: Navigate to the Wallet Homepage
- Open [Wallet Homepage](edge://wallet). You can input 'edge://wallet' in the address bar, then hit enter. Noted that, this is an internal page, please stop and ask me if you found the page cannot be loaded.
- Make sure the page was fully loaded.
---

### Step 2: Open the ETree widget
- There's an floating bubble showing a small tree on the bottom-left.
- Check what the current level is, it usually shown like 'Level N' in white color on the bottom of the bubble.
- Click this floating bubble to open the ETree pop-up window.
---

### Step 3: Find out today's tasks
- On the bottom of the pop-up window, there's a section shows the Today's tasks, which is designed to help me to promote my ETree level and earn the rewards.
- Check each task, including the task name and the reward. 
---

### Step 4: Check my current certificates
- On the top-left of the pop-up window, there'a certificate icon.
- Click this icon to open the 'My Certificates' page, it shows all my badges.
- Check each badge I owned, including the badge's name and current progress.
---

### Step 5: Gather all information and let me know
- Output all the informations I ask you to check above as following format:
  - **My current ETree Level is:**.
  - **My today's tasks are:**, ** (including the name and reward).
  - **My certificates are:**, ** (including the name and progress).

**Important:** Ensure efficiency and accuracy throughout the process.
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
    history_file = os.path.join('.\\tmp\\history\\', f"{int(time.time())}.json")
    agent.save_history(history_file)
    result = history.final_result()
    if result:
        print(f'{result}')
    else:
        print('No result')

    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())