from tasks import views
from tasks.models import Task
from django.test import TestCase
from django.urls import reverse

class ViewTest(TestCase):
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
