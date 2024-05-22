import boto3
import pandas as pd
from datetime import datetime, timedelta

# Initialize a session using Amazon Lambda
session = boto3.Session(region_name='ap-southeast-1')  # specify your region
lambda_client = session.client('lambda')
cloudwatch_client = session.client('cloudwatch')

# Get the list of all Lambda functions
def get_lambda_functions():
    functions = []
    response = lambda_client.list_functions()
    functions.extend(response['Functions'])

    while 'NextMarker' in response:
        response = lambda_client.list_functions(Marker=response['NextMarker'])
        functions.extend(response['Functions'])

    return functions

# Get invocation metrics for a specific function
def get_invocation_metrics(function_name, start_time, end_time):
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Invocations',
        Dimensions=[
            {
                'Name': 'FunctionName',
                'Value': function_name
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # 1 day
        Statistics=['Sum']
    )

    if response['Datapoints']:
        return response['Datapoints'][0]['Sum']
    else:
        return 0

# Get duration metrics for a specific function
def get_duration_metrics(function_name, start_time, end_time):
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='Duration',
        Dimensions=[
            {
                'Name': 'FunctionName',
                'Value': function_name
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # 1 day
        Statistics=['Average']
    )

    if response['Datapoints']:
        return response['Datapoints'][0]['Average']
    else:
        return 0

# Get concurrent executions metrics for a specific function
def get_concurrent_executions_metrics(function_name, start_time, end_time):
    response = cloudwatch_client.get_metric_statistics(
        Namespace='AWS/Lambda',
        MetricName='ConcurrentExecutions',
        Dimensions=[
            {
                'Name': 'FunctionName',
                'Value': function_name
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,  # 1 day
        Statistics=['Maximum']
    )

    if response['Datapoints']:
        return response['Datapoints'][0]['Maximum']
    else:
        return 0

# Main function to retrieve and save Lambda function details and metrics to Excel
def main():
    functions = get_lambda_functions()

    if not functions:
        print("No Lambda functions found.")
        return
    
    # Define the time period for metrics
    # Define the time period for metrics (from May 13 to May 16)
    start_time = datetime(2024, 5, 17)
    end_time = datetime(2024, 5, 20) - timedelta(seconds=1)  # end time is exclusive

    data = []
    for function in functions:
        function_name = function['FunctionName']
        invocations = get_invocation_metrics(function_name, start_time, end_time)
        duration = get_duration_metrics(function_name, start_time, end_time)
        concurrent_executions = get_concurrent_executions_metrics(function_name, start_time, end_time)
        data.append({
            'FunctionName': function_name,
            'Runtime': function['Runtime'],
            'Handler': function['Handler'],
            'LastModified': function['LastModified'],
            'MemorySize': function['MemorySize'],
            'Timeout': function['Timeout'],
            'Description': function.get('Description', 'No description'),
            'Invocations (Last 7 days)': invocations,
            'Average Duration (ms) (Last 7 days)': duration,
            'Max Concurrent Executions (Last 7 days)': concurrent_executions
        })

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save to Excel
    df.to_excel('lambda_functions_with_metrics-17-20.xlsx', index=False)

    print("Lambda functions details and metrics saved to lambda_functions_with_metrics_17-20.xlsx")

if __name__ == '__main__':
    main()
