clear

mkdir -p backup/$1/

python ./manage.py dumpdata auth.user --indent 2 --format xml > backup/$1/user.xml
python ./manage.py dumpdata scheduler.realm --indent 2 --format xml > ./backup/$1/realm.xml
python ./manage.py dumpdata scheduler.profile --indent 2 --format xml > ./backup/$1/profile.xml
python ./manage.py dumpdata scheduler.game --indent 2 --format xml > ./backup/$1/game.xml
python ./manage.py dumpdata scheduler.session --indent 2 --format xml > ./backup/$1/session.xml
python ./manage.py dumpdata scheduler.inscription --indent 2 --format xml > ./backup/$1/inscription.xml
python ./manage.py dumpdata scheduler.follower --indent 2 --format xml > ./backup/$1/follower.xml