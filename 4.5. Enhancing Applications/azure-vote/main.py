from flask import Flask, request, render_template
import os
import random
import redis
import socket
import sys
import logging
from datetime import datetime

# App Insights
# TODO: Import required libraries for App Insights
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.log_exporter import AzureEventHandler
from opencensus.ext.azure import metrics_exporter
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.tags import tag_map as tag_map_module
from opencensus.trace import config_integration
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

#from applicationinsights import TelemetryClient

INSTRUMENTATION_KEY = '648e3a8c-bf03-4f82-9125-2cb58e86969e'

# Logging
# TODO: Setup logger
config_integration.trace_integrations(['logging'])
config_integration.trace_integrations(['requests'])

handler = AzureLogHandler(
    connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}')
handler.setFormatter(logging.Formatter('%(traceId)s %(spanId)s %(message)s'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.addHandler(handler)

# Logging custom Events
logger.addHandler(AzureEventHandler(
    connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'))

# Metrics
# TODO: Setup exporter
stats = stats_module.stats
view_manager = stats.view_manager

exporter = metrics_exporter.new_metrics_exporter(
    enable_standard_metrics=True,
    connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}')

view_manager.register_exporter(exporter)

# Tracing
# TODO: Setup tracer
tracer = Tracer(
    exporter=AzureExporter(
        connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'),
    sampler=ProbabilitySampler(1.0),
)

#tc = TelemetryClient(INSTRUMENTATION_KEY)

app = Flask(__name__)

# Requests
# TODO: Setup flask middleware
middleware = FlaskMiddleware(
    app,
    exporter=AzureExporter(
        connection_string=f'InstrumentationKey={INSTRUMENTATION_KEY}'),
    sampler=ProbabilitySampler(rate=1.0),
)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ('VOTE1VALUE' in os.environ and os.environ['VOTE1VALUE']):
    button1 = os.environ['VOTE1VALUE']
else:
    button1 = app.config['VOTE1VALUE']

if ('VOTE2VALUE' in os.environ and os.environ['VOTE2VALUE']):
    button2 = os.environ['VOTE2VALUE']
else:
    button2 = app.config['VOTE2VALUE']

if ('TITLE' in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

# Redis Connection
r = redis.Redis()

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == 'true':
    title = socket.gethostname()

# Init Redis
if not r.get(button1):
    r.set(button1, 0)
if not r.get(button2):
    r.set(button2, 0)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        # Get current values
        vote1 = r.get(button1).decode('utf-8')
        # TODO: use tracer object to trace cat vote
        with tracer.span(name='Cats Vote'):
            print(f'Cats Vote')

            #tc.track_event('Cats Vote')
            # tc.flush()

        vote2 = r.get(button2).decode('utf-8')
        # TODO: use tracer object to trace dog vote
        with tracer.span(name='Dogs Vote'):
            print(f'Dogs Vote')

            #tc.track_event('Dogs Vote')
            # tc.flush()

        # Return index with values
        return render_template("index.html",
                               value1=int(vote1),
                               value2=int(vote2),
                               button1=button1,
                               button2=button2,
                               title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':

            # Empty table and return results
            r.set(button1, 0)
            r.set(button2, 0)

            vote1 = r.get(button1).decode('utf-8')
            properties = {'custom_dimensions': {'Cats Vote': vote1}}
            # TODO: use logger object to log cat vote
            logger.info('Cats Vote', extra=properties)

            vote2 = r.get(button2).decode('utf-8')
            properties = {'custom_dimensions': {'Dogs Vote': vote2}}
            # TODO: use logger object to log dog vote
            logger.info('Dogs Vote', extra=properties)

            return render_template("index.html",
                                   value1=int(vote1),
                                   value2=int(vote2),
                                   button1=button1,
                                   button2=button2,
                                   title=title)

        else:

            # Insert vote result into DB
            vote = request.form['vote']
            r.incr(vote, 1)

            # Get current values
            vote1 = r.get(button1).decode('utf-8')
            properties = {'custom_dimensions': {'Cats Vote': vote1}}
            # TODO: use logger object to log cat vote
            logger.info('Cats Vote', extra=properties)

            #tc.track_event('Cats Vote')
            # tc.flush()

            vote2 = r.get(button2).decode('utf-8')
            properties = {'custom_dimensions': {'Dogs Vote': vote2}}
            # TODO: use logger object to log dog vote
            logger.info('Dogs Vote', extra=properties)

            #tc.track_event('Dogs Vote')
            # tc.flush()

            # Return results
            return render_template('index.html',
                                   value1=int(vote1),
                                   value2=int(vote2),
                                   button1=button1,
                                   button2=button2,
                                   title=title)


if __name__ == '__main__':
    # comment line below when deploying to VMSS
    #app.run()  # local
    
    # uncomment the line below before deployment to VMSS
    app.run(host='0.0.0.0', threaded=True, debug=True) # remote
