# loggly-watch

This package provides a way to take facet searches run on your Loggly account and push the results to [Amazon's CloudWatch service](http://aws.amazon.com/cloudwatch/).  The results can be used for alerting on certain types of events occuring in the logs on your servers.

## Installation
Get started by installing the Python package 'hoover':

<pre>
  sudo apt-get install python-setuptools
  sudo easy_install hoover
</pre>

Download the package from Github by locally cloning the repository:

<pre>
  cd ~/
  git clone git@github.com:loggly/loggly-watch.git
</pre>

### Configuring
Next, you'll need to set your AWS key and private keys.  One way to do this is by editing your .profile and exporting them to the environment:

<pre>
  vim ~/.profile
  export AWS_ACCESS_KEY_ID=your_aws_key_goes_here
  export AWS_SECRET_ACCESS_KEY_ID=your_aws_secret_key_goes_here
</pre>

Or, you can just edit the line in the *main.py* file:
<pre>
  cw = cloudwatch.connection('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY_ID') 
</pre>

You'll also need to set your Loggly credentials:

<pre>
  hoover.authorize('ACCOUNT_NAME', 'USERNAME', 'PASSWORD')
</pre>

and set your namespace for your site:

<pre>
  namespace = 'Loggly'
</pre>

### Defining Searches
You'll need to configure a set of searches you want to run from Loggly.  Change 'default' to the Loggly input you want to search if it's.  

The example below gets counts of events matching the wildcard search for a five minute window starting six minutes ago for the default input.  Obviously this input needs to be receiving data from your web server to work.

<pre>
  account_name = hoover.utils.get_input_by_name('default')
  num_results = account_name.facets(q='*', starttime='NOW-6MINUTES', endtime='NOW-1MINUTE', buckets=1)['data'].items()[0][1]
</pre>

### Running
Run the code to test it.
<pre>
  python main.py
</pre>

Now set it up as a cron job:

<pre>
  crontab -e
  */5 * * * * python ~/loggly-watch/main.py
</pre>

You should get custom data flowing into your CloudWatch account after about 5-10 minutes.  Adjust your timeframes and cronjob as necessary, and add more searches for other use cases.

To graph the data on your own dashboard, use [Micahel Babineau's CloudViz package](https://github.com/mbabineau/cloudviz).
