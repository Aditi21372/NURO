import logging
from django.shortcuts import render
from google import genai
import requests

from django.conf import settings  # Import settings
import json  # Ensure json is imported

from django.http import JsonResponse
from .models import Task
from django.utils import timezone

# Set up logging
logger = logging.getLogger(__name__)

def load_llm_model():
    try:
        logger.info("Loading DeepSeek R1 model...")
        # Code to load the DeepSeek R1 model goes here
        logger.info("DeepSeek R1 model loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")

def manage_task(request):
    load_llm_model()

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        if not task_name:
            return render(request, 'manage_tasks.html', {'error': 'Task name cannot be empty.'})

        new_task = Task(
            title=task_name,
            description="Default description",  # Set a default description
            priority=1,  # Set a default priority
            deadline=timezone.now()  # Set the current time as the default deadline
        )
        try:
            new_task.save()  # Save the task to the database
        except Exception as e:
            logger.error(f"Failed to save task: {str(e)}")
            return render(request, 'manage_tasks.html', {'error': 'Failed to save task: ' + str(e)})

        # Call the LLM to get the breakdown
        try:
            client = genai.Client(api_key=settings.GENAI_API_KEY)  # Use the API key from settings
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=f"I have a task:{task_name} . Break it down into smaller, actionable steps that are clear, manageable, and ordered logically. Each step should be specific and concise, ensuring steady progress toward completing the main task. If possible, suggest any tools, techniques, or resources that might help. return it as a json response"  # Update content based on task name
            )
            logger.info("Response Content: {}".format(response.text))
            breakdown = response.text  # Adjust this line based on the new API response structure
            logger.info(f"Breakdown Data: {breakdown}")
            logger.info("LLM breakdown retrieved successfully.")
        except Exception as e:
            logger.error(f"Failed to retrieve breakdown from LLM: {str(e)}")
            logger.error("Using fallback breakdown.")
            breakdown = { 
                "mindmap": [f"Research {task_name}", f"Draft {task_name} outline", f"Review {task_name}"],
                "checklist": [f"Gather materials for {task_name}", f"Complete {task_name} draft", f"Submit {task_name}"]
            }

        return render(request, 'task_result.html', {'breakdown': breakdown})

    return render(request, 'manage_tasks.html', {'success': 'Task created successfully!'})

def test_endpoint(request):
    return JsonResponse({'message': 'Django API is running!'}, status=200)
