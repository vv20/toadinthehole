import aws_cdk as core
import aws_cdk.assertions as assertions

from stack.stack import ToadInTheHoleStack

def test_sqs_queue_created():
    app = core.App()
    stack = ToadInTheHoleStack(app, "dev")
    template = assertions.Template.from_stack(stack)
