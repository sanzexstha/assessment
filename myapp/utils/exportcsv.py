from django.http import HttpResponse
import csv
 

def nested_getattr(obj, attribute, split_rule='__'):
    """
    This function is responsible for getting the nested record from the given obj parameter
    :param obj: whole item without splitting
    :param attribute: field after splitting
    :param split_rule:
    :return:
    """
    split_attr = attribute.split(split_rule)
    for attr in split_attr:
        if not obj:
            break
        obj = getattr(obj, attr)
    return obj


def export_to_csv(queryset, fields, titles, file_name):

 
    model = queryset.model
    response = HttpResponse(content_type='text/csv')
    # force download
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(file_name)
    # the csv writer
    writer = csv.writer(response)
    if fields:
        headers = fields
        if titles:
            titles = titles
        else:
            titles = headers
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)
        titles = headers

    # Writes the title for the file
    writer.writerow(titles)

    # write data rows
    for item in queryset:
        writer.writerow([nested_getattr(item, field) for field in headers])
    return response