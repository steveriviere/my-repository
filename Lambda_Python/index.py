'''
Required imports.
- boto3 for AWS
- datetime to get the current time
'''
import boto3
from datetime import datetime


'''
Define the tag key values which will determine if the instance needs to be 
stopped and/or started.  If the instance doesn't have these tags, the
scheduler will ignore the instance
'''
start_time_tag="SchedulerStartTime"
stop_time_tag="SchedulerStopTime"
scheduler_tags=[start_time_tag,stop_time_tag]

'''
Define the ec2 boto3 client which we can use as needed
'''
ec2_client=boto3.client('ec2')

'''
Get the current hour use datetime module
'''
def get_current_hour():
    current_time = datetime.now()
    current_hour = current_time.strftime("%-H")
    print(f"Current time: {current_hour}")

    return int(current_hour)




'''
Function to takes a specific key as input and determine the associated value
if it exists in the instance tags
'''
def get_instance_tag_value(key_to_find, tags):

    # "tags" is a LIST of key / value pairs that look like this:
    # - Key: FirstKey
    #   Value: FirstValue
    # - Key: SecondKey
    #   Value: SecondValue
    # - Key: SchedulerStartTime
    #   Value: 8
    # - Key: SchedulerStopTime
    #   Value: 18
    # We are looking for the VALUE when the Key is equal to the 'key_to_find' passed
    # into the function

    val = -1
    for tag in tags:
        if tag["Key"] == key_to_find:
            val = tag["Value"]

    return int(val)


'''
Return a list of all of the instances that have the keys specified
'''
def get_instances_with_tag(list_of_keys):

    # The definition of the request to and response from describe_instances
    # is in the boto3 ec2 documentation.
    #important, read it to understand below
    response=ec2_client.describe_instances(Filters=[{'Name': 'tag-key','Values': list_of_keys}])


    # The response, like most boto3 responses, is either a list
    # or dictionary. In this case, a "list" of "reservations"
    instances = response['Reservations'][0]['Instances']


    return instances


'''
Decide what to do with an instance, given the instance state and current time:
- if instance is running and stop_time is now, stop it
- if instance is stopped and start_time is now, start it
- in all other cases, leave the instance as is
'''
def process_instance(instance, current_hour):

    # "instance" is defined in the boto3 documentation
    # it is made up of key/value pairs
    # we need to extract the instance_id, instance_state, instance_tags
    # to do this, check the documentation for "ec2 boto3"

    # print the instance id
    instance_state = instance['State']['Name']
    instance_tags = instance['Tags']
    instance_id = instance['InstanceId']

    print (f" instance_id: {instance_id} and instance_state: {instance_state} and instance_tags: {instance_tags}")


    # set the default result to 'No action required for <instance id>'
    # if action is required, change the message later on
    result= f"No action required for instance {instance_id} in state {instance_state}"

    if instance_state == "running":
        # if instance is running and stop_time is now, stop it
        stop_time=get_instance_tag_value(stop_time_tag, instance_tags)
        if stop_time == current_hour:
            # stop it
            ec2_client.stop_instances(InstanceIds=[instance_id,])

            result=f" stopping instance {instance_id} "


    elif instance_state == "stopped":
        # if instance is stopped and start_time is now, start it
        start_time=get_instance_tag_value(start_time_tag, instance_tags)
        if start_time == current_hour:
            #start ig
            ec2_client.start_instances(InstanceIds=[instance_id, ])
            result=f" starting instance {instance_id} "


    return result

'''
Get the list of all instances that have the start and stop tags, 
then process those instances.
'''
def process_instances(instances, current_hour):

    # process each instance

    for instance in instances:
        status = process_instance(instance, current_hour)
        print(f"status {status} of {instance['InstanceId']}")

    return "Done processing all instances"


'''
Main lambda_handler.  This Lambda function should be triggered on a schedule.
We can ignore the event and context input variables.
'''
def lambda_handler(event, context):

    # get a list of all the instances with the required tags
    instances = get_instances_with_tag(scheduler_tags)

    if len(instances) == 0:
        # we don't need to continue if there are no instances
        status_message = "No instances to process"
    else:
        # get the current hour
        curr_hour = get_current_hour()

        # process instances
        status_message = process_instances(instances, curr_hour)

    return status_message





'''
This is put in for testing from the IDE.  If this function is not running as a
Lambda function, then __name__ will be "__main__" and we can brute force call
the lambda_handler.
'''
if __name__ == "__main__":
    result=lambda_handler(None, None)
    print(result)


