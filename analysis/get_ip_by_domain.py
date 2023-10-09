import requests


def GetIPByDomainName(queryDomainName):
    r = requests.get('https://websites.ipaddress.com/' + queryDomainName)
    # print(r.status_code)  # 响应状态码
    result_txt = r.text  # 响应字符串
    result_list = result_txt.strip(',').split('\n')  # 利用换行符分隔为list对象

    myres = ''  # 以section来分割
    for line in result_list:
        line = line.strip('\n')
        if line.find('<section class="panel">') and line.find('</section>') >= 0:
            myres = line.strip(',').split('<section')

    sectionSummary_string = ''
    sectionLocation_string = ''
    sectionInformation_string = ''
    for every_section in myres:
        if every_section.find('Domain Summary') >= 0 or every_section.find(
                'Hostname Summary') >= 0:  # Domain Summary/ Hostname Summary对应的section
            sectionSummary_string = every_section[every_section.find('<table class'):every_section.find('</table>') + 8]
        elif every_section.find('IP Address and Server Location') >= 0:  # IP Address and Server Location对应的section
            sectionLocation_string = every_section[
                                     every_section.find('<table class'):every_section.find('</table>') + 8]
        elif every_section.find(
                'Website and Web Server Information') >= 0:  # Website and Web Server Information对应的section
            sectionInformation_string = every_section[
                                        every_section.find('<table class'):every_section.find('</table>') + 8]

    result = {'IPAddress': '',
              'Longitude': '',
              'Latitude': '',
              'Location': '',
              'Domain_Creation_Date': '',
              'Domain_Age': '',
              'Global_Traffic_Rank': '',
              'Estimated_Visitors': '',
              'Estimated_Page_Impressions': '',
              'Website_Abstract': '',
              'Website_Host': '',
              'Server_Software': '',
              'Median_Page_Load_Time': '',
              'Number_of_Sites_Linking_In': ''
              }
    if sectionLocation_string.find('IPv6 Addresses') >= 0:
        result['IPAddress'] = sectionLocation_string[
                              sectionLocation_string.find('IPv4 Addresses') + 55:sectionLocation_string.find(
                                  'IPv6 Addresses') - 28].replace('</li><li>', ',')
    else:
        if sectionLocation_string.find('IPv4 Addresses') >= 0:
            result['IPAddress'] = sectionLocation_string[
                                  sectionLocation_string.find('IPv4 Addresses') + 55:sectionLocation_string.find(
                                      '</tbody></table>') - 20].replace('</li><li>', ',')
        else:
            result['IPAddress'] = sectionLocation_string[
                                  sectionLocation_string.find('IPv4 Addresses') + 51:sectionLocation_string.find(
                                      '</tbody></table>') - 20].replace('</li><li>', ',')
    result['Longitude'] = sectionLocation_string[
                          sectionLocation_string.find('Longitude') + 18:sectionLocation_string.find('Timezone') - 18]
    result['Latitude'] = sectionLocation_string[
                         sectionLocation_string.find('Latitude') + 17:sectionLocation_string.find('Longitude') - 18]
    result['Location'] = sectionLocation_string[
                         sectionLocation_string.find('Location') + 17:sectionLocation_string.find('Latitude') - 18]
    result['Domain_Creation_Date'] = sectionSummary_string[
                                     sectionSummary_string.find('Domain Creation Date') + 57:sectionSummary_string.find(
                                         'Domain Age') - 25]
    result['Domain_Age'] = sectionSummary_string[
                           sectionSummary_string.find('Domain Age') + 43:sectionSummary_string.find('IP Address') - 25]
    result['Global_Traffic_Rank'] = sectionSummary_string[
                                    sectionSummary_string.find('Global Traffic Rank') + 28:sectionSummary_string.find(
                                        'Estimated Visitors') - 18]
    result['Estimated_Visitors'] = sectionSummary_string[
                                   sectionSummary_string.find('Estimated Visitors') + 27:sectionSummary_string.find(
                                       'Estimated Page Impressions') - 18]
    result['Estimated_Page_Impressions'] = sectionSummary_string[sectionSummary_string.find(
        'Estimated Page Impressions') + 35:sectionSummary_string.find('Domain Creation Date') - 18]
    if sectionInformation_string.find('Website Title') >= 0:
        result['Website_Abstract'] = sectionInformation_string[sectionInformation_string.find(
            'Website Abstract') + 50:sectionInformation_string.find('Website Title') - 18]
    else:
        result['Website_Abstract'] = sectionInformation_string[sectionInformation_string.find(
            'Website Abstract') + 50:sectionInformation_string.find('Website Host') - 18]
    result['Website_Host'] = sectionInformation_string[
                             sectionInformation_string.find('Website Host') + 21:sectionInformation_string.find(
                                 'Server Software') - 18]
    result['Server_Software'] = sectionInformation_string[
                                sectionInformation_string.find('Server Software') + 24:sectionInformation_string.find(
                                    'Median Page Load Time') - 18]
    result['Median_Page_Load_Time'] = sectionInformation_string[sectionInformation_string.find(
        'Median Page Load Time') + 30:sectionInformation_string.find('Number of Sites Linking In') - 18]
    result['Number_of_Sites_Linking_In'] = sectionInformation_string[sectionInformation_string.find(
        'Number of Sites Linking In') + 35:sectionInformation_string.find('</tbody></table>') - 10]
    return result



queryDomainName = 'github.com'
result = GetIPByDomainName(queryDomainName)
print('Domain Name:   ' + queryDomainName)
print('IPv4 Addresses:   ' + result['IPAddress'])
print('Location:   ' + result['Location'])
print('Longitude:   ' + result['Longitude'])
print('Latitude:   ' + result['Latitude'])
print('Domain Creation Date:   ' + result['Domain_Creation_Date'])
print('Domain Age:   ' + result['Domain_Age'])
print('Global Traffic Rank:   ' + result['Global_Traffic_Rank'])
print('Estimated Visitors:   ' + result['Estimated_Visitors'])
print('Estimated Page Impressions:   ' + result['Estimated_Page_Impressions'])
print('Website Abstract:   ' + result['Website_Abstract'])
print('Website Host:   ' + result['Website_Host'])
print('Server Software:   ' + result['Server_Software'])
print('Median Page Load Time:   ' + result['Median_Page_Load_Time'])
print('Number of Sites Linking In:   ' + result['Number_of_Sites_Linking_In'])
