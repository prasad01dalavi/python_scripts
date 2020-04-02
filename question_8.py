'''
Protocol
|  Can be ignored
| |  Prefix
| |  |                                         Time since route learned (age)
| |  |                                              |
| |  |                AD  Metric       Next Hop     |      Exit Interface
| |  |                 |    |            |          |         |
i L2 84.38.34.45/32 [115/20400] via 2.120.13.35, 1d10h, Bundle-Ether11
'''

route_table = """
i L2 84.38.34.45/32 [115/20400] via 2.120.13.35, 1d10h, Bundle-Ether11
                    [115/20400] via 2.120.13.37, 1d10h, Bundle-Ether10
                    [115/20400] via 2.120.13.39, 1d10h, Bundle-Ether9
                    [115/20400] via 2.120.13.33, 1d10h, Bundle-Ether8
i L2 84.38.34.2/32 [115/20130] via 2.120.13.39, 10w1d, Bundle-Ether9
i L2 84.38.34.3/32 [115/20120] via 2.120.13.37, 1d10h, Bundle-Ether10
i L2 84.38.34.4/32 [115/20900] via 2.120.13.39, 6w1d, Bundle-Ether9
B    1.0.0.0/24 [20/900] via 2.127.241.243, 1w6d
B    1.0.4.0/22 [20/1000] via 195.66.224.21, 5d22h
B    1.0.4.0/24 [20/1000] via 195.66.224.21, 5d22h
B    1.0.5.0/24 [20/1000] via 195.66.224.21, 5d22h
B    1.0.6.0/24 [20/1000] via 195.66.224.21, 5d22h
B    1.0.7.0/24 [20/1000] via 195.66.224.21, 5d22h
S    84.38.36.0/24 is directly connected, 11w5d, Null0
S    84.38.36.59/32 [1/0] via 84.38.32.94, 11w5d, TenGigE0/7/0/31/3.22
S    84.38.36.60/32 [1/0] via 84.38.32.96, 11w5d, TenGigE0/7/0/31/3.2
S    90.197.16.2/32 [1/0] via 84.38.32.96, 11w5d, TenGigE0/7/0/31/3.2
S    192.0.2.0/24 is directly connected, 11w5d, Null0
C    2.120.13.32/31 is directly connected, 11w1d, Bundle-Ether8
C    2.120.13.34/31 is directly connected, 11w2d, Bundle-Ether11
C    2.120.13.36/31 is directly connected, 1d11h, Bundle-Ether10
C    2.120.13.38/31 is directly connected, 10w1d, Bundle-Ether9
C    2.127.241.68/31 is directly connected, 11w5d, Bundle-Ether1087
"""

import json


logs = []
records = route_table.split("\n")
past_tokens = []

for index, record in enumerate(records):
    # print(f'[INFO] Processing Record: {record}')
    # Remove blank spaces which are more than one
    record = ' '.join(record.split())
    tokens = record.split()
    token_length = len(tokens)
    complete_data = ''
    if 'via' in record:
        via_index = tokens.index('via')
        left_missing_count = 4 - via_index
        right_missing_count = 8 - token_length - left_missing_count
        if left_missing_count == 0 and right_missing_count == 0:
            # we have all data records
            complete_data = tokens    

        if left_missing_count == 1:
            complete_data = tokens    

        if left_missing_count > 1:
            left_data = past_tokens[:left_missing_count]
            complete_data = left_data + tokens
        
        if right_missing_count > 0:
            complete_data = tokens + past_tokens[-(right_missing_count):]
            past_tokens = complete_data

        if len(complete_data) == 7:
            complete_data = [complete_data[0],'L2'] + complete_data[1:] 

        print(f'[INFO] Via Connected: {complete_data}')
        past_tokens = complete_data
        ad_metric = complete_data[3]
        ad_metric_string = ad_metric[1:-1]
        ad = ad_metric_string.split("/")[0]
        metric = ad_metric_string.split("/")[1]
        logs.append({
            'protocol': complete_data[0],
            'can_be_ignored': complete_data[1],
            'prefix': complete_data[2],
            'ad': ad,
            'metric': metric,
            'next_hop': complete_data[5],
            'time_since_route_learned(age)': complete_data[6],
            'exit_interface': complete_data[7]
        })
    
    if 'directly' in record:
        tokens = \
            [tokens[0], 'L2', tokens[1], '', '', '', tokens[-2], tokens[-1]]
        print(f'[INFO] Directly Connected: {tokens}')
        logs.append({
                'protocol': tokens[0],
                'can_be_ignored': tokens[1],
                'prefix': tokens[2],
                'ad': tokens[3],
                'metric': tokens[4],
                'next_hop': tokens[5],
                'time_since_route_learned(age)': tokens[6],
                'exit_interface': tokens[7],
        })


with open('structured_data.json', 'w') as f:
    json.dump(logs, f)
    print(f'\n[INFO] Structured Data saved in file: structured_data.json!')
