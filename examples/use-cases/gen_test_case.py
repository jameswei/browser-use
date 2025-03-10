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

    # def generate_test_case(self, use_case_description: str) -> Dict[str, Any]:
    def generate_test_case(self, use_case_description: str) -> str:
        # Add system prompt
        system_prompt = """
        You are a product expert and testing expert.
        You are good at designing test cases from a given use case description or product feature description.
        I'm building a Web Agent by leveraging LLM and other frameworks like browser-use, it can help me to test functionality of a web product.
        You'll be given a use case description or product feature description and you need to generate test cases as following format.

        ```
        ## Test Case 1: {{test_case_name}}
        ** {{test_case_description}} **
        ### Test Steps
        #### Step 1: {{step_name}}
        - {{step_description}}
        - {{expected_result}}
        #### Step 2: {{step_name}}
        - {{step_description}}
        - {{expected_result}}
        ===
        ## Test Case 2: {{another_test_case_name}}
        ** {{another_test_case_description}} **
        ### Test Steps
        #### Step 1: {{step_name}}
        - {{step_description}}
        - {{expected_result}}
        #### Step 2: {{step_name}}
        - {{step_description}}
        - {{expected_result}}
        ```

        Other hints and requirements are:
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
                # response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            if content is None:
                # return {"error": "No content received from API"}
                return "No content received from API"
            # return json.loads(content)
            return content
        except Exception as e:
            # return {"error": str(e)}
            return str(e)

def main():
    test_case_generator = TestCaseGenerator()
    test_cases = test_case_generator.generate_test_case("""
- The feature is called ETree, which is a virtual tree-planting event that encourages users to complete certain tasks, level up, and earn corresponding certificates or badges.
- The entrance to this feature is located in the bottom left corner of the edge://wallet page, which is a floating widget that displays a tree and the user's current level below.
- Clicking on the hover component will open a popup window, which is the main interface for the feature. It contains several different and important elements as following, make sure all elements are shown.
    - The page displays the user's nickname in the upper left corner.
    - The page has a green background and a small sapling in the middle of the background.
    - There're some 'Water drop' icons above the sapling, which are used to water the sapling, but it's a kind of virtual watering.
    - At the bottom of the page, you'll find your 'Today's Tasks', which have a brief description and corresponding rewards.
    - At the top-right corner, there's a 'X' icon, clicking on it will close the popup window.
    - There is a badge icon under the user's nickname at the top left of the page.
- Make sure you're on the ETree main interface, then click the edit button, which looks like a pencil icon, will make the user's nickname editable. You can input a new nickname, for example, 'XPay Team', and click the save button, which looks like a checkmark icon, to save the new nickname. After that, you should see the nickname has been updated to 'XPay Team'.
- Make sure you're on the ETree main interface, then click the any one of the 'Water drop' icons will water the sapling, you'll find the sapling grows a little bit and the progress bar, which is a green bar under the sapling, increases a little bit. 
- Make sure you're on the ETree main interface, try to click all the 'Water drop' icons. Check if the progress bar is full.
    - If so, you'll get a 'Congratulations! You've reached Level n!' level up notification, which means you've achieved a milestone. Then you're able to click the 'Got it' button with green background to close the notification.
    - If not, you'll see the sapling grows a lot and the progress bar also increases a lot, but it doesn't reach the maximum.
