# import the necessary libraries
# - need boto3 for AWS API
# - use JSON to do all JSON processing
# - need datetime for checking current time


# define the tag key/value pair to look for
#   Name: SchedulerStartTime
#   Value: 0-23 (any other value is considered invalid)
#
#   Name: SchedulerStopTime
#   Value: 0-23 (any other value is considered invalid)


# main processing:
#   process all instances
#   return status code and message

# process all instances:
#   get a list of instances with start time and stop time tags
#   get the current hour in the correct time zone
#   for each instance:
#       - if it is running
#           - if the current hour == stop time
#               - stop the instance
#       - if it is stopped
#           - if the current hour == start time
#               - start the instance
#       - in all other cases, do nothing

