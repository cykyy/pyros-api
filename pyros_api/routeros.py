try:
    import routeros_api
except Exception as eee:
    print(':Error: Some modules are missing. {}'.format(eee))


class RosCall:

    def __init__(self, ros_ip, username='admin', password='', port=8728,
                 plaintext_login=False, use_ssl=False, ssl_verify=True, ssl_verify_hostname=True, ssl_context=None):

        # credentials saves to global
        self._mikrotik_ip = ros_ip
        self._username = username
        self._password = password
        self._port = port
        self._plaintext_login = plaintext_login
        self._use_ssl = use_ssl
        self._ssl_verify = ssl_verify
        self._ssl_verify_hostname = ssl_verify_hostname
        self._ssl_context = ssl_context

        self.connection = None
        self.api = None
        # deprecated and soon will get removed
        '''try:
            # connecting with ros
            self.connection = routeros_api.RouterOsApiPool(host=self._mikrotik_ip, username=self._username,
                                                           password=self._password, port=self._port,
                                                           plaintext_login=self._plaintext_login, use_ssl=self._use_ssl,
                                                           ssl_verify=self._ssl_verify,
                                                           ssl_verify_hostname=self._ssl_verify_hostname,
                                                           ssl_context=self._ssl_context)

            self.connection.set_timeout(5)
            self.api = self.connection.get_api()
            # print(connection.connected)
        except Exception as rce:
            print(':Error: connecting with routerOS! {}'.format(rce))'''

    def login(self):
        try:
            # connecting with ros
            self.connection = routeros_api.RouterOsApiPool(host=self._mikrotik_ip, username=self._username,
                                                           password=self._password, port=self._port,
                                                           plaintext_login=self._plaintext_login, use_ssl=self._use_ssl,
                                                           ssl_verify=self._ssl_verify,
                                                           ssl_verify_hostname=self._ssl_verify_hostname,
                                                           ssl_context=self._ssl_context)

            self.connection.set_timeout(5)
            self.api = self.connection.get_api()
        except Exception as rce:
            print(':Error: connecting with routerOS! {}'.format(rce))

    # returns all ppp secret with desired values. if specific _ppp given then returns that ppp secret only.
    def get_ppp_secret(self, _ppp=''):
        ppp_list_dict = []
        try:
            list_ppp = self.api.get_resource('/ppp/secret')
            if _ppp:
                ppp_list_dict = list_ppp.get(name=_ppp)
            else:
                ppp_list_dict = list_ppp.get()
        except Exception as gc:
            print(':Error: in accessing ppp secret list of dictionary! detailed: {}'.format(gc))
        ppp_secret_all = []
        ppp_secret_dict = {}

        for x in ppp_list_dict:
            ppp_secret_dict.update({'c_ident': x.get('name')})
            ppp_secret_dict.update({'p_pw': x.get('password')})

            if x.get('disabled') == 'false':
                val = False
            else:
                val = True
            ppp_secret_dict.update({'has_suspended': val})
            ppp_secret_dict.update({'profile': x.get('profile')})
            ppp_secret_dict.update({'last_logged_out': x.get('last-logged-out')})
            ppp_secret_dict.update({'service_type': x.get('service')})
            ppp_secret_dict.update({'remote-address': x.get('remote-address')})
            ppp_secret_all.append(ppp_secret_dict.copy())
        return ppp_secret_all

    # returns only enabled ppp secret
    def get_enabled_ppp(self, rtr_clients_all):
        rtr_clients = rtr_clients_all
        ena_clients = []
        for x in rtr_clients:
            if not x.get('has_suspended'):
                ena_clients.append(x)
        return ena_clients

    # returns only disabled ppp secret
    def get_disabled_ppp(self, rtr_clients_all):
        rtr_clients = rtr_clients_all
        disa_clients = []
        for x in rtr_clients:
            if x.get('has_suspended'):
                disa_clients.append(x)
        return disa_clients

    # setting a ppp secret enable. receiving only client pppoe name (eg: GCN1)
    def set_ppp_enable(self, client_id):
        try:
            list_ppp = self.api.get_resource('/ppp/secret')
            list_ppp.set(id=client_id, disabled='no')
            return True
        except Exception as _e:
            print("{} may not exist on router! detailed: ".format(client_id), _e)
            return False

    # setting a client disable. receiving only client pppoe name (eg: GCN1)
    def set_ppp_disable(self, client_id):
        # print('disabling clients:', client_id)
        try:
            list_ppp = self.api.get_resource('/ppp/secret')
            list_ppp.set(id=client_id, disabled='yes')
            return True
        except Exception as _e:
            print("{} may not exist on router! detailed: ".format(client_id), _e)
            return False

    def add_ppp_secret(self, _secret):
        _name = ''
        _password = ''
        _profile = 'default'
        _has_suspended = False
        _service = 'pppoe'
        _comment = ''
        _profile_ros = self.get_profile()
        try:
            _name = _secret.get('c_ident')
            _password = str(_secret.get('p_pw'))

            if _secret.get('profile'):
                _profile = _secret.get('profile')

            if _secret.get('service_type'):
                _service = _secret.get('service_type')

            if _secret.get('has_suspended'):
                _has_suspended = True

            if _secret.get('comment'):
                _comment = _secret.get('comment')

        except Exception as ee:
            print(":Error: during parsing data from received ppp secrets. detailed: {}".format(ee))

        if _secret.get('profile') in _profile_ros:
            try:
                list_ppp = self.api.get_resource('/ppp/secret')
                list_ppp.add(name=_name, password=_password, service='pppoe', profile=_profile, comment=_comment)
                # print(self.list_ppp.get(name=_name))
                # disabling the client if has_suspended True
                if _has_suspended is True:
                    _try_res = self.set_ppp_disable(_name)
                    if _try_res:
                        if self.is_active_ppp(_name):
                            self.remove_active_ppp_secret(_name)
                return True
            except Exception as e:
                print(':Error: detailed:', e)
                return False
        else:
            print(
                ":Error: during adding new client on router. perhaps profile {} didn't matched?".format(
                    _profile))
            return False

    # update password on function
    def update_secret_password(self, _secret_name, pw):
        try:
            list_ppp = self.api.get_resource('/ppp/secret')
            list_ppp.set(id=_secret_name, password=pw)
            # kicking out from active list
            self.remove_active_ppp_secret(_secret_name)
            return True
        except Exception as e:
            print(':Error: occurred during updating/setting password from crm to rtr. {}'.format(e))
            return False

    # update service-package/profile
    def update_secret_profile(self, _secret_name, _profile):
        try:
            list_ppp = self.api.get_resource('/ppp/secret')
            list_ppp.set(id=_secret_name, profile=_profile)
            # checking changed package client is active on routerOS. if so then remove from active.
            active_clients = self.get_active_ppp()
            for x in active_clients:
                if x.get('rtr_active_name') == _secret_name:
                    self.remove_active_ppp_secret(_secret_name)
            return True
        except Exception as e:
            print(':Error: occurred during updating/setting profile on routerOS. {}'.format(e))
            return False

    def remove_active_ppp_secret(self, _secret_name):
        try:
            list_active = self.api.get_resource('/ppp/active')
            _active = list_active.get(name=_secret_name)
            if _active:
                list_active.remove(id=_active[0].get('id'))
                return True
            else:
                return False
        except Exception as _re:
            print(':Error: during removing ppp secret. detailed: {}'.format(_re))
            return False

    # checking if given ppp secret is active or not
    def is_active_ppp(self, _secret_name):
        try:
            list_active = self.api.get_resource('/ppp/active')
            _active = list_active.get(name=_secret_name)
            if _active:
                return True
            else:
                return False
        except Exception as _e:
            print(':Error: during checking is_active_ppp. detailed: {}'.format(_e))

    # returns all active clients from routerOS. if no-one active then returns empty list.
    # if specific pppoe is given as param on _ppp and that pppoe is active now then returns that pppoe with all info's.
    # if specific pppoe not active then returns empty dictionary.
    def get_active_ppp(self, _secret_name=''):
        active_secrets = []
        active_secrets_dict = {}
        active_secrets_np = []
        try:
            list_active = self.api.get_resource('/ppp/active')
            active_secrets_np = list_active.get()
        except Exception as acn:
            print(':Error: {}'.format(acn))

        for x in active_secrets_np:
            active_secrets_dict.update({'rtr_active_name': x.get('name')})
            active_secrets_dict.update({'rtr_active_ip': x.get('address')})
            active_secrets_dict.update({'rtr_active_mac': x.get('caller-id')})
            active_secrets.append(active_secrets_dict.copy())
            active_secrets_dict.clear()

        # if any ppp secret is given then return only that secret info
        if _secret_name:
            for xp in active_secrets:
                if _secret_name == xp.get('rtr_active_name'):
                    return xp
            return {}

        return active_secrets

    # returns connection state as True or False with the routerOS, on the fly
    def check_connection_ros(self):
        connection = routeros_api.RouterOsApiPool(host=self._mikrotik_ip, username=self._username,
                                                  password=self._password, plaintext_login=True)
        connection.set_timeout(5)  # we can set timeout -> tested on playground
        connection.get_api()
        return connection.connected
        # returns True/False

    # returns all the profiles as list from routerOS
    def get_profile(self):
        list_profile = self.api.get_resource('/ppp/profile')
        profile_response = list_profile.get()
        profile_list = []
        for x in profile_response:
            profile_list.append(x.get('name'))
        return profile_list

    # returns all the original functions from the routerOS-api by socialwifi
    def ros_api_raw(self):
        return self.api

    # disconnect from the routerOS socket
    def disconnect(self):
        self.connection.disconnect()
