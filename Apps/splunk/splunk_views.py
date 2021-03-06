# File: splunk_views.py
# Copyright (c) 2014-2020 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
# --


def _get_ctx_result(result, provides):

    ctx_result = {}
    headers = []
    processed_data = []

    param = result.get_param()
    summary = result.get_summary()
    data = result.get_data()

    ctx_result['param'] = param
    ctx_result["action_name"] = provides
    if summary:
        ctx_result['summary'] = summary

    if not data:
        ctx_result['data'] = {}
        return ctx_result

    if param.get("display"):
        headers = [x.strip() for x in param['display'].split(',')]

    else:
        for key in data[0].keys():
            if key[0] != '_':
                headers.append(key)

    for item in data:
        header_values = dict()
        for header in headers:
            header_values[header] = item.get(header)
        processed_data.append(header_values)

    ctx_result['data'] = data
    ctx_result['processed_data'] = processed_data
    ctx_result['headers'] = headers

    return ctx_result


def display_view(provides, all_app_runs, context):

    context['results'] = results = []
    for summary, action_results in all_app_runs:
        for result in action_results:
            ctx_result = _get_ctx_result(result, provides)
            if not ctx_result:
                continue
            results.append(ctx_result)

    return 'splunk_run_query.html'
