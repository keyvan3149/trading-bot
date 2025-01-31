import ccxt

# اطلاعات API خود را وارد کنید
api_key = "9245e98c-4172-48bc-b26d-7a9cec40cbd5"
secret_key = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAM1ODpvOvUsyFRcZqdBmCMxYom0/8rAc/zrLHsUiJT7iygEopHb/UQNAX8z34U8Nz0qkvYMnsIEVHsOJ15IuEiXodJlmC88RHi0mbqovVZiBfMCVQySWfDnsWuB5K0CAax7c9VicsOi/MV1985SWQihFF0XLbC1b7KsWammc3PVnAgMBAAECgYEAjN9XpM+KEdPOpugkHmw080qKQV6UvwVWmFgRyACy/+CL7ZmeqExuoUWFttYL0rvOFhDOPPV55kjAsDmgIpzcM84bPiaPj3XMRshGNT7pIJ+CaRbUPcyK7bVKVdCRwQwEDgmcUTdxTQS+U/kk1QR3Do2lAQUiq5+7TPE1HybHutkCQQDmad4TzLC939CKUITsuPujj3vDxjJ4qGmK5P7eHCcF7vdJR60Pl+CwOT4TTjW2fvKvMnRuMcCGyRN23aZ50tJDAkEA5Bpog8gGVWiKzFSJkpIkAUGXz/u4mPtE+VJXKDb1AvmocmnNKbLHwJJR3okfOJe9KViIJHeLZR3IIm1dRqYYDQJBAKtdtaN4K0MsgMc+F36QHeeJwXzbnZILf2Oj6MJ8obFSB2zi+B2O0bd++2IUWvJ9/DS9C8chDZWxWt6e/z+/wk0CQEvEfdzwLzJlhF0043GdO3pzWEMMoRentxR+BldkUeRIG2zNuglUykcsEyexMn6w4HOAZdB/KP1QdC8DVs1l1G0CQDN1K1GPzIs1TU+NqrQk7PTHwUhs/r/grvQpBESj6cOIOcr0HAQzshMvKglyVNufrHXhnwj1ZC7SueE+eKJhe2k="

# اتصال به صرافی LBank
exchange = ccxt.lbank({
    "apiKey": api_key,
    "secret": secret_key
})

try:
    # تست اتصال و نمایش موجودی
    exchange.load_markets()
    balance = exchange.fetch_balance()
    print("اتصال موفق! موجودی:")
    print(balance)
except Exception as e:
    print(f"خطا: {e}")
