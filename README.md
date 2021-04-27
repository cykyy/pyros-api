# pyros-api
## A simplified routerOS api in python!
```
Thanks to Social WiFi for their incredible RouterOS-api
```
pyros-api is a simple python api for [MikroTik](https://mikrotik.com/) RouterOS extended from [RouterOS-api](https://github.com/socialwifi/RouterOS-api). \
pyros-api on [PyPi](https://pypi.org/project/pyros-api/)

### Why Another API?
Well, I find the routeros-api by socialwifi (their api is great!) is complicated unless you are well familiar with routerOS.\
Though I was somewhat familiar with routerOS I still needed to often search on google and play with winbox/cli to do a simple stuff. \
And the most embarrassing part is I used to often forget what I did to achieve something let's say a day ago If I deleted or needed to implement the same logic with a bit of twist.\
That's where this wrapper comes in. There's not many functions are covered so far but I will be working on this and will update with more simplified api. Any contribution is welcome.


## Usage
`pip install pyros-api`

### Connection

```python
#!/usr/bin/python

import pyros_api

connection = pyros_api.RosCall('Mikrotik IP', username='admin', password='')
connection.login()
connection.get_ppp_secret()
```

#### Connect Options

```python
pyros_api.RosCall(
    host,
    username='admin',
    password='',
    port=8728,
    use_ssl=False,
    ssl_verify=True,
    ssl_verify_hostname=True,
    ssl_context=None,
)
```

Parameters:

* `host` - String - Hostname or IP of device

Optional Parameters:

* `username` - String - Login username - Default 'admin'
* `password` - String - Login password - Default empty string
* `port` - Integer - TCP Port for API - Default 8728 or 8729 when using SSL
* `plaintext_login` - Boolean - Try plaintext login (for RouterOS 6.43 onwards) - Default **False**
* `use_ssl` - Boolean - Use SSL or not? - Default **False**
* `ssl_verify` - Boolean - Verify the SSL certificate? - Default **True**
* `ssl_verify_hostname` - Boolean - Verify the SSL certificate hostname matches? - Default **True**
* `ssl_context` - Object - Pass in a custom SSL context object. Overrides other options. - Default **None**

#### Using SSL

If we want to use SSL, we can simply specify `use_ssl` as `True`:

```python
connection = pyros_api.RosCall('<IP>', username='admin', password='', use_ssl=True)
connection.login()
```

This will automatically verify SSL certificate and hostname. 
The most flexible way to modify SSL parameters is to provide an SSL Context object using the 
`ssl_context` parameter, but for typical use-cases with self-signed certificates, the shorthand options of
 `ssl_verify` and `ssl_verify_hostname` are provided.

e.g. if using a self-signed certificate, you can (but probably shouldn't) use:

```python
connection = pyros_api.RosCall(
    '<IP>',
    username='admin',
    password='',
    use_ssl=True,
    ssl_verify=False,
    ssl_verify_hostname=False,
)
```

#### Login for RouterOS v6.43 onwards

RouterOS Versions v6.43 onwards now use a different login method. 
The disadvantage is that it passes the password in plain text. 
For security we only attempt the plaintext login if requested using the `plaintext_login` parameter. 
It is highly recommended only to use this option with SSL enabled.

```python
pyros_api.RosCall(host, username='admin', password='', plaintext_login=True)
connection.login()
```

### Execute Commands

After successfully connecting with routerOS you can call all the available functions.

### Examples
```python
x = connection.get_ppp_secret()
print(x)  # print list of all ppp secrets from routerOS
```

```python
# changes password of given ppp secret. e.g.: secret = 'abc1 & password = '1234'
x = connection.update_secret_password(secret, password)
```

#### Create New PPP Secret
```
secret = {
    'c_ident': '',
    'p_pw': '',
    'profile': 'default',
    'service_type': 'pppoe',
    'comment': '',
    'has_suspended': False
 }
```
Secret Dictionary Key-Value Pair:

* `c_ident` - String - PPP secret name (e.g: abc1) - Default empty string

Optional Keys:

* `p_pw` - String - PPP secret password - Default empty string
* `profile` - String - PPP secret profile - Default 'default' profile
* `service_type` - String - PPP secret service type (e.g: pptp/any/pppe) - Default pppoe
* `comment` - String - PPP secret comment - Default empty string
* `has_suspended` - Boolean - PPP secret state after creation (e.g: if True then after creating the secret the ppp secret will be disabled) - Default **False**
##### Example
```python
secret = {
    'c_ident': 'abc5',
    'p_pw': '1234',
    'profile': 'default',
    'service_type': 'pppoe',
    'comment': 'This is a dummy comment!',
    'has_suspended': False
}
connection.add_ppp_secret(secret)  # returns True if successfully created
```

### Close conection:

```python
connection.disconnect()
```

## socialWifi's routerOS-api API's

Everything from the routerOS-api by socialWifi is also available by invoking the given function.
```
api = connection.ros_api_raw()
```
Now we can access all the functions from the routerOS-api by socialWifi.
#### Example
```
api = connection.ros_api_raw()
list_ppp = api.get_resource('/ppp/secret')
print(list_ppp.get())  # prints all ppp secrets
```
To learn more about how to access API's from [RouterOS-api] by Social WiFi please visit their [repository].

Any contribution is welcome! Thanks.




[RouterOS-api]: <https://github.com/socialwifi/RouterOS-api>
[repository]: <https://github.com/socialwifi/RouterOS-api>
