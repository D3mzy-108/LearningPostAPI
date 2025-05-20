import json
from django.shortcuts import render

from core.settings import BASE_DIR
from website.models import User, UserSubscription


def get_grades_list() -> list:
    """
    Retrieves grade data from grades.json and passes it to a template.
    """
    try:
        with open(f'{BASE_DIR}/static/assets/grades.json', 'r') as f:
            data = json.load(f)
            grades = data.get('grades', [])
    except FileNotFoundError:
        grades = []
        # Optionally log the error or display a user-friendly message
        print("Error: grades.json file not found.")
    except json.JSONDecodeError:
        grades = []
        # Optionally log the error or display a user-friendly message
        print("Error: Could not decode JSON from grades.json.")

    return grades


def user_subscribed_grades(user: User) -> list:
    try:
        subscription = UserSubscription.objects.filter(profile=user).first()
        if subscription:
            user_grades = subscription.grades
            user_grades_list = user_grades.split('|') if user_grades else []
            return user_grades_list
        else:
            return []
    except:
        return []


def set_user_subscribed_grades_string(grades: list[str]) -> str:
    return '|'.join(grades)
