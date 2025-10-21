python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt
cd todolist
python3 manage.py makemigrations
python3 manage.py migrate
deactivate
