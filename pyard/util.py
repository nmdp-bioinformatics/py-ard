# -*- coding: utf-8 -*-

#
#    seqann Sequence Annotation
#    Copyright (c) 2017 Be The Match operated by National Marrow Donor Program. All Rights Reserved.
#
#    This library is free software; you can redistribute it and/or modify it
#    under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation; either version 3 of the License, or (at
#    your option) any later version.
#
#    This library is distributed in the hope that it will be useful, but WITHOUT
#    ANY WARRANTY; with out even the implied warranty of MERCHANTABILITY or
#    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
#    License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this library;  if not, write to the Free Software Foundation,
#    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#    > http://www.fsf.org/licensing/licenses/lgpl.html
#    > http://www.opensource.org/licenses/lgpl-license.php
#
import os
import string
import random as r
from datetime import datetime, date
from six import integer_types, iteritems
import pandas as pd
import copy
import http.client
import pickle
import urllib.request
import zipfile
import re


# def all_macs(csv_file, url='hml.nmdp.org'):
#     # conn = http.client.HTTPSConnection(url, 443)
#     # conn.putrequest('GET', '/mac/api/codes')
#     # conn.endheaders()
#     # response = conn.getresponse().read().decode('utf8').splitlines()
#     data = [l.split("\t")[1:3] for l in response]
#     urllib.request.urlretrieve(url, 'numeric.v3.zip')
#     df = pd.DataFrame(data, columns=['Code','Alleles'])
#     df.to_csv(csv_file, header=True, index=False)
#     df['Alleles'] = df['Alleles'].apply(lambda x: x.split("/"))
#     mac_dict = df.set_index("Code").to_dict('index')
#     return mac_dict

def all_macs(csv_file, url='https://bioinformatics.bethematchclinical.org/HLA/numeric.v3.zip'):
    urllib.request.urlretrieve(url, 'numeric.v3.zip')
    zip_ref = zipfile.ZipFile('numeric.v3.zip', 'r')
    data_dir = os.path.dirname(__file__)
    zip_ref.extractall(data_dir)
    zip_ref.close()
    data = []
    out_file = data_dir + "/numer.v3.txt"
    with open(out_file, 'r') as f:
        for line in f:
            line = line.rstrip()
            if re.search("^\D", line) and not re.search("CODE", line) and not re.search("LAST", line):
                data.append(line.split("\t"))
        f.close()
    df = pd.DataFrame(data, columns=['Code','Alleles'])
    df.to_csv(csv_file, header=True, index=False)
    df['Alleles'] = df['Alleles'].apply(lambda x: x.split("/"))
    mac_dict = df.set_index("Code").to_dict('index')
    return mac_dict


def pandas_explode(df, column_to_explode):
    """
    Similar to Hive's EXPLODE function, take a column with iterable elements, and flatten the iterable to one element 
    per observation in the output table
    :param df: A dataframe to explod
    :type df: pandas.DataFrame
    :param column_to_explode: 
    :type column_to_explode: str
    :return: An exploded data frame
    :rtype: pandas.DataFrame
    """
    # Create a list of new observations
    new_observations = list()
    # Iterate through existing observations
    for row in df.to_dict(orient='records'):
        # Take out the exploding iterable
        explode_values = row[column_to_explode]
        del row[column_to_explode]
        # Create a new observation for every entry in the exploding iterable & add all of the other columns
        for explode_value in explode_values:
            # Deep copy existing observation
            new_observation = copy.deepcopy(row)
            # Add one (newly flattened) value from exploding iterable
            new_observation[column_to_explode] = explode_value
            # Add to the list of new observations
            new_observations.append(new_observation)
    # Create a DataFrame
    return_df = pd.DataFrame(new_observations)
    # Return
    return return_df


def _deserialize(data, klass):
    """
    Deserializes dict, list, str into an object.

    :param data: dict, list or str.
    :param klass: class literal, or string of class name.

    :return: object.
    """
    if data is None:
        return None

    if klass in integer_types or klass in (float, str, bool):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == date:
        return deserialize_date(data)
    elif klass == datetime:
        return deserialize_datetime(data)
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """
    Deserializes to primitive type.

    :param data: data to deserialize.
    :param klass: class literal.

    :return: int, long, float, str, bool.
    :rtype: int | long | float | str | bool
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = unicode(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """
    Return a original value.

    :return: object.
    """
    return value


def deserialize_date(string):
    """
    Deserializes string to date.

    :param string: str.
    :type string: str
    :return: date.
    :rtype: date
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def deserialize_datetime(string):
    """
    Deserializes string to datetime.

    The string should be in iso8601 datetime format.

    :param string: str.
    :type string: str
    :return: datetime.
    :rtype: datetime
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string


def deserialize_model(data, klass):
    """
    Deserializes list or dict to model.

    :param data: dict, list.
    :type data: dict | list
    :param klass: class literal.
    :return: model object.
    """
    instance = klass()

    if not instance.swagger_types:
        return data

    for attr, attr_type in iteritems(instance.swagger_types):
        if data is not None \
                and instance.attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize_list(data, boxed_type):
    """
    Deserializes a list and its elements.

    :param data: list to deserialize.
    :type data: list
    :param boxed_type: class literal.

    :return: deserialized list.
    :rtype: list
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """
    Deserializes a dict and its elements.

    :param data: dict to deserialize.
    :type data: dict
    :param boxed_type: class literal.

    :return: deserialized dict.
    :rtype: dict
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in iteritems(data)}
