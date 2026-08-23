

# GetActivityTask
<a name="API_GetActivityTask"></a>

Used by workers to retrieve a task (with the specified activity ARN) which has been scheduled for execution by a running state machine. This initiates a long poll, where the service holds the HTTP connection open and responds as soon as a task becomes available (i.e. an execution of a task of this type is needed.) The maximum time the service holds on to the request before responding is 60 seconds. If no task is available within 60 seconds, the poll returns a `taskToken` with a null string.

**Important**  
Workers should set their client side socket timeout to at least 65 seconds (5 seconds higher than the maximum time the service may hold the poll request).  
Polling with `GetActivityTask` can cause latency in some implementations. See [Avoid Latency When Polling for Activity Tasks](https://docs.aws.amazon.com/step-functions/latest/dg/bp-activity-pollers.html) in the Step Functions Developer Guide.

## Request Syntax
<a name="API_GetActivityTask_RequestSyntax"></a>

```
{
   "activityArn": "{{string}}",
   "workerName": "{{string}}"
}
```

## Request Parameters
<a name="API_GetActivityTask_RequestParameters"></a>

For information about the parameters that are common to all actions, see [Common Parameters](CommonParameters.md).

The request accepts the following data in JSON format.

 ** [activityArn](#API_GetActivityTask_RequestSyntax) **   <a name="StepFunctions-GetActivityTask-request-activityArn"></a>
The Amazon Resource Name (ARN) of the activity to retrieve tasks from (assigned when you create the task using [CreateActivity](API_CreateActivity.md).)  
Type: String  
Length Constraints: Minimum length of 1. Maximum length of 256.  
Required: Yes

 ** [workerName](#API_GetActivityTask_RequestSyntax) **   <a name="StepFunctions-GetActivityTask-request-workerName"></a>
You can provide an arbitrary name in order to identify the worker that the task is assigned to. This name is used when it is logged in the execution history.  
Type: String  
Length Constraints: Minimum length of 1. Maximum length of 80.  
Required: No

## Response Syntax
<a name="API_GetActivityTask_ResponseSyntax"></a>

```
{
   "input": "string",
   "taskToken": "string"
}
```

## Response Elements
<a name="API_GetActivityTask_ResponseElements"></a>

If the action is successful, the service sends back an HTTP 200 response.

The following data is returned in JSON format by the service.

 ** [input](#API_GetActivityTask_ResponseSyntax) **   <a name="StepFunctions-GetActivityTask-response-input"></a>
The string that contains the JSON input data for the task. Length constraints apply to the payload size, and are expressed as bytes in UTF-8 encoding.  
Type: String  
Length Constraints: Maximum length of 1048576.

 ** [taskToken](#API_GetActivityTask_ResponseSyntax) **   <a name="StepFunctions-GetActivityTask-response-taskToken"></a>
A token that identifies the scheduled task. This token must be copied and included in subsequent calls to [SendTaskHeartbeat](API_SendTaskHeartbeat.md), [SendTaskSuccess](API_SendTaskSuccess.md) or [SendTaskFailure](API_SendTaskFailure.md) in order to report the progress or completion of the task.  
Type: String  
Length Constraints: Minimum length of 1. Maximum length of 2048.

## Errors
<a name="API_GetActivityTask_Errors"></a>

For information about the errors that are common to all actions, see [Common Error Types](CommonErrors.md).

 ** ActivityDoesNotExist **   
The specified activity does not exist.  
HTTP Status Code: 400

 ** ActivityWorkerLimitExceeded **   
The maximum number of workers concurrently polling for activity tasks has been reached.  
HTTP Status Code: 400

 ** InvalidArn **   
The provided Amazon Resource Name (ARN) is not valid.  
HTTP Status Code: 400

 ** KmsAccessDeniedException **   
Either your AWS KMS key policy or API caller does not have the required permissions.  
HTTP Status Code: 400

 ** KmsInvalidStateException **   
The AWS KMS key is not in valid state, for example: Disabled or Deleted.    
 ** kmsKeyState **   
Current status of the AWS KMS; key. For example: `DISABLED`, `PENDING_DELETION`, `PENDING_IMPORT`, `UNAVAILABLE`, `CREATING`.
HTTP Status Code: 400

 ** KmsThrottlingException **   
Received when AWS KMS returns `ThrottlingException` for a AWS KMS call that Step Functions makes on behalf of the caller.  
HTTP Status Code: 400

## See Also
<a name="API_GetActivityTask_SeeAlso"></a>

For more information about using this API in one of the language-specific AWS SDKs, see the following:
+  [AWS Command Line Interface V2](https://docs.aws.amazon.com/goto/cli2/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for .NET V4](https://docs.aws.amazon.com/goto/DotNetSDKV4/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for C\+\+](https://docs.aws.amazon.com/goto/SdkForCpp/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for Go v2](https://docs.aws.amazon.com/goto/SdkForGoV2/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for Java V2](https://docs.aws.amazon.com/goto/SdkForJavaV2/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for JavaScript V3](https://docs.aws.amazon.com/goto/SdkForJavaScriptV3/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for Kotlin](https://docs.aws.amazon.com/goto/SdkForKotlin/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for PHP V3](https://docs.aws.amazon.com/goto/SdkForPHPV3/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for Python](https://docs.aws.amazon.com/goto/boto3/states-2016-11-23/GetActivityTask) 
+  [AWS SDK for Ruby V3](https://docs.aws.amazon.com/goto/SdkForRubyV3/states-2016-11-23/GetActivityTask) 