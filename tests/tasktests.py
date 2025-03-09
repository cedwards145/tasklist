from datetime import datetime
import json
import unittest

from tasklist.models.task import Task
from tasklist.models.newtask import NewTask
from tasklist.main import add_task


class TaskTests(unittest.TestCase):
    def test_post_task(self):
        title = "Task Title"
        description = "Task Description"
        priority = 1
        due_date = datetime.fromisoformat("2000-01-30T15:00:00")

        input = NewTask(title=title, description=description, priority=priority, due_date=due_date)
        
        expected_output = {
            "id": 1,
            "title": title,
            "description": description,
            "priority": priority,
            "due_date": due_date,
            "completed": False
        }

        actual = add_task(input)
        self.assertEqual(actual, expected_output)

if __name__ == '__main__':
    unittest.main()