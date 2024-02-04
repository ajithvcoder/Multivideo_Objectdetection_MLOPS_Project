config = {
    'bootstrap.servers': 'broker:29092',
    'enable.idempotence': True,
    'acks': 'all',
    'retries': 10,
    'max.in.flight.requests.per.connection': 5,
    'compression.type': 'snappy',
    'linger.ms': 5,
    'batch.num.messages': 32
    }