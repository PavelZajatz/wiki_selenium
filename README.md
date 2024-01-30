# Set up python environment for autotests
1. Make sure you have python installed on your machine by typing in console "python --version" 
   (python 3.12 was used for test development)
2. Activate VirtualEnv 
   >source venv/bin/activate
3. Install requirements.txt
   >pip install -r requirements.txt
4. Install Allure for reporting. Instruction can be found here: https://docs.qameta.io/allure-report/
5. Install PyTest as default runner(instruction for PyCharm IDE )
- PyCharm - Preferences - Tools - Python integrated tools - default test runner: pytest

# Run tests
- To run all tests execute next script:
  >pytest
- To run specific tests execute next script:
  >pytest tests/test_search.py::TestSearch::test_verify_search
- To run test with allure report execute next script: 
  >pytest --alluredir=reports
- To serve allure report execute next script: 
  >allure serve reports