- Make sure you're on the ETree main interface, then click the badge icon will open the Certificates page, which will display the user's current certificates or medals, including the name, and current progress. Make sure all elemenets are shown.
- Make sure you've opened the Certificates page, then you're able to return to the main page by clicking the 'Back' button.
- Finally, after you've played with the sapling for a while, you're able to click 'X' button to close the ETree window.
    """)
    # print(json.dumps(test_cases, indent=2))
    print(test_cases)

if __name__ == "__main__":
    main()

# {
#   "test_cases": [
#     {
#       "test_case_name": "Verify ETree Component Visibility",
#       "test_case_description": "Ensure the ETree component is visible on the edge://wallet page.",
#       "steps": [
#         {
#           "step_name": "Open Wallet Page",
#           "step_description": "Navigate to edge://wallet in the browser.",
#           "expected_result": "The Wallet page loads successfully."
#         },
#         {
#           "step_name": "Check ETree Widget",
#           "step_description": "Locate the ETree component in the bottom left corner of the Wallet page. Ensure it displays a tree icon and the user's current level.",
#           "expected_result": "The ETree component is visible, showing a tree icon and the user's level."
#         }
#       ]
#     },
#     {
#       "test_case_name": "Open ETree Functionality",
#       "test_case_description": "Test the functionality of the ETree component when clicked.",
#       "steps": [
#         {
#           "step_name": "Click ETree Component",
#           "step_description": "Click on the ETree component located at the bottom left corner of the wallet page.",
#           "expected_result": "A new window opens displaying the main interface of the ETree feature."
#         },
#         {
#           "step_name": "Verify User Nickname",
#           "step_description": "Check the top left of the ETree interface for the user's nickname.",
#           "expected_result": "The user's nickname is correctly displayed at the top left."
#         },
#         {
#           "step_name": "Check Background and Tree Seedling",
#           "step_description": "Examine the background image of the ETree interface and ensure a small seedling tree is visible.",
#           "expected_result": "The background displays a lush green image with a small seedling tree."
#         },
#         {
#           "step_name": "View Daily Tasks",
#           "step_description": "Scroll down to view the displayed daily tasks. Verify that each task has a description and a reward.",
#           "expected_result": "Daily tasks are displayed with their descriptions and corresponding rewards."
#         }
#       ]
#     },
#     {
#       "test_case_name": "Access Certificates from ETree",
#       "test_case_description": "Verify that the certificates page can be accessed from the ETree interface.",
#       "steps": [
#         {
#           "step_name": "Click Medal Icon",
#           "step_description": "In the ETree interface, click on the medal icon located directly beneath the user's nickname.",
#           "expected_result": "The certificates page opens, showing the user's current certificates and progress."
#         },
#         {
#           "step_name": "Check Certificates List",
#           "step_description": "Verify that the certificates page lists all certificates the user has earned, displaying names and progress.",
#           "expected_result": "The certificates page displays a list of earned certificates with their corresponding progress."
#         },
#         {
#           "step_name": "Return to Main ETree Page",
#           "step_description": "Locate and click on the back button to return to the main ETree interface from the certificates page.",
#           "expected_result": "The user is navigated back to the main ETree interface."
#         }
#       ]
#     }
#   ]
# }

# ## ETree Functional Test Case
# ### Verify the ETree functionality and user interface elements
# ### Test Steps
# - Launch the browser and navigate to edge://wallet
#   - Open the specified URL.
#   - The ETree component should be visible at the bottom left of the page, showing a tree and the user’s current level.

# - Click on the ETree component
#   - Interact with the ETree floating component by clicking it.
#   - A new window should open displaying the ETree main interface.

# - Verify the user nickname display
#   - Check if the user's nickname is shown in the top left corner of the main interface.
#   - The displayed nickname should match the logged-in user's nickname.

# - Verify background image and tree visibility
#   - Inspect the background of the ETree main interface.
#   - The background should show a lush green image and a small sapling should be visible.

# - Verify today's tasks section
#   - Locate the section containing today's tasks on the main interface.
#   - This section should list the tasks along with brief descriptions and their corresponding rewards.

# - Click on the medal icon
#   - Click on the medal icon located below the user’s nickname.
#   - A new page should open displaying the certificates page.

# - Verify the certificates page content
#   - Inspect the certificates page for the user's current awarded certificates or badges.
#   - The page should display the names of certificates/badges along with the current progress towards each.

# - Navigate back to the main page from certificates page
#   - Click the designated "Back" button on the certificates page.
#   - The main ETree interface should be displayed again without any errors.

# - Edge case: Check behavior with no tasks available
#   - Ensure that when there are no tasks assigned for the day, appropriate messaging is displayed in the tasks section.
#   - The message should indicate that there are no current tasks.

# - Edge case: User without certificates
#   - Log in as a user who has not earned any certificates.
#   - When accessing the certificates page, it should indicate that no certificates are currently available.