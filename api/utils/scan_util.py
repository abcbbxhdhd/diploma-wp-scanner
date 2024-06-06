import requests
from bs4 import BeautifulSoup
import re
from utils import llm_util


def check_license_txt(url):
    data = {
        'scan_type': 'Discovering license.txt',
        'is_discovered': False,
        'error': None
    }

    try:
        resp = requests.get(url + '/license.txt')
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200 and resp.text != '':
        data['is_discovered'] = True
        return data

    return data


def check_login_endpoint(url):
    data = {
        'scan_type': 'Discovering login endpoints',
        'is_discovered': False,
        'endpoints': [],
        'error': None
    }

    possible_endpoints = [
        '/login.php',
        '/wp-login.php',
        '/wp-admin/login.php',
        '/wp-admin/wp-login.php',
    ]

    for e in possible_endpoints:
        try:
            resp = requests.get(url + e)
        except Exception as e:
            data['error'] = str(e)
            return data

        if resp.status_code == 200 and resp.text != '':
            data['is_discovered'] = True
            data['endpoints'].append(e)

    return data


def check_wp_sitemap_xml(url):
    data = {
        'scan_type': 'Discovering wp-sitemap.xml',
        'is_discovered': False,
        'content': '',
        'error': None
    }

    try:
        resp = requests.get(url + '/wp-sitemap.xml')
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200 and resp.text != '':
        data['is_discovered'] = True
        data['content'] = resp.text
        return data

    return data


def check_wp_activate_php(url):
    data = {
        'scan_type': 'Discovering wp-activate.php',
        'is_discovered': False,
        'error': None
    }

    try:
        resp = requests.get(url + '/wp-activate.php')
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200:
        data['is_discovered'] = True
        return data

    return data


def check_wp_version(url):
    data = {
        'scan_type': 'Discovering wp-version',
        'is_discovered': False,
        'version': '',
        'error': None
    }

    try:
        resp = requests.get(url)
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        meta_tag = soup.find('meta', {'name': 'generator'})

        if meta_tag:
            content_attr = meta_tag.get('content')
            if 'WordPress' in content_attr:
                data['is_discovered'] = True
                data['version'] = content_attr[:content_attr.find('WordPress') + len('WordPress')].strip()
                return data

    return data


def check_xmlrpc_php(url):
    data = {
        'scan_type': 'Discovering xmlrpc.php',
        'is_discovered': False,
        'endpoints': [],
        'error': None
    }

    possible_endpoints = [
        '/xmlrpc.php',
        '/xml-rpc.php',
    ]

    for e in possible_endpoints:
        try:
            resp = requests.get(url + e)
        except Exception as e:
            data['error'] = str(e)
            return data

        if resp.status_code == 405:
            data['is_discovered'] = True
            data['endpoints'].append(e)

    return data


def check_wpcron_php(url):
    data = {
        'scan_type': 'Discovering wp-cron.php',
        'is_discovered': False,
        'error': None
    }

    try:
        resp = requests.get(url + '/wp-cron.php')
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200:
        data['is_discovered'] = True

    return data


def check_proxy_oembed_requests(url):
    data = {
        'scan_type': 'Checking if the application is vulnerable to proxied oEmber requests',
        'is_discovered': False,
        'error': None
    }

    try:
        resp = requests.get(url + '/wp-json/oembed/1.0/proxy')
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code != 401 or resp.status_code != 404:
        data['is_discovered'] = True

    return data


def find_used_plugins(url):
    data = {
        'scan_type': 'Discovering used plugins',
        'is_discovered': False,
        'pluginLinks': [],
        'error': None
    }

    to_match = '/wp-content/plugins'

    try:
        resp = requests.get(url)
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        matched_elements = soup.find_all(attrs={'src': re.compile(to_match)})
        if matched_elements:
            data['is_discovered'] = True
            for element in matched_elements:
                if element.get('src') not in data['pluginLinks']:
                    data['pluginLinks'].append(element.get('src'))

    return data


def find_used_themes(url):
    data = {
        'scan_type': 'Discovering used themes',
        'is_discovered': False,
        'themesLinks': [],
        'error': None
    }

    to_match = '/wp-content/themes'

    try:
        resp = requests.get(url)
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        matched_elements = soup.find_all(attrs={'src': re.compile(to_match)})
        if matched_elements:
            data['is_discovered'] = True
            for element in matched_elements:
                if element.get('src') not in data['themesLinks']:
                    data['themesLinks'].append(element.get('src'))

    return data


def find_used_includes(url):
    data = {
        'scan_type': 'Discovering used includes',
        'is_discovered': False,
        'includesLinks': [],
        'error': None
    }

    to_match = '/wp-includes'

    try:
        resp = requests.get(url)
    except Exception as e:
        data['error'] = str(e)
        return data

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        matched_elements = soup.find_all(attrs={'src': re.compile(to_match)})
        if matched_elements:
            data['is_discovered'] = True
            for element in matched_elements:
                if element.get('src') not in data['includesLinks']:
                    data['includesLinks'].append(element.get('src'))

    return data


def execute_full_scan(url):

    if url[-1] == '/':
        url = url[:-1]

    license_txt = check_license_txt(url)
    login_endpoint = check_login_endpoint(url)
    wp_sitemap_xml = check_wp_sitemap_xml(url)
    wp_activate_php = check_wp_activate_php(url)

    wp_version = check_wp_version(url)
    if wp_version['is_discovered']:
        wp_version = llm_util.ask_wpversion_details(wp_version['version'])

    xmlrpc_php = check_xmlrpc_php(url)
    wp_cron_php = check_wpcron_php(url)

    oembed_reqs = check_proxy_oembed_requests(url)
    used_includes = find_used_includes(url)

    used_plugins = find_used_plugins(url)
    if used_plugins['is_discovered']:
        used_plugins = llm_util.ask_plugins_details(used_includes['pluginLinks'])

    used_themes = find_used_themes(url)
    if used_themes['is_discovered']:
        used_themes = llm_util.ask_themes_details(used_themes['themesLinks'])

    return {
        "license_txt": license_txt,
        "login_endpoint": login_endpoint,
        "wp_sitemap_xml": wp_sitemap_xml,
        "wp_activate_php": wp_activate_php,
        "wp_version": wp_version,
        "wp_cron_php": wp_cron_php,
        "oembed_reqs": oembed_reqs,
        "used_includes": used_includes,
        "used_plugins": used_plugins,
        "used_themes": used_themes,
        "xmlrpc_php": xmlrpc_php,
    }

