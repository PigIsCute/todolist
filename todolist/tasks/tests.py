from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from tasks.models import Task
from tasks import views

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

class ViewUnitTest(TestCase):
    TASKS = {
        'test case1':'todo',
        'test case2':'done'
    }

    def setUp(self):
        for content, status in self.TASKS.items():
            Task.objects.create(content=content, status=status)

    def test_list_task(self):
        LIST_TASKS_ROUTER = 'list_tasks'
        response = self.client.get(reverse(LIST_TASKS_ROUTER))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todolist.html')
        for content, status in self.TASKS.items():
            self.assertContains(response, content)
            self.assertContains(response, status)

    def test_add_task(self):
        ADD_TASK_ROUTER = 'add_task'
        # test get method
        response = self.client.get(reverse(ADD_TASK_ROUTER))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_task.html')

        # test post method
        data = {
            'content':'test add task'
        }
        response = self.client.post(reverse('add_task'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('list_tasks'))
        task = Task.objects.get(content=data['content'])
        self.assertEqual(task.content, data['content'])
        self.assertEqual(task.status, 'undo')

    def test_edit_task(self):
        EDIT_TASK_ROUTER = 'edit_task'
        LIST_TASKS_ROUTER_NAME = 'list_tasks'
        BE_EDIT_TASK_ID = 1
        NEW_CONTENT = 'edit test'
        NEW_STATUS = 'done'

        # test get method
        response = self.client.get(reverse(EDIT_TASK_ROUTER, args=[BE_EDIT_TASK_ID]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('edit_task.html')

        # test post method
        response = self.client.post(
            reverse(
                EDIT_TASK_ROUTER,
                args=[BE_EDIT_TASK_ID]
            ),
            data={
                'content':NEW_CONTENT,
                'status':NEW_STATUS
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(LIST_TASKS_ROUTER_NAME))
        task = Task.objects.get(id=BE_EDIT_TASK_ID)
        self.assertEqual(task.content, NEW_CONTENT)
        self.assertEqual(task.status, NEW_STATUS)
        
    def test_delete_task(self):
        DELETE_TASK_ROUTER = 'delete_task'
        BE_DELETE_TASK_ID = 1
        response = self.client.get(reverse(DELETE_TASK_ROUTER, args=[BE_DELETE_TASK_ID]))
        task_amount = Task.objects.all().count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(task_amount, 1)
