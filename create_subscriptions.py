import boto3
import click


@click.command()
@click.argument('sns_topic_arn')
@click.argument('path_to_phone_number_list')
def run(sns_topic_arn, path_to_phone_number_list):
    sns_client = boto3.client('sns')

    list_sub_params = {'TopicArn': sns_topic_arn}
    current_subscriptions = []
    while True:
        list_sub_resp = sns_client.list_subscriptions_by_topic(
            **list_sub_params
        )
        current_subscriptions.extend(list_sub_resp['Subscriptions'])
        if 'NextToken' in list_sub_resp:
            list_sub_params['NextToken'] = list_sub_resp['NextToken']
        else:
            break
    current_phone_numbers = dict(
        (s['Endpoint'], s['SubscriptionArn'])
        for s in current_subscriptions
        if s['Protocol'] == 'sms'
    )

    phone_numbers = []
    with open(path_to_phone_number_list) as phone_number_list_f:
        for dirty_phone_number in phone_number_list_f.readlines():
            phone_number = dirty_phone_number.strip()
            phone_numbers.append(
                phone_number
                if phone_number.startswith('+886')
                else '+886' + phone_number[1:]
            )

    # Subscribe new phone numbers
    for new_phone_number in set(phone_numbers) - set(
        current_phone_numbers.keys()
    ):
        sns_client.subscribe(
            TopicArn=sns_topic_arn, Protocol='sms', Endpoint=new_phone_number
        )

    # Unsubscribe old phone numbers
    for old_phone_number in set(current_phone_numbers.keys()) - set(
        phone_numbers
    ):
        sns_client.unsubscribe(
            SubscriptionArn=current_phone_numbers[old_phone_number]
        )


if __name__ == '__main__':
    run()
