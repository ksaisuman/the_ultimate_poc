from prometheus_client import multiprocess



def child_exit(server, worker):
    multiprocess.mark_process_dead(worker.pid)


bind = "0.0.0.0:8000"
accesslog  = "-"
access_log_format = "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s' %(M)s"
workers = 7
threads = 3
statsd_host = "statsd_exporter:9125"
statsd_prefix = "tup"