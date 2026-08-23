

# Integrating services with Step Functions
<a name="integrate-services"></a>

Learn how to integrate AWS services and call HTTPS APIs with Step Functions. With service integrations, your workflows can coordinate resources and orchestrate your business processes. 

Depending on workflow type and availability, your workflows call services using one of three service integration patterns:
+ Request a Response (default) - wait for HTTP response, then go to the next state
+ Run a Job (`.sync`) - wait for the job to complete
+ Wait for Callback (`.waitForTaskToken`) - pause a workflow until a task token is returned

To learn more, see [Service integration patterns](connect-to-resource.md). And to learn more about controlling the flow of data to your integrated services, see [Passing parameters to a service API in Step Functions](connect-parameters.md).

## AWS SDK integrations
<a name="connect-to-services-awssdk"></a>

AWS SDK integrations work exactly like an API call using the AWS SDK.

Using [AWS SDK integrations](supported-services-awssdk.md), your state machines can call over nine thousand API actions for over two hundred AWS services.

**Example integrations you might use:**  
+ Invoke a AWS Lambda function.
+ Run an AWS Batch job and take different actions based on the results.
+ Retrieve or updated items in Amazon DynamoDB.
+ Run an Amazon Elastic Container Service (Amazon ECS) task and wait for it to complete.
+ Publish to a topic in Amazon Simple Notification Service (Amazon SNS).
+ Send a message in Amazon Simple Queue Service (Amazon SQS).
+ Manage a job for AWS Glue or Amazon SageMaker AI.
+ Build workflows for executing Amazon EMR jobs.
+ Launch another AWS Step Functions workflow execution.

## Optimized integrations
<a name="connect-to-services-optimized"></a>

In addition to standard integrations, Step Functions provides optimized integrations which provide enhanced functionality. Optimized integrations have been customized by Step Functions to provide an improved developer experience when integrating the service in a workflow context.

For example, the optimized [Lambda `Invoke`](connect-lambda.md) automatically converts API output from escaped JSON to a JSON object which you can more easily use. Another example is how [AWS Batch`SubmitJob`](connect-batch.md) can pause execution until the batch job completes, which is a common scenario.

When possible, we **recommend** using the optimized integrations.

For the full list of optimized integrations, see the dedicated chapter for [Integrating optimized services with Step Functions](integrate-optimized.md)

## Call HTTPS APIs
<a name="connect-to-services-https"></a>

An HTTP Task is a type of [Task workflow state](state-task.md) state that you can use to call HTTPS APIs in your workflows. The API can be public, such as third-party SaaS applications like Stripe or Salesforce. You can also call private API, such as HTTPS-based applications in an Amazon Virtual Private Cloud.

For more information, see [Call HTTPS APIs in Step Functions workflows](call-https-apis.md).