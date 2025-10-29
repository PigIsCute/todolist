from django.test import TestCase
from django.core.exceptions import ValidationError
from tasks.models import Task

# Create your tests here.
class ModelTest(TestCase):
    def test_str_method(self):
        task = Task.objects.create(content="Buy milk", status="undo")
        self.assertEqual(str(task), "Buy milk, undo")

    def test_default_status(self):
        task = Task.objects.create(content="Walk dog")
        self.assertEqual(task.status, "undo")

    def test_status_choices(self):
        # 測試存入錯誤的狀態應該拋出錯誤
        task = Task(content="Invalid task", status="invalid_status")
        with self.assertRaises(ValidationError):
            task.full_clean()  # 驗證模型欄位（會觸發 choices 檢查）

    def test_content_required(self):
        task = Task(status="undo")  # 沒有 content
        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_content_max_length(self):
        long_content = "A" * 51
        task = Task(content=long_content)
        with self.assertRaises(ValidationError):
            task.full_clean()

        