from __future__ import annotations

from enum import Enum


class Result(Enum):
    """Steam error result codes.

    Attributes:
       OK (int): Success.
        FAIL (int): Generic failure.
        NOCONNECTION (int): Your Steam client doesn't have a connection to the back-end.
        INVALIDPASSWORD (int): Password/ticket is invalid.
        LOGGEDINELSEWHERE (int): The user is logged in elsewhere.
        INVALIDPROTOCOLVER (int): Protocol version is incorrect.
        INVALIDPARAM (int): A parameter is incorrect.
        FILENOTFOUND (int): File was not found.
        BUSY (int): Called method is busy - action not taken.
        INVALIDSTATE (int): Called object was in an invalid state.
        INVALIDNAME (int): The name was invalid.
        INVALIDEMAIL (int): The email was invalid.
        DUPLICATENAME (int): The name is not unique.
        ACCESSDENIED (int): Access is denied.
        TIMEOUT (int): Operation timed out.
        BANNED (int): The user is VAC2 banned.
        ACCOUNTNOTFOUND (int): Account not found.
        INVALIDSTEAMID (int): The Steam ID was invalid.
        SERVICEUNAVAILABLE (int): The requested service is currently unavailable.
        NOTLOGGEDON (int): The user is not logged on.
        PENDING (int): Request is pending, it may be in process or waiting on third party.
        ENCRYPTIONFAILURE (int): Encryption or Decryption failed.
        INSUFFICIENTPRIVILEGE (int): Insufficient privilege.
        LIMITEXCEEDED (int): Too much of a good thing.
        REVOKED (int): Access has been revoked (used for revoked guest passes.)
        EXPIRED (int): License/Guest pass the user is trying to access is expired.
        ALREADYREDEEMED (int): Guest pass has already been redeemed by account, cannot be used again.
        DUPLICATEREQUEST (int): The request is a duplicate and the action has already occurred in the past,
            ignored this time.
        ALREADYOWNED (int): All the games in this guest pass redemption request are already owned by the user.
        IPNOTFOUND (int): IP address not found.
        PERSISTFAILED (int): Failed to write change to the data store.
        LOCKINGFAILED (int): Failed to acquire access lock for this operation.
        LOGONSESSIONREPLACED (int): The logon session has been replaced.
        CONNECTFAILED (int): Failed to connect.
        HANDSHAKEFAILED (int): The authentication handshake has failed.
        IOFAILURE (int): There has been a generic IO failure.
        REMOTEDISCONNECT (int): The remote server has disconnected.
        SHOPPINGCARTNOTFOUND (int): Failed to find the shopping cart requested.
        BLOCKED (int): A user blocked the action.
        IGNORED (int): The target is ignoring sender.
        NOMATCH (int): Nothing matching the request found.
        ACCOUNTDISABLED (int): The account is disabled.
        SERVICEREADONLY (int): This service is not accepting content changes right now.
        ACCOUNTNOTFEATURED (int): Account doesn't have value, so this feature isn't available.
        ADMINISTRATOROK (int): Allowed to take this action, but only because requester is admin.
        CONTENTVERSION (int): A Version mismatch in content transmitted within the Steam protocol.
        TRYANOTHERCM (int): The current CM can't service the user making a request, user should try another.
        PASSWORDREQUIREDTOKICKSESSION (int): You are already logged in elsewhere,
            this cached credential login has failed.
        ALREADYLOGGEDINELSEWHERE (int): The user is logged in elsewhere. (Use LoggedInElsewhere instead!)
        SUSPENDED (int): Long running operation has suspended/paused. (eg. content download.)
        CANCELLED (int): Operation has been canceled, typically by user. (eg. a content download.)
        DATACORRUPTION (int): Operation canceled because data is ill formed or unrecoverable.
        DISKFULL (int): Operation canceled - not enough disk space.
        REMOTECALLFAILED (int): The remote or IPC call has failed.
        PASSWORDUNSET (int): Password could not be verified as it's unset server side.
        EXTERNALACCOUNTUNLINKED (int): External account (PSN, Facebook...) is not linked to a Steam account.
        PSNTICKETINVALID (int): PSN ticket was invalid.
        EXTERNALACCOUNTALREADYLINKED (int): External account (PSN, Facebook...) is already linked to some other account,
            must explicitly request to replace/delete the link first.
        REMOTEFILECONFLICT (int): The sync cannot resume due to a conflict between the local and remote files.
        ILLEGALPASSWORD (int): The requested new password is not allowed.
        SAMEASPREVIOUSVALUE (int): New value is the same as the old one. This is used for secret question and answer.
        ACCOUNTLOGONDENIED (int): Account login denied due to 2nd factor authentication failure.
        CANNOTUSEOLDPASSWORD (int): The requested new password is not legal.
        INVALIDLOGINAUTHCODE (int): Account login denied due to auth code invalid.
        ACCOUNTLOGONDENIEDNOMAIL (int): Account login denied due to 2nd factor auth failure - and no mail has been sent.
        HARDWARENOTCAPABLEOFIPT (int): The users hardware does not support Intel's Identity Protection Technology (IPT).
        IPTINITERROR (int): Intel's Identity Protection Technology (IPT) has failed to initialize.
        PARENTALCONTROLRESTRICTED (int): Operation failed due to parental control restrictions for current user.
        FACEBOOKQUERYERROR (int): Facebook query returned an error.
        EXPIREDLOGINAUTHCODE (int): Account login denied due to an expired auth code.
        IPLOGINRESTRICTIONFAILED (int): The login failed due to an IP restriction.
        ACCOUNTLOCKEDDOWN (int): The current users account is currently locked for use.
            This is likely due to a hijacking and pending ownership verification.
        ACCOUNTLOGONDENIEDVERIFIEDEMAILREQUIRED (int): The logon failed because the accounts email is not verified.
        NOMATCHINGURL (int): There is no URL matching the provided values.
        BADRESPONSE (int): Bad Response due to a Parse failure, missing field, etc.
        REQUIREPASSWORDREENTRY (int): The user cannot complete the action until they re-enter their password.
        VALUEOUTOFRANGE (int): The value entered is outside the acceptable range.
        UNEXPECTEDERROR (int): Something happened that we didn't expect to ever happen.
        DISABLED (int): The requested service has been configured to be unavailable.
        INVALIDCEGSUBMISSION (int): The files submitted to the CEG server are not valid.
        RESTRICTEDDEVICE (int): The device being used is not allowed to perform this action.
        REGIONLOCKED (int): The action could not be complete because it is region restricted.
        RATELIMITEXCEEDED (int): Temporary rate limit exceeded, try again later,
            different from LimitExceeded which may be permanent.
        ACCOUNTLOGINDENIEDNEEDTWOFACTOR (int): Need two-factor code to login.
        ITEMDELETED (int): The thing we're trying to access has been deleted.
        ACCOUNTLOGINDENIEDTHROTTLE (int): Login attempt failed, try to throttle response to possible attacker.
        TWOFACTORCODEMISMATCH (int): Two factor authentication (Steam Guard) code is incorrect.
        TWOFACTORACTIVATIONCODEMISMATCH (int): The activation code for two-factor
            authentication (Steam Guard) didn't match.
        ACCOUNTASSOCIATEDTOMULTIPLEPARTNERS (int): The current account has been associated with multiple partners.
        NOTMODIFIED (int): The data has not been modified.
        NOMOBILEDEVICE (int): The account does not have a mobile device associated with it.
        TIMENOTSYNCED (int): The time presented is out of range or tolerance.
        SMSCODEFAILED (int): SMS code failure - no match, none pending, etc.
        ACCOUNTLIMITEXCEEDED (int): Too many accounts access this resource.
        ACCOUNTACTIVITYLIMITEXCEEDED (int): Too many changes to this account.
        PHONEACTIVITYLIMITEXCEEDED (int): Too many changes to this phone.
        REFUNDTOWALLET (int): Cannot refund to payment method, must use wallet.
        EMAILSENDFAILURE (int): Cannot send an email.
        NOTSETTLED (int): Can't perform operation until payment has settled.
        NEEDCAPTCHA (int): The user needs to provide a valid captcha.
        GSLTDENIED (int): A game server login token owned by this token's owner has been banned.
        GSOWNERDENIED (int): Game server owner is denied for some other reason such as account locked,
            community ban, vac ban, missing phone, etc.
        INVALIDITEMTYPE (int): The type of thing we were requested to act on is invalid.
        IPBANNED (int): The IP address has been banned from taking this action.
        GSLTEXPIRED (int): This Game Server Login Token (GSLT) has expired from disuse; it can be reset for use.
        INSUFFICIENTFUNDS (int): user doesn't have enough wallet funds to complete the action
        TOOMANYPENDING (int): There are too many of this thing pending already
    """

    OK = 1
    FAIL = 2
    NOCONNECTION = 3
    INVALIDPASSWORD = 5
    LOGGEDINELSEWHERE = 6
    INVALIDPROTOCOLVER = 7
    INVALIDPARAM = 8
    FILENOTFOUND = 9
    BUSY = 10
    INVALIDSTATE = 11
    INVALIDNAME = 12
    INVALIDEMAIL = 13
    DUPLICATENAME = 14
    ACCESSDENIED = 15
    TIMEOUT = 16
    BANNED = 17
    ACCOUNTNOTFOUND = 18
    INVALIDSTEAMID = 19
    SERVICEUNAVAILABLE = 20
    NOTLOGGEDON = 21
    PENDING = 22
    ENCRYPTIONFAILURE = 23
    INSUFFICIENTPRIVILEGE = 24
    LIMITEXCEEDED = 25
    REVOKED = 26
    EXPIRED = 27
    ALREADYREDEEMED = 28
    DUPLICATEREQUEST = 29
    ALREADYOWNED = 30
    IPNOTFOUND = 31
    PERSISTFAILED = 32
    LOCKINGFAILED = 33
    LOGONSESSIONREPLACED = 34
    CONNECTFAILED = 35
    HANDSHAKEFAILED = 36
    IOFAILURE = 37
    REMOTEDISCONNECT = 38
    SHOPPINGCARTNOTFOUND = 39
    BLOCKED = 40
    IGNORED = 41
    NOMATCH = 42
    ACCOUNTDISABLED = 43
    SERVICEREADONLY = 44
    ACCOUNTNOTFEATURED = 45
    ADMINISTRATOROK = 46
    CONTENTVERSION = 47
    TRYANOTHERCM = 48
    PASSWORDREQUIREDTOKICKSESSION = 49
    ALREADYLOGGEDINELSEWHERE = 50
    SUSPENDED = 51
    CANCELLED = 52
    DATACORRUPTION = 53
    DISKFULL = 54
    REMOTECALLFAILED = 55
    PASSWORDUNSET = 56
    EXTERNALACCOUNTUNLINKED = 57
    PSNTICKETINVALID = 58
    EXTERNALACCOUNTALREADYLINKED = 59
    REMOTEFILECONFLICT = 60
    ILLEGALPASSWORD = 61
    SAMEASPREVIOUSVALUE = 62
    ACCOUNTLOGONDENIED = 63
    CANNOTUSEOLDPASSWORD = 64
    INVALIDLOGINAUTHCODE = 65
    ACCOUNTLOGONDENIEDNOMAIL = 66
    HARDWARENOTCAPABLEOFIPT = 67
    IPTINITERROR = 68
    PARENTALCONTROLRESTRICTED = 69
    FACEBOOKQUERYERROR = 70
    EXPIREDLOGINAUTHCODE = 71
    IPLOGINRESTRICTIONFAILED = 72
    ACCOUNTLOCKEDDOWN = 73
    ACCOUNTLOGONDENIEDVERIFIEDEMAILREQUIRED = 74
    NOMATCHINGURL = 75
    BADRESPONSE = 76
    REQUIREPASSWORDREENTRY = 77
    VALUEOUTOFRANGE = 78
    UNEXPECTEDERROR = 79
    DISABLED = 80
    INVALIDCEGSUBMISSION = 81
    RESTRICTEDDEVICE = 82
    REGIONLOCKED = 83
    RATELIMITEXCEEDED = 84
    ACCOUNTLOGINDENIEDNEEDTWOFACTOR = 85
    ITEMDELETED = 86
    ACCOUNTLOGINDENIEDTHROTTLE = 87
    TWOFACTORCODEMISMATCH = 88
    TWOFACTORACTIVATIONCODEMISMATCH = 89
    ACCOUNTASSOCIATEDTOMULTIPLEPARTNERS = 90
    NOTMODIFIED = 91
    NOMOBILEDEVICE = 92
    TIMENOTSYNCED = 93
    SMSCODEFAILED = 94
    ACCOUNTLIMITEXCEEDED = 95
    ACCOUNTACTIVITYLIMITEXCEEDED = 96
    PHONEACTIVITYLIMITEXCEEDED = 97
    REFUNDTOWALLET = 98
    EMAILSENDFAILURE = 99
    NOTSETTLED = 100
    NEEDCAPTCHA = 101
    GSLTDENIED = 102
    GSOWNERDENIED = 103
    INVALIDITEMTYPE = 104
    IPBANNED = 105
    GSLTEXPIRED = 106
    INSUFFICIENTFUNDS = 107
    TOOMANYPENDING = 108
