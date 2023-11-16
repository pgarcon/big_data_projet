from model.kafka.producer import ProducerClass
from model.kafka.consumer import ConsumerClass

print("#### Main is running...")
mw = ProducerClass()
cs = ConsumerClass()


mw.produce()
