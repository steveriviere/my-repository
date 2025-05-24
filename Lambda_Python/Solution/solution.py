'''
Required imports.
- boto3 for AWS
- json for all JSON processing
- datetime to get the current time
'''
import boto3
from datetime import datetime


'''
Define the tag key values which will determine if the instance needs to be 
stopped and/or started.  If the instance doesn't have these tags, the
scheduler will ignore the instance
'''
label_start_time = "SchedulerStartTime"
label_stop_time = "SchedulerStopTime"
labels_to_find = [label_start_time, label_stop_time]

'''
Define the ec2 boto3 client which we can use as needed
'''
ec2 = boto3.client('ec2')


'''
Get the current hour use datetime module
'''
def get_current_hour():

    now = datetime.now()
    current_hour = int(now.strftime("%H"))
    print(f"Current hour is: {current_hour}")
    return current_hour




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
    value = None
    for tag in tags:
        tag_key = tag['Key']
        if tag_key == key_to_find:
            value = tag['Value']
        if value is not None:
            break

    return value


'''
Return a list of all of the instances that have the keys specified
'''
def get_instances_with_tag(list_of_keys):

    # The definition of the request to and response from describe_instances
    # is in the boto3 documentation.
    instances = None
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': list_of_keys
            }
        ]
    )

    # The response, like most boto3 responses, is either a list
    # or dictionary. In this case, a "list" of "reservations"
    if len(response['Reservations']) > 0:
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
    instance_id = instance['InstanceId']
    instance_state = instance['State']['Name']
    instance_tags = instance['Tags']

    # print the instance id
    print(f"Checking instance {instance_id}")

    # set the default result to 'No action required for <instance id>'
    # if action is required, change the message later on
    result = f"No action required for {instance_id}"

    if instance_state == "running":
        # if instance is running and stop_time is now, stop it
        stop_time = get_instance_tag_value(label_stop_time, instance_tags)
        if int(stop_time) == current_hour:
            result = f"Stopping instance {instance_id}"
            ec2.stop_instances(InstanceIds=[instance_id])
    elif instance_state == "stopped":
        # if instance is stopped and start_time is now, start it
        start_time = get_instance_tag_value(label_start_time, instance_tags)
        if int(start_time) == current_hour:
            result = f"Starting instance {instance_id}"
            ec2.start_instances(InstanceIds=[instance_id])

    return result

'''
Get the list of all instances that have the start and stop tags, 
then process those instances.
'''
def process_instances(instances, current_hour):


    print(f"Found {len(instances)} instances to process")

    # process each instance
    for instance in instances:
        message = process_instance(instance, current_hour)
        print(message)
    return_status = "Finished processing all instances."

    return return_status

'''
Main lambda_handler.  This Lambda function should be triggered on a schedule.
We can ignore the event and context input variables.
'''
def lambda_handler(event, context):

    try:
        # get a list of all the instances with the required tags
        instances = get_instances_with_tag(labels_to_find)

        if instances is None:
            # we don't need to continue if there are no instances
            status_msg = "No instances to process"

        else:
            # get the current hour
            current_hour = get_current_hour()
            status_msg = process_instances(instances, current_hour)

    except Exception as e:
        status_msg = f"Unexpected error occured: {e}"

    finally:
        print(status_msg)
        return status_msg


'''
This is put in for testing from the IDE.  If this function is not running as a
Lambda function, then __name__ will be "__main__" and we can brute force call
the lambda_handler.
'''
if __name__ == "__main__":
    lambda_handler(None, None)

