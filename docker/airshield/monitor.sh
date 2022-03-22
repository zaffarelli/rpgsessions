multitail -sw 105,0 -sn 3 -ts -R 10 \
    -l "echo -n 'RawSourceData: '; echo 'from airshield.common.models import RawSourceData; print(RawSourceData.objects.count())'|airshield-admin shell" \
    -ts -r 10 -cS vmstat -l vmstat \
    -ts -R 10 -l "airshield-admin stats --no-{update,object}-counts --tasks|grep \'name\':|awk '{print \$2}'|tr -d ,|sort |uniq -c" \
    -ts -R 10 -l 'redis-cli info memory' \
    -ts -R 10 -l 'rabbitmqctl list_queues name messages messages_ready messages_unacknowledged' \
    -f /var/log/airshield/cve-aggregation-workers.log
