
# transcrypt telscodes -n
# cd __target__
# rollup telscodes.js --o telscodes_bundle.js --f iife --name 'telscodes'

def filter_tel(tel:str, data:list):
    lst = []
    for telcode in data :
        if telcode['tel'].startswith(tel):
            lst.append(telcode)
    return lst

def result(tel,data):
    lst = filter_tel(tel,data)
    html = ''
    for telcode in lst:
        html += "<tr><td> {}</td><td> {}</td><td> {} </td></tr>".format(
             '7777', telcode['tel'], telcode['code'] )
    return html

#lst1 = filter_tel('24',data)
#print(lst1)
def action():
    tel = document.getElementById ('tel').value
    html = result('22' , data)
    alert(html)
    document.getElementById ('t') .innerHTML += html

action()