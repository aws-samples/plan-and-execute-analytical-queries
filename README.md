## Plan & Execute using Amazon Bedrock

This sample illustrates how one can use Claude 3.5 and Amazon Bedrock to perform complex agent based tasks that requires orchestration of multiple function calls.

This particular examples aims to showcase how an LLM can answer analytical questions based on a dataset.

# Plan

The planning stage is where the LLM is asked to define an execution plan. A plan is a series of function calls with defined parameters that the LLM concludes should be able to answer the question.
# Execute
In the execute step the plan is executed with Python code that parses the plan and calls the functions.
# How to run

```
pip install -r requirements.txt
python plan_and_execute.py
```