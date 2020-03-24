"""
 Licensed to the Apache Software Foundation (ASF) under one or more
 contributor license agreements.  See the NOTICE file distributed with
 this work for additional information regarding copyright ownership.
 The ASF licenses this file to You under the Apache License, Version 2.0
 (the "License"); you may not use this file except in compliance with
 the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
import composer
import json

def main():
    return composer.sequence('input', composer.when(
        composer.action('choice-2fns',  { 'action': lambda args: { 'value': args['body']['number']%2 } }),
        composer.action('choice-increment', { 'action': lambda args: {'value': 2*args['body']['number']}}),
        composer.action('choice-double',  { 'action': lambda args: {'value': 1+args['body']['number']}}),
        # composer.action('choice-increment', { 'action': lambda args: { 'value': args['value']+1 }}),
        # composer.action('choice-double',  { 'action': lambda args: { 'value': args['value']*2 } }),
        ))

