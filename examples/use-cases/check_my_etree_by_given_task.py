import os
import time
from pprint import pprint

from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from browser_use.browser.browser import BrowserContextConfig
from browser_use.browser.context import BrowserContext
from dotenv import load_dotenv

load_dotenv()

import asyncio

# task="""
# Verify navigation between the main interface and the certificates page
# Step 1: Open the browser and navigate to the edge://wallet page.
# Step 2: Click on the ETree widget in the bottom left corner of the edge://wallet page.
# Step 3: Ensure that a pop-up window opens, displaying the main ETree interface.
# Step 4: From the ETree main interface, click the medal icon to open the certificates page.
# Step 5: Verify that the user can navigate back to the main ETree interface from the certificates page by clicking a designated back button on the top left corner of the certificates page.
# Expected Result: The user should be able to easily navigate between the main interface and the certificates page.
# """

task="""
## Test Case 1: Accessing ETree Feature
** Verify that the ETree feature can be accessed successfully from the wallet page. **
### Test Steps
#### Step 1: Navigate to Wallet Page
- Open the browser and navigate to edge://wallet.
- The expected result is that the wallet page loads successfully without errors.
#### Step 2: Locate ETree Component
- Look for the ETree floating component located at the bottom left corner of the wallet page.
- The expected result is that the ETree component is visible and displays a tree image along with the user's current level.

## Test Case 2: Opening ETree Main Interface
** Verify that clicking on the ETree component opens the main interface. **
### Test Steps
#### Step 1: Click on ETree Component
- Click on the ETree floating component.
- The expected result is that a new window opens with the ETree main interface.
#### Step 2: Verify Main Interface Elements
- Check that the main interface displays the user's nickname in the upper left corner, a background image of greenery, and a small tree seedling.
- The expected result is that all these elements are displayed correctly without any layout issues.

## Test Case 3: Viewing Today's Tasks
** Verify that today's tasks are displayed properly in the ETree interface. **
### Test Steps
#### Step 1: Check Task Descriptions and Rewards
- In the ETree main interface, look for the section that lists today's tasks.
- The expected result is that each task is displayed with a clear description and the corresponding rewards.
#### Step 2: Validate Task Information
- Click on each task to view detailed information, if available.
- The expected result is that the detailed information of each task is displayed correctly.

## Test Case 4: Accessing Certificates Page
** Verify that users can access the certificates page by clicking on the medal icon. **
### Test Steps
#### Step 1: Click on Medal Icon
- Locate and click the medal icon just below the user's nickname on the ETree main interface.
- The expected result is that the certificates page opens successfully.
#### Step 2: Verify Certificates Display
- Check that the certificates page displays currently earned certificates or badges, including their names and current progress.
- The expected result is that all certificates and their progress are displayed accurately.

## Test Case 5: Returning to Main Interface from Certificates Page
** Ensure that users can return to the main ETree interface from the certificates page. **
### Test Steps
#### Step 1: Navigate Back to Main Interface
- Look for a back button or link on the certificates page to return to the main interface.
- The expected result is that clicking the back button successfully navigates the user back to the ETree main interface.
#### Step 2: Verify Main Interface After Returning
- Confirm that the main interface is displayed correctly upon returning.
- The expected result is that all elements (user's nickname, background image, today's tasks) are intact and visible.
"""

initial_actions = [
	{'switch_tab': {'page_id': '0'}},
]

browser = Browser(
	config=BrowserConfig(
		headless=False,
		disable_security=True,
		chrome_instance_path='C:\\Users\\wjia\\AppData\\Local\\Microsoft\\Edge SxS\\Application\\msedge.exe',
		extra_chromium_args=['--profile-directory=Profile 1', '--user-data-dir=C:\\Users\\wjia\\AppData\\Local\\Microsoft\\Edge SxS\\User Data\\'],
    )
)

context = BrowserContext(
    browser=browser,
    config=BrowserContextConfig(
        save_recording_path='./tmp/recording',
        wait_for_network_idle_page_load_time=3.0,
    )
)

llm=ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task=task,
        initial_actions=initial_actions,
        llm=llm,
        use_vision=True,
        # browser=browser,
        browser_context=context,
        generate_gif=os.path.join('./tmp/gif/', f"{int(time.time())}.gif")
        )

    history = await agent.run(max_steps=50)
    history_file = os.path.join('./tmp/history/', f"{int(time.time())}.json")
    agent.save_history(history_file)
    
    print('\nFinal Result:')
    print(history.final_result())

    if history.has_errors():
        print('\nErrors:')
        print(history.errors())

    # print('\nThoughts:')
    # print(history.model_thoughts())

    # print('\nAction Results:')
    # print(history.action_results())

    await browser.close()
    await context.close()

if __name__ == '__main__':
    asyncio.run(main())