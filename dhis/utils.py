def clean_data(data, geojson):
    '''

    :param data:
    :param geojson:
    :return:
    '''
    # create an a dict with an records key, that has empty list as value
    columns = {
        "records": []
    }
    # create an empty list that will hold all the organisation units found in the results
    organisationUnits = []

    '''
    Loop through the response data rows, create an empty dict to hold the records that we will extract,
    Get the organisations units that appear in the response and add them to the above organisationUnits list,
    Extract the Period of the response and and the values corresponding to the given dx during this period,
    Add the extracted  data to the records key in in the columns dict we created earier
    
    '''
    for i in range(len(data["rows"])):
        records = {}
        org = data['rows'][i][0]
        organisationUnits.append(org)
        pe = data['rows'][i][1]
        val = data['rows'][i][2]
        records['Organisation Unit'] = org
        records['Period'] = pe
        records['Value'] = float(val)
        columns['records'].append(records)

    # get unique organisation units
    unique_organisationUnits = set(organisationUnits)
    # create an empty dict to hold the final collected data
    collection = {
        "records":[{}]
    }
    # create key value pairs corresponding to a unique org Unit and the data it will hold
    for org in unique_organisationUnits:
        collection['records'][0][org] = [{"period": [], "value": [], "name": '', "average": ''}]
    # fill the key value pairs that we created with extracted data
    for x in unique_organisationUnits:
        for n in columns["records"]:
            org = n["Organisation Unit"]
            if x == org:
                collection['records'][0][x][0]["period"].append(n['Period'])
                collection['records'][0][x][0]["value"].append(n['Value'])
                tot = sum(collection['records'][0][x][0]["value"])
                av = tot / len(collection['records'][0][x][0]["period"])
                collection['records'][0][x][0]["average"] = av
                # get geojson data and add properties where the org IDs match. We use the unique org IDs for spatial join
                for i in range(len(geojson["features"])):
                    feat = geojson["features"][i]
                    id = feat["id"]
                    if x == id:
                        total = sum(collection['records'][0][x][0]["value"])
                        av = total / len(collection['records'][0][x][0]["period"])
                        feat["properties"]['average'] = av
    collection["geojson"] = geojson
    return collection
