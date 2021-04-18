import boto3
from pprint import  pprint
MemberTable=None

def InitDataBase():
    global MemberTable
    dynamodb=boto3.resource('dynamodb')
    MemberTable=dynamodb.Table('GuildMembers')


def GetMemberAttribute(AttributeKey,MemberObject):
    global MemberTable
    GuildID=MemberObject.guild.id
    MemberID=MemberObject.id
    response = MemberTable.get_item(
        Key={
            'MemberId': MemberID,
            'GuildId': GuildID
        }
    )
    #pprint(response)
    if "Item" in response.keys() and  AttributeKey in response["Item"].keys():
        return response["Item"][AttributeKey]
    else:
        return None


def SetMemberAttribute(AttributeKey,MemberObject,AttributeValue):
    global MemberTable
    GuildID=MemberObject.guild.id
    MemberID=MemberObject.id
    response = MemberTable.update_item(
        Key={
            'MemberId': MemberID,
            'GuildId': GuildID
        },
        UpdateExpression="set "+AttributeKey+"=:val",
        ExpressionAttributeValues={
            ':val': AttributeValue
        },
        ReturnValues="UPDATED_NEW"
    )
    #pprint(response)


def GetAllMemberData(MemberObject):
    global MemberTable
    GuildID=MemberObject.guild.id
    MemberID=MemberObject.id
    response = MemberTable.get_item(
        Key={
            'MemberId': MemberID,
            'GuildId': GuildID
        }
    )
    return response["Item"]
InitDataBase()


