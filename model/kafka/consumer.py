from confluent_kafka import Consumer
from model.utils import read_ccloud_config
from model.utils import PROPERTIES_FILE

class ConsumerClass:

    def consumerMessage(self):

        props = read_ccloud_config(PROPERTIES_FILE)
        props["group.id"] = "python-group-1"
        props["auto.offset.reset"] = "earliest"

        consumer = Consumer(props)
        consumer.subscribe(["big_data_meteo_topic"])

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break

                print('Received message: {}'.format(msg.value().decode('utf-8')))
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()