from concurrent.futures import ThreadPoolExecutor
from datetime import date
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from io import StringIO
from unittest.mock import patch

from app import TaskWebApp
from tasks import Task, TaskList
from task_storage import JsonTaskStorage
from main import main


class TaskStorageTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'tasks.json'
        self.tasks = TaskList(JsonTaskStorage(self.path))

    def test_restart_restores_dates_status_and_counter_after_deletion(self):
        first = self.tasks.add_task(Task('First', 'Study', date(2026, 12, 1)))
        second = self.tasks.add_task(Task('Second', 'Work'))
        self.tasks.complete_task(first.id)
        self.tasks.delete_task(second.id)
        restored = TaskList(JsonTaskStorage(self.path))
        saved = restored.list_tasks()[0]
        self.assertEqual(saved.id, first.id)
        self.assertEqual(saved.due_date, date(2026, 12, 1))
        self.assertTrue(saved.done)
        third = restored.add_task(Task('Third', 'Work'))
        self.assertEqual(third.id, 3)
        self.assertIsNone(TaskList(JsonTaskStorage(self.path)).list_tasks()[1].due_date)
        restored.delete_task(first.id)
        restored.delete_task(third.id)
        self.assertEqual(TaskList(JsonTaskStorage(self.path)).add_task(Task('Fourth', 'Work')).id, 4)

    def test_old_page_actions_never_target_another_task(self):
        client = TaskWebApp(self.tasks).app.test_client()
        first = self.tasks.add_task(Task('First', 'Study'))
        second = self.tasks.add_task(Task('Second', 'Work'))
        self.assertIn(f'/tasks/{second.id}/complete', client.get('/').text)
        self.assertEqual(client.post(f'/tasks/{first.id}/delete').status_code, 302)
        self.assertEqual(client.post(f'/tasks/{second.id}/complete').status_code, 302)
        self.assertEqual(client.post(f'/tasks/{first.id}/complete').status_code, 404)
        self.assertEqual(client.post(f'/tasks/{first.id}/delete').status_code, 404)
        self.assertTrue(TaskList(JsonTaskStorage(self.path)).list_tasks()[0].done)
        self.assertEqual(client.post('/tasks', data={'text':'Third', 'category':'Work'}).status_code, 302)
        self.assertEqual([task.id for task in self.tasks.list_tasks()], [2, 3])

    def test_concurrent_requests_assign_unique_ids_and_save_all_tasks(self):
        with ThreadPoolExecutor(max_workers=8) as executor:
            added = list(executor.map(lambda i: self.tasks.add_task(Task(str(i), 'Study')), range(30)))
        self.assertEqual(len({task.id for task in added}), 30)
        self.assertEqual(len(TaskList(JsonTaskStorage(self.path)).list_tasks()), 30)

    def test_failed_save_preserves_previous_file_and_memory(self):
        self.tasks.add_task(Task('First', 'Study'))
        original = self.path.read_bytes()
        with patch('task_storage.os.replace', side_effect=OSError('Disk error')):
            with self.assertRaises(OSError):
                self.tasks.delete_task(1)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(len(self.tasks.list_tasks()), 1)
        self.assertEqual(list(self.path.parent.glob('*.tmp')), [])

    def test_invalid_json_is_not_overwritten(self):
        self.path.write_text('{broken')
        with self.assertRaises(json.JSONDecodeError):
            TaskList(JsonTaskStorage(self.path))
        self.assertEqual(self.path.read_text(), '{broken')

    def test_terminal_deletes_by_id_after_a_gap(self):
        first = self.tasks.add_task(Task('First', 'Study'))
        second = self.tasks.add_task(Task('Second', 'Study'))
        self.tasks.delete_task(first.id)
        with patch('main.TaskList', return_value=self.tasks), patch(
            'builtins.input', side_effect=['3', str(second.id), '0']
        ), patch('sys.stdout', new_callable=StringIO):
            main()
        self.assertEqual(TaskList(JsonTaskStorage(self.path)).list_tasks(), [])


if __name__ == '__main__':
    unittest.main()
