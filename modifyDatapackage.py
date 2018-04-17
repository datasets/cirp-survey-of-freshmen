from datapackage import Package

package = Package('datapackage.json')
descriptions = {14: "Survey of Full-Time Freshmen by Institutional Type",
    6: "Institutions Participating in the 2014 CIRP Freshman Survey",
    12: "Estimated Standard Errors of Percentages for Comparison Groups of Various Sizes"}

for resource in package.descriptor['resources']:
    key = len(resource['schema']['fields'])
    resource['description'] = descriptions[key]
    myDict[key] += 1

package.commit()
package.save('datapackage.json')