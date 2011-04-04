import cloudwatch
import httplib2, simplejson
import hoover
from hoover import utils

# init our connection to cloudwatch
cw = cloudwatch.connection('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY_ID') 

# init our connection to loggly
hoover.authorize('geekceo', 'kordless', 'password')

# cloudwatch namespace
namespace = 'Loggly'

# get back the number of events for the website
geekceo = hoover.utils.get_input_by_name('default')
num_results = geekceo.facets(q='*', starttime='NOW-6MINUTES', endtime='NOW-1MINUTE', buckets=1)['data'].items()[0][1]
# push it to cloudwatch
cw.putData(namespace, "WebEventCount", num_results)

# get back the number of 404s for the website
geekceo = hoover.utils.get_input_by_name('loggly_web')
num_results = geekceo.facets(q='GET AND 404', starttime='NOW-6MINUTES', endtime='NOW-1MINUTE', buckets=1)['data'].items()[0][1]
# push it to cloudwatch
cw.putData(namespace, "404Count", num_results)




