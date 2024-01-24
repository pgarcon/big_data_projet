from model.kafka.producer import ProducerClass

print("#### Producer is running...")
mw = ProducerClass('2023-12-01', '2023-12-07')

mw.produce()