#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch-create ownCloud users
"""
__author__ = "Constantin Kraft <c@onstant.in>"

import sys
import argparse

import owncloud
from owncloud.owncloud import HTTPResponseError
import csv

API_URL = ''
# User needs Admin permissions
OC_USER = ''
OC_PASS = ''

oc = owncloud.Client(API_URL)


# authenticate with ownCloud
def authenticate():
    try:
        oc.login(OC_USER, OC_PASS)
        print("Authentifizierung erfolgreich")

    except Exception as e:
        print("Authetifizierung fehlgeschlagen: ")
        print(e)


# create user
def create_user(username, password):
    try:
        return oc.create_user(username, password)
    except Exception as e:
        print("Anlegen des Users {} mit Passwort {} fehlgeschlagen".format(username, password))
        print(e)

# add user to existing group
def add_user_to_group(username, group):
    try:
        return oc.add_user_to_group(username, group)
    except Exception as e:
        print("Hinzufügen des Users {} zur Gruppe {} fehlgeschlagen".format(username, group))
        print(e)

# create users
def create_users_from_file(file):
    try:
        with open(file, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                if create_user(row['Name'], row['Passwort']):
                    print("User {} erfolgreich angelegt!".format(row['Name']))
                if add_user_to_group(row['Name'], row['Alias']):
                    print("User {} erfolgreich zu Gruppe {} hinzugefügt!".format(row['Name'], row['Alias']))
    except Exception as e:
        print(e)

def main():
    authenticate()
    create_users_from_file(args.file)


if __name__ == "__main__":
    try:
        assert(API_URL != "")
        assert(OC_USER != "")
        assert(OC_PASS != "")
    except AssertionError:
        print("API-URL, Benutzername und Passwort müssen gesetzt sein!")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Mit diesem Skript lassen sich OwnCloud-User aus einer CSV-Datei einlesen"
                                                 " und anlegen")
    parser.add_argument('-f', '--file', help='Die CSV-Datei, aus der Username, Passwort und Gruppe gelesen werden sollen',
                        required=True)
    args = parser.parse_args()
    main()