while ! curl http://db:5432/ 2>&1 | grep '52'
do
  sleep 1
done


export FLASK_APP=main.py
flask db upgrade
python main.